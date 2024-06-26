import base64
import os
from datetime import datetime, timedelta
import datetime
from functools import wraps
from io import BytesIO
from django import forms
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, FormView
from django.http import JsonResponse
from .models import *
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import *
import math
import aiofiles
from moviepy.editor import VideoFileClip
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Captain, CaptainTrip, CaptainTripStatus
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime


# ==================================================================================
api_view(['POST'])


def register_user(request):  # TP
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        contact_no = request.data.get('contact_no')
        address = request.data.get('address')

        if not contact_no:
            return JsonResponse({'msg': 'contact number is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            contact_no = int(contact_no)
        except ValueError:
            return JsonResponse({'msg': 'contact number must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        if len(str(contact_no)) != 10:
            return JsonResponse({'msg': 'Mobile number must be 10 digits'}, status=status.HTTP_400_BAD_REQUEST)

        if not address:
            return JsonResponse({'msg': 'Address is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name']
        )

        user_details = UserDetails.objects.create(
            user=user,
            contact_no=contact_no,
            address=address
        )

        return JsonResponse({'msg': 'Registered successfully'}, status=status.HTTP_201_CREATED)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================================================================================


# ==================================================================================
def is_within_radius(lat1, lon1, lat2, lon2, radius):
    R = 6371
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(
        d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c * 1000
    return distance <= float(radius)


@api_view(['POST'])  # TP
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_videosurl(request):
    try:
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        captain = request.user

        if latitude and longitude:
            campaigns = Campaign.objects.all()
            filtered_campaigns = []

            for campaign in campaigns:
                geo_fencing = json.loads(campaign.cm_geo_fencing)[0]
                if is_within_radius(float(latitude), float(longitude), float(geo_fencing['latitude']),
                                    float(geo_fencing['longitude']), geo_fencing['radius']):
                    filtered_campaigns.append(campaign)

            if filtered_campaigns:
                filtered_campaigns.sort(key=lambda campaign: (
                    math.sqrt(
                        (float(json.loads(campaign.cm_geo_fencing)[0]['latitude']) - float(latitude)) ** 2 +
                        (float(json.loads(campaign.cm_geo_fencing)[0]['longitude']) - float(longitude)) ** 2
                    )
                ))
                nearest_campaign = filtered_campaigns[0]
                campaign_serializer = CampaignSerializer(nearest_campaign, context={'request': request})

                video_files = campaign_serializer.data['cm_ad_video_file']
                video_urls = []

                for video_file in video_files:
                    video_urls.append(video_file)

                    VideoView.objects.create(
                        captain=captain,
                        campaign=nearest_campaign,
                        video_url=video_file,
                        viewed_at=timezone.now()
                    )

                return JsonResponse({
                    'status': 'success',
                    'message': 'Videos received',
                    'data': {'video_urls': video_urls}
                }, status=200)
            else:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Videos not available',
                    'data': [],
                }, status=404)

        return JsonResponse({'msg': 'Please provide latitude and longitude.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================================================================================

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_captain_details(request):
    captain_id = request.data.get('captain_id')

    if captain_id:
        try:
            captain_id = int(captain_id)
            captain = Captain.objects.get(captain_id=captain_id)
        except ValueError:
            return JsonResponse({"msg": "captain_id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        except Captain.DoesNotExist:
            return JsonResponse({"msg": "Captain not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        captain_serializer = CaptaindataSerializer(captain)
        return JsonResponse({'data': captain_serializer.data}, safe=False, status=status.HTTP_200_OK)
    else:
        try:
            captains = Captain.objects.all()
            captain_serializer = CaptaindataSerializer(captains, many=True)
            return JsonResponse({"data": captain_serializer.data}, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_captain_earn_points(request):
    captain_id = request.data.get('captain_id')
    if not captain_id:
        return JsonResponse({"msg": "Captain ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        captain_id = int(captain_id)
    except ValueError:
        return JsonResponse({"msg": "Captain ID must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        captain = Captain.objects.get(pk=captain_id)
    except Captain.DoesNotExist:
        return JsonResponse({"msg": "Captain not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        earn_points = EarnPoint.objects.filter(captain=captain)
        serializer = EarnPointSerializer(earn_points, many=True)
        return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def format_duration(duration):
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f"{days} day(s), {hours} hour(s), {minutes} minute(s)"
    elif hours > 0:
        return f"{hours} hour(s), {minutes} minute(s)"
    elif minutes > 0:
        return f"{minutes} minute(s), {seconds} second(s)"
    else:
        return f"{seconds} second(s)"


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def captain_check_in_out(request):
    try:
        user = request.user
        captain = Captain.objects.filter(user=user).first()
        if not captain:
            return Response({'msg': 'Captain not found'}, status=status.HTTP_404_NOT_FOUND)

        current_trips = CaptainTrip.objects.filter(captain=captain, status=CaptainTripStatus.RUNNING)

        if current_trips.exists():
            current_trip = current_trips.latest('check_in')
            current_trip.check_out = timezone.now()
            current_trip.status = CaptainTripStatus.CLOSE
            total_duration = current_trip.check_out - current_trip.check_in
            current_trip.total_hours = total_duration
            print(total_duration)
            current_trip.save()

            formatted_total_hours = format_duration(total_duration)
            return Response({
                'status': 'success',
                'message': 'Checked out successfully',
                'data': {
                    'check_in': current_trip.check_in.strftime('%Y-%m-%d %H:%M:%S'),
                    'check_out': current_trip.check_out.strftime('%Y-%m-%d %H:%M:%S'),
                    'total_hours': formatted_total_hours,
                    'status': current_trip.status
                }
            }, status=status.HTTP_200_OK)
        else:
            new_trip = CaptainTrip.objects.create(captain=captain, status=CaptainTripStatus.RUNNING)
            return Response({
                'status': 'success',
                'message': 'Checked in successfully',
                'data': {
                    'check_in': new_trip.check_in.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': new_trip.status
                }
            }, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_captain_trips(request):
    try:
        captain_id = request.data.get('captain_id')

        if captain_id != None:
            captain = Captain.objects.get(pk=captain_id)
            trips = CaptainTrip.objects.filter(captain=captain)
        else:

            trips = CaptainTrip.objects.all()

        trips_data = []

        for trip in trips:
            trip_data = {
                'id': trip.id,
                'check_in': trip.check_in.strftime('%Y-%m-%d %H:%M:%S'),
                'check_out': trip.check_out.strftime('%Y-%m-%d %H:%M:%S') if trip.check_out else None,
                'total_hours': str(trip.total_hours) if trip.total_hours else None,
                'status': trip.status,
            }
            trips_data.append(trip_data)

        return Response({
            'status': 'success',
            'message': 'ok',
            'data': trips_data
        }, status=status.HTTP_200_OK)

    except Captain.DoesNotExist:
        return Response({'msg': 'Captain not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return JsonResponse({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def get_campaign_data(request):
    try:

        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        campaign_id = request.POST.get('campaign_id')
        client_id = request.POST.get('client_id')

        campaigns = Campaign.objects.all()

        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = None

        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = datetime.now().date()

        if end_date_str and not start_date_str:
            return JsonResponse({'error': 'Start date must be provided'}, status=400)

        if start_date and end_date:
            campaigns = campaigns.filter(cm_start_date__gte=start_date, cm_start_date__lte=end_date)
        elif start_date:
            campaigns = campaigns.filter(cm_start_date__gte=start_date)
        elif end_date:
            campaigns = campaigns.filter(cm_start_date__lte=end_date)

        if campaign_id:
            campaigns = campaigns.filter(campaign_id=campaign_id)

        if client_id:
            campaigns = campaigns.filter(client_id=client_id)

        page_number = request.POST.get('page_number')
        paginator = Paginator(campaigns, 10)

        try:
            campaigns = paginator.page(page_number)
        except PageNotAnInteger:
            campaigns = paginator.page()
        except EmptyPage:
            campaigns = paginator.page(paginator.num_pages)

        if not campaigns:
            return JsonResponse({'st': 'success', 'msg': 'data not available'}, status=status.HTTP_200_OK)

        serialized_data = []
        for campaign in campaigns:
            serialized_data.append({
                'campaign_id': campaign.campaign_id,
                'client_id': campaign.client_id,
                'geo_fencing': campaign.cm_geo_fencing,
                'ad_video_file': campaign.cm_ad_video_file,
                'no_of_repetition': campaign.cm_no_of_repetition,
                'start_date': campaign.cm_start_date,
                'tenure': campaign.cm_tenure,
                'end_date': campaign.cm_end_date,
                'amount': campaign.cm_amount,
                'status': campaign.cm_status,
            })

        return JsonResponse({'st': 'success', 'msg': 'ok', 'data': serialized_data}, safe=False)

    except Exception as e:
        return JsonResponse({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def verify_contact(request):
    c_contact_no = request.data.get('c_contact_no')

    if not c_contact_no:
        return JsonResponse({'msg': 'Contact number is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        captain = Captain.objects.get(c_contact_no=c_contact_no)
        return JsonResponse({'msg': 'Contact number verified. OTP sent.'}, status=status.HTTP_200_OK)

    except Captain.DoesNotExist:
        return JsonResponse({'msg': 'Invalid contact number'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return JsonResponse({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def verify_otp(request):
    serializer = CaptainOTPSerializer(data=request.data)

    if serializer.is_valid():
        c_contact_no = serializer.validated_data['c_contact_no']
        otp = serializer.validated_data['otp']

        try:
            captain = Captain.objects.get(c_contact_no=c_contact_no)

            if otp == "1234":
                if not captain.user:
                    return JsonResponse({'msg': 'Captain does not have an account.'},
                                        status=status.HTTP_400_BAD_REQUEST)

                refresh = RefreshToken.for_user(captain.user)

                refresh['user_id'] = captain.user.id
                refresh['captain_id'] = captain.captain_id

                tokens = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                return JsonResponse({
                    'st': 'success',
                    'message': 'Login successful',
                    'data': tokens,
                }, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'msg': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        except Captain.DoesNotExist:
            return JsonResponse({'msg': 'Invalid contact number'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return JsonResponse({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
