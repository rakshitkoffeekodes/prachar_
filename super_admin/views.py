import base64
import os
from datetime import datetime, timedelta
import datetime
from functools import wraps
from io import BytesIO
from django import forms
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from p_app.models import *
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from p_app.models import Captain


def user_two_factor_auth_data_create(*, user) -> TwoFactorData:
    print('--------->', user)
    user_data = TwoFactorData.objects.filter(user=user).first()
    print(user)
    if user_data != None:
        two_factor_auth_data = user_data
    else:
        print('--------')
        two_factor_auth_data = TwoFactorData.objects.create(
            user=user,
            otp_secret=pyotp.random_base32()
        )

    return two_factor_auth_data


class AdminSetupTwoFactorAuthView(TemplateView):
    print('-----')
    template_name = "admin/setup.html"

    def post(self, request, *args, **kwargs):
        print("AdminSetupTwoFactorAuthView POST method called")
        context = {}
        user = request.user
        try:
            two_factor_auth_data = user_two_factor_auth_data_create(user=user)
            otp_secret = two_factor_auth_data.otp_secret

            context["otp_secret"] = otp_secret
            context["qr_code"] = two_factor_auth_data.generate_qr_code(
                name=user.email,
                username=user.username
            )
            print('-=--==-=-', two_factor_auth_data)
        except ValidationError as exc:
            context["form_errors"] = exc.messages

        return self.render_to_response(context)


class AdminConfirmTwoFactorAuthView(FormView):
    template_name = "admin/confirm.html"  # Use the same template as setup.html for OTP verification
    success_url = reverse_lazy("admin:index")

    class Form(forms.Form):
        otp1 = forms.CharField(max_length=1, widget=forms.TextInput(
            attrs={'maxlength': '1', 'class': 'otp-input', 'pattern': '[0-9]'}))
        otp2 = forms.CharField(max_length=1, widget=forms.TextInput(
            attrs={'maxlength': '1', 'class': 'otp-input', 'pattern': '[0-9]'}))
        otp3 = forms.CharField(max_length=1, widget=forms.TextInput(
            attrs={'maxlength': '1', 'class': 'otp-input', 'pattern': '[0-9]'}))
        otp4 = forms.CharField(max_length=1, widget=forms.TextInput(
            attrs={'maxlength': '1', 'class': 'otp-input', 'pattern': '[0-9]'}))
        otp5 = forms.CharField(max_length=1, widget=forms.TextInput(
            attrs={'maxlength': '1', 'class': 'otp-input', 'pattern': '[0-9]'}))
        otp6 = forms.CharField(max_length=1, widget=forms.TextInput(
            attrs={'maxlength': '1', 'class': 'otp-input', 'pattern': '[0-9]'}))

        def clean(self):
            cleaned_data = super().clean()
            otp1 = cleaned_data.get('otp1')
            otp2 = cleaned_data.get('otp2')
            otp3 = cleaned_data.get('otp3')
            otp4 = cleaned_data.get('otp4')
            otp5 = cleaned_data.get('otp5')
            otp6 = cleaned_data.get('otp6')

            combined_otp = otp1 + otp2 + otp3 + otp4 + otp5 + otp6

            # Example validation logic, replace with your own
            two_factor_auth_data = TwoFactorData.objects.filter(
                user=self.user
            ).first()

            if not two_factor_auth_data:
                raise ValidationError('2FA not set up.')

            if not two_factor_auth_data.validate_otp(combined_otp):
                raise ValidationError('Invalid OTP Code.')

            self.two_factor_auth_data = two_factor_auth_data

            return cleaned_data

    def get_form_class(self):
        return self.Form

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.user = self.request.user
        return form

    def form_valid(self, form):
        form.two_factor_auth_data.rotate_session_identifier()
        self.request.session['2fa_token'] = str(form.two_factor_auth_data.session_identifier)

        refresh = RefreshToken.for_user(self.request.user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        print('access_token', access_token, 'refresh_token', refresh_token)

        self.request.session['access_token'] = access_token
        self.request.session['refresh_token'] = refresh_token

        return redirect(self.success_url)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def view_qrcode(request, user_id):
    get_user = User.objects.get(pk=user_id)
    get_otp_secret = TwoFactorData.objects.get(user=get_user)
    otp_secret = get_otp_secret.otp_secret

    # Generate QR code
    issuer = get_user.username  # Replace with your issuer name
    account_name = get_user.username  # or use any other identifier for the account
    otp_uri = f"otpauth://totp/{issuer}:{account_name}?secret={otp_secret}&issuer={issuer}"

    # Debugging: Print the OTP URI to verify its value
    print("OTP URI:", otp_uri)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=4,
    )
    qr.add_data(otp_uri)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return JsonResponse({'qr_code': img_str, 'username': get_user.username})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@login_required
def regenerate_qr_code_view(request, user_id):
    user = User.objects.get(pk=user_id)

    # Regenerate the OTP secret
    if hasattr(user, 'two_factor_auth_data'):
        print('---------')
        print('////////')
        user.two_factor_auth_data.otp_secret = pyotp.random_base32()
        print('---------', user.two_factor_auth_data.otp_secret)
        user.two_factor_auth_data.rotate_session_identifier()
        print('---------', user.two_factor_auth_data.rotate_session_identifier())
        user.two_factor_auth_data.save()

    # Log out the user
    logout(request)
    print('-----------')
    # Add a message to inform the user to log in again
    messages.success(request, 'QR code regenerated. Please log in again to continue.')

    return redirect('admin:login')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        mobile_no = request.POST['mobile_no']
        address = request.POST['address']
        print(username, password, mobile_no, address)
        user = User.objects.filter(username=username).first()
        print('----->', user)
        if user is None:
            mobile = UserDetails.objects.filter(contact_no=mobile_no).first()
            if mobile is None:
                User.objects.create_user(
                    username=username,
                    password=password
                )

                UserDetails.objects.create(
                    contact_no=mobile_no,
                    address=address
                )

                return redirect('admin:setup-2fa')

            else:
                return render(request, 'admin/sign-up.html', {'message': 'Mobile Number is already exist'})
        else:
            return render(request, 'admin/sign-up.html', {'message': 'Username is already exist'})
    else:
        return render(request, 'admin/sign-up.html')


def custom_logout_view(request):
    logout(request)
    return redirect('admin:login')


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_captain_create(request):
    state = State.objects.all()
    city = City.objects.all()
    device = AssignDevice.objects.filter(ad_assign_status='Pending')

    if request.method == 'POST':
        c_name = request.POST['c_name']
        c_email = request.POST['c_email']
        c_contact_no = request.POST['c_contact_no']
        c_address = request.POST['c_address']
        state = request.POST['state']
        city = request.POST['city']
        c_documents = request.FILES.getlist('c_documents')
        license_number = request.POST['c_license_no']
        c_license_image = request.FILES.getlist('c_license_image')
        vi_vehicle_number = request.POST['vi_vehicle_no']
        vi_vehicle_image = request.FILES.getlist('vi_vehicle_image')
        vi_rc_book_image = request.FILES.getlist('vi_rc_book_image')
        c_assign_device = request.POST['Assign_Device']

        document_directory_name = os.path.join(os.getcwd(), 'media', 'Captain', 'documents')
        image_directory_name = os.path.join(os.getcwd(), 'media', 'Captain', 'licenseimages')
        vehicle_directory_name = os.path.join(os.getcwd(), 'media', 'Captain', 'vehicleimages')
        rc_book_directory_name = os.path.join(os.getcwd(), 'media', 'Captain', 'rcbookimages')

        for directory in [document_directory_name, image_directory_name, vehicle_directory_name,
                          rc_book_directory_name]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        if c_documents:
            for image in c_documents:
                file_path = os.path.join(document_directory_name, image.name)
                with open(file_path, "wb") as f:
                    f.write(image.file.read())

        if vi_vehicle_image:
            print('---->', vi_vehicle_number)
            for image in vi_vehicle_image:
                file_path = os.path.join(vehicle_directory_name, image.name)
                with open(file_path, "wb") as f:
                    f.write(image.file.read())

        if vi_rc_book_image:
            print('------>', vi_rc_book_image)
            for image in vi_rc_book_image:
                file_path = os.path.join(rc_book_directory_name, image.name)
                with open(file_path, "wb") as f:
                    f.write(image.file.read())

        if c_license_image:
            for image in c_license_image:
                file_path = os.path.join(image_directory_name, image.name)
                with open(file_path, "wb") as f:
                    f.write(image.file.read())

        url_path = request.META['HTTP_HOST']
        document_urls = ['http://' + url_path + '/media/Captain/documents/' + image.name.replace(' ', '') for image in
                         c_documents]
        image_url = [
            'http://' + url_path + '/media/Captain/licenseimages/' + image.name.replace(' ', '').replace('(',
                                                                                                         '').replace(
                ')',
                '')
            for image in c_license_image]

        vehicle_url = [
            'http://' + url_path + '/media/Captain/vehicleimages/' + image.name.replace(' ', '').replace('(',
                                                                                                         '').replace(
                ')',
                '')
            for image in vi_vehicle_image]

        rc_book_url = [
            'http://' + url_path + 'media/Captain/rcbookimages/' + image.name.replace(' ', '').replace('(',
                                                                                                       '').replace(')',
                                                                                                                   '')
            for image in vi_rc_book_image]

        state = State.objects.get(state_name=state)
        city = City.objects.get(city_name=city)
        user = User.objects.get(username=request.user)
        user_details = UserDetails.objects.get(user=user)
        assign_device = AssignDevice.objects.get(ad_id=c_assign_device)

        vehicle_data = VehicleLicenseInformation.objects.create(
            vi_vehicle_no=vi_vehicle_number,
            vi_vehicle_image=vehicle_url,
            vi_rc_book_image=rc_book_url,
            created_by=user_details
        )

        Captain.objects.create(
            user=user,
            c_name=c_name,
            c_email=c_email,
            c_contact_no=c_contact_no,
            c_address=c_address,
            state=state,
            city=city,
            c_documents=document_urls,
            c_license_no=license_number,
            c_license_image=image_url,
            VehicleLicense_Information=vehicle_data,
            Assign_Device=assign_device,
            created_by=user_details,
        )

        assign_device.ad_assign_status = 'Assign'
        assign_device.save()

        return redirect('admin:p_app_captain_changelist')

    return render(request, 'admin/custom_captain_form.html',
                  {'state': state, 'city': city, 'device': device})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_captain_change(request, pk):
    state = State.objects.all()
    city = City.objects.all()
    captains = Captain.objects.get(captain_id=pk)
    device = AssignDevice.objects.filter(ad_assign_status='Pending')
    print('------->', captains.VehicleLicense_Information)
    vehicle = VehicleLicenseInformation.objects.get(vi_id=captains.VehicleLicense_Information.vi_id)

    if request.method == 'POST':
        c_name = request.POST.get('c_name', '')
        c_email = request.POST.get('c_email', '')
        c_contact_no = request.POST.get('c_contact_no', '')
        c_address = request.POST.get('c_address', '')
        state = request.POST.get('state', '')
        city = request.POST.get('city', '')
        c_documents = request.FILES.getlist('c_documents', '')
        c_license_number = request.POST.get('c_license_no', '')
        c_license_image = request.FILES.getlist('c_license_image', '')
        vi_vehicle_number = request.POST.get('vi_vehicle_no', '')
        vi_vehicle_image = request.FILES.getlist('vi_vehicle_image', '')
        vi_rc_book_image = request.FILES.getlist('vi_rc_book_image', '')
        c_assign_device = request.POST.get('Assign_Device', '')

        document_directory_name = os.path.join(os.getcwd(), 'media', 'Captain', 'documents')
        image_directory_name = os.path.join(os.getcwd(), 'media', 'Captain', 'licenseimages')
        vehicle_directory_name = os.path.join(os.getcwd(), 'media', 'Captain', 'vehicleimages')
        rc_book_directory_name = os.path.join(os.getcwd(), 'media', 'Captain', 'rcbookimages')

        for directory in [document_directory_name, image_directory_name, vehicle_directory_name,
                          rc_book_directory_name]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        if c_documents:
            for image in c_documents:
                file_path = os.path.join(document_directory_name, image.name)
                with open(file_path, "wb") as f:
                    f.write(image.file.read())

        if vi_vehicle_image:
            print('---->', vi_vehicle_number)
            for image in vi_vehicle_image:
                file_path = os.path.join(vehicle_directory_name, image.name)
                with open(file_path, "wb") as f:
                    f.write(image.file.read())

        if vi_rc_book_image:
            print('------>', vi_rc_book_image)
            for image in vi_rc_book_image:
                file_path = os.path.join(rc_book_directory_name, image.name)
                with open(file_path, "wb") as f:
                    f.write(image.file.read())

        if c_license_image:
            for image in c_license_image:
                file_path = os.path.join(image_directory_name, image.name)
                with open(file_path, "wb") as f:
                    f.write(image.file.read())

        url_path = request.META['HTTP_HOST']

        if c_name != '':
            captains.c_name = c_name

        if c_email != '':
            captains.c_email = c_email

        if c_contact_no != '':
            captains.c_contact_no = c_contact_no

        if c_address != '':
            captains.c_address = c_address

        if state != '':
            print('---->', state)
            state = State.objects.get(state_id=state)
            captains.state = state

        if city != '':
            city = City.objects.get(city_id=city)
            captains.city = city

        if c_documents != '':
            document_urls = ['http://' + url_path + '/media/Captain/documents/' + image.name.replace(' ', '') for image
                             in
                             c_documents]
            captains.c_documents = document_urls

        if c_license_number != '':
            captains.c_license_number = c_license_number

        if c_license_number != '':
            image_url = [
                'http://' + url_path + '/media/Captain/licenseimages/' + image.name.replace(' ', '').replace('(',
                                                                                                             '').replace(
                    ')', '')
                for image in c_license_image]
            captains.c_license_image = image_url

        if vi_vehicle_number != '':
            vehicle.vi_vehicle_no = vi_vehicle_number

        if vi_vehicle_image != '':
            vehicle_url = [
                'http://' + url_path + '/media/Captain/vehicleimage/' + image.name.replace(' ', '').replace('(',
                                                                                                            '').replace(
                    ')', '')
                for image in vi_vehicle_image]
            vehicle.vi_vehicle_image = vehicle_url

        if vi_rc_book_image != '':
            rc_book_url = [
                'http://' + url_path + 'media/Captain/rcbookimage/' + image.name.replace(' ', '').replace('(',
                                                                                                          '').replace(
                    ')', '')
                for image in vi_rc_book_image]
            vehicle.vo_rc_book_image = rc_book_url

        if c_assign_device != '':
            print('-=-=-=-=-', c_assign_device)
            device = AssignDevice.objects.get(ad_id=c_assign_device)
            captains.Assign_Device = device

        captains.save()
        vehicle.save()
        return redirect('admin:p_app_captain_changelist')
    print('--', device)
    return render(request, 'admin/custom_captain_form.html',
                  {'captains': captains, 'state': state, 'city': city, 'device': device, 'vehicle': vehicle})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def close_captain(request):
    return redirect('admin:p_app_captain_changelist')


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_campaign_create(request):
    client = Client.objects.all()
    if request.method == 'POST':
        id_cm_client = request.POST['client']
        id_cm_geo_fencing = request.POST['cm_geo_fencing']
        id_cm_ad_video_file = request.FILES.getlist('cm_ad_video_file')
        id_cm_no_of_repetition = request.POST['cm_no_of_repetition']
        id_cm_start_date = request.POST['cm_start_date']
        id_cm_tenure = request.POST['cm_tenure']
        id_cm_amount = request.POST['cm_amount']

        print('------------>', id_cm_ad_video_file)

        document_directory_name = os.path.join(os.getcwd(), 'media', 'campaign', 'adsvideo')
        if not os.path.exists(document_directory_name):
            os.makedirs(document_directory_name)

        if id_cm_ad_video_file:
            for image in id_cm_ad_video_file:
                file_path = os.path.join(document_directory_name, image.name)
                with open(file_path, "wb") as f:
                    f.write(image.file.read())

        url_path = request.META['HTTP_HOST']
        ads_urls = ['http://' + url_path + '/media/campaign/adsvideo/' + image.name.replace(' ', '') for image in
                    id_cm_ad_video_file]
        print('-----', ads_urls)

        from datetime import datetime, timedelta

        start_date = datetime.strptime(id_cm_start_date, "%Y-%m-%d")
        end_date = start_date + timedelta(days=int(id_cm_tenure))

        client_data = Client.objects.get(client_id=id_cm_client)
        user = User.objects.get(username=request.user)
        user_details = UserDetails.objects.get(user=user)
        Campaign.objects.create(
            client=client_data,
            cm_geo_fencing=id_cm_geo_fencing,
            cm_ad_video_file=ads_urls,
            cm_no_of_repetition=id_cm_no_of_repetition,
            cm_start_date=id_cm_start_date,
            cm_tenure=id_cm_tenure,
            cm_end_date=end_date,
            cm_amount=id_cm_amount,
            cm_status='Pending',
            created_by=user_details,
        )
        return redirect('admin:p_app_campaign_changelist')  # Redirect to the list of captains in the admin
    return render(request, 'admin/custom_campaign_from.html', {'client': client})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_campaign_change(request, pk):
    client = Client.objects.all()
    campaign = Campaign.objects.get(campaign_id=pk)
    print('------->', campaign.cm_no_of_repetition)
    formatted_date = campaign.cm_start_date.strftime('%Y-%m-%d') if campaign.cm_start_date else ''

    if request.method == 'POST':
        id_cm_client = request.POST.get('cm_client', '')
        id_cm_geo_fencing = request.POST.get('cm_geo_fencing', '')
        id_cm_ad_video_file = request.FILES.getlist('cm_ad_video_file', '')
        id_cm_no_of_repetition = request.POST.get('cm_no_of_repetition', '')
        id_cm_start_date = request.POST.get('cm_start_date', '')
        id_cm_tenure = request.POST.get('cm_tenure', '')
        id_cm_amount = request.POST.get('cm_amount', '')

        document_directory_name = os.path.join(os.getcwd(), 'media', 'campaign', 'adsvideo')
        if not os.path.exists(document_directory_name):
            os.makedirs(document_directory_name)

        ads_urls = []
        for image in id_cm_ad_video_file:
            file_path = os.path.join(document_directory_name, image.name)
            with open(file_path, "wb") as f:
                f.write(image.read())
            url_path = request.META['HTTP_HOST']
            ads_urls.append('http://' + url_path + '/media/campaign/adsvideo/' + image.name.replace(' ', ''))

        if id_cm_start_date:
            start_date = datetime.strptime(id_cm_start_date, "%Y-%m-%d")
            end_date = start_date + timedelta(days=int(id_cm_tenure))
            campaign.cm_start_date = start_date
            campaign.cm_end_date = end_date

        if id_cm_client:
            client_data = Client.objects.get(cl_id=id_cm_client)
            campaign.cm_client = client_data

        if id_cm_geo_fencing:
            campaign.cm_geo_fencing = id_cm_geo_fencing

        if ads_urls:
            campaign.cm_ad_video_file = ads_urls

        if id_cm_no_of_repetition:
            campaign.cm_no_of_repetition = id_cm_no_of_repetition

        if id_cm_tenure:
            campaign.cm_tenure = id_cm_tenure

        if id_cm_amount:
            campaign.cm_amount = id_cm_amount

        campaign.save()

        return redirect('admin:p_app_campaign_changelist')
    print('campaign', campaign.cm_no_of_repetition)
    return render(request, 'admin/custom_campaign_from.html',
                  {'client': client, 'cm_start_date': formatted_date, 'campaign': campaign})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def close_campaign(request):
    return redirect('admin:p_app_campaign_changelist')


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_client_create(request):
    state = State.objects.all()
    city = City.objects.all()
    if request.method == 'POST':
        name = request.POST['cl_contact_person_name']
        email = request.POST['cl_email']
        contact_number = request.POST['cl_contact_no']
        second_contact_number = request.POST['cl_secondary_contact_no']
        address = request.POST['cl_address']
        gst_number = request.POST['cl_gst_no']
        firm_name = request.POST['cl_firm_name']
        firm_address = request.POST['cl_firm_address']
        firm_state = request.POST['state']
        firm_city = request.POST['city']

        state = State.objects.get(state_id=firm_state)
        city = City.objects.get(city_id=firm_city)
        user = User.objects.get(username=request.user)
        user_details = UserDetails.objects.get(user=user)

        Client.objects.create(
            cl_contact_person_name=name,
            cl_email=email,
            cl_contact_no=contact_number,
            cl_secondary_contact_no=second_contact_number,
            cl_address=address,
            cl_gst_no=gst_number,
            cl_firm_name=firm_name,
            cl_firm_address=firm_address,
            state=state,
            city=city,
            created_by=user_details
        )
        return redirect('admin:p_app_client_changelist')
    return render(request, 'admin/custom_client_form.html', {'state': state, 'city': city})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_client_change(request, pk):
    client = Client.objects.get(client_id=pk)
    state = State.objects.all()
    city = City.objects.all()

    if request.method == 'POST':
        name = request.POST.get('cl_contact_person_name', '')
        email = request.POST.get('cl_email', '')
        contact_number = request.POST.get('cl_contact_no', '')
        second_contact_number = request.POST.get('cl_secondary_contact_no', '')
        address = request.POST.get('cl_address', '')
        gst_number = request.POST.get('cl_gst_no', '')
        firm_name = request.POST.get('cl_firm_name', '')
        firm_address = request.POST.get('cl_firm_address', '')
        firm_state = request.POST.get('state', '')
        firm_city = request.POST.get('city', '')

        if name != '':
            client.cl_contact_person_name = name

        if email != '':
            client.cl_email = email

        if contact_number != '':
            client.cl_contact_no = contact_number

        if second_contact_number != '':
            client.cl_secondary_contact_no = second_contact_number

        if address != '':
            client.cl_address = address

        if gst_number != '':
            client.cl_gst_no = gst_number

        if firm_name != '':
            client.cl_firm_name = firm_name

        if firm_address != '':
            client.cl_firm_address = firm_address

        if firm_state != '':
            print('----------', firm_state)
            firm_state = State.objects.get(state_id=firm_state)
            client.state = firm_state

        if firm_city != '':
            firm_city = City.objects.get(city_id=firm_city)
            client.city = firm_city

        client.save()
        return redirect('admin:p_app_client_changelist')
    return render(request, 'admin/custom_client_form.html', {'client': client, 'state': state, 'city': city})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def close_client(request):
    return redirect('admin:p_app_client_changelist')


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_assign_device_create(request):
    if request.method == 'POST':
        ad_brand_name = request.POST['ad_brand_name']
        ad_model_no = request.POST['ad_model_no']
        ad_mac_address = request.POST['ad_mac_address']

        user = User.objects.get(username=request.user)
        user_details = UserDetails.objects.get(user=user)

        AssignDevice.objects.create(
            ad_brand_name=ad_brand_name,
            ad_model_no=ad_model_no,
            ad_mac_address=ad_mac_address,
            ad_device_status='Deactivate',
            ad_assign_status='Pending',
            created_by=user_details,
        )
        return redirect('admin:p_app_assigndevice_changelist')
    return render(request, 'admin/custom_assign_device_form.html')


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_assign_device_change(request, pk):
    captain = Captain.objects.all()
    device = AssignDevice.objects.get(ad_id=pk)
    if request.method == 'POST':
        ad_captain = request.POST.get('ad_captain', '')
        ad_brand_name = request.POST.get('ad_brand_name', '')
        ad_model_no = request.POST.get('ad_model_no', '')
        ad_mac_address = request.POST.get('ad_mac_address', '')
        ad_device_status = request.POST.get('ad_device_status', '')
        ad_assign_status = request.POST.get('ad_assign_status', '')

        print('--->', ad_captain, ad_brand_name, ad_model_no, ad_mac_address, ad_device_status, ad_assign_status)

        if ad_captain != '':
            captain = Captain.objects.get(c_id=ad_captain)
            device.ad_captain = captain

        if ad_brand_name != '':
            device.ad_brand_name = ad_brand_name

        if ad_model_no != '':
            device.ad_model_no = ad_model_no

        if ad_mac_address != '':
            device.ad_mac_address = ad_mac_address

        if ad_device_status != '':
            device.ad_device_status = ad_device_status

        if ad_assign_status != '':
            device.ad_assign_status = ad_assign_status

        device.save()
        return redirect('admin:p_app_assigndevice_changelist')
    return render(request, 'admin/custom_assign_device_form.html', {'captain': captain, 'device': device})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_city_create(request):
    state = State.objects.all()
    if request.method == 'POST':
        state = request.POST['state']
        city_name = request.POST['city_name']
        state_data = State.objects.get(state_id=state)
        user = User.objects.get(username=request.user)
        user_details = UserDetails.objects.get(user=user)

        City.objects.create(
            state=state_data,
            city_name=city_name,
            created_by=user_details,
        )
        return redirect('admin:p_app_city_changelist')

    return render(request, 'admin/custom_city_form.html', {'state': state})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_city_change(request, pk):
    state = State.objects.all()
    city = City.objects.get(city_id=pk)

    if request.method == 'POST':
        state = request.POST.get('state', '')
        city_name = request.POST.get('city_name', '')
        state_data = State.objects.get(state_id=state)

        if state != '':
            city.state = state_data

        if city_name != '':
            city.city_name = city_name

        city.save()

        return redirect('admin:p_app_city_changelist')

    return render(request, 'admin/custom_city_form.html', {'city': city, 'state': state})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def close_city(request):
    return redirect('admin:p_app_city_changelist')


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_state_create(request):
    country = Country.objects.all()

    if request.method == 'POST':
        country = request.POST['country']
        state_name = request.POST['state_name']
        country = Country.objects.get(country_id=country)
        user = User.objects.get(username=request.user)
        user_details = UserDetails.objects.get(user=user)

        State.objects.create(
            country=country,
            state_name=state_name,
            created_by=user_details
        )
        return redirect('admin:p_app_state_changelist')
    return render(request, 'admin/custom_state_form.html', {'country': country})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_state_change(request, pk):
    country = Country.objects.all()
    state = State.objects.get(state_id=pk)

    if request.method == 'POST':
        country = request.POST.get('country', '')
        state_name = request.POST.get('state_name', '')

        country = Country.objects.get(country_id=country)
        if country != '':
            state.country = country

        if state_name != '':
            state.state_name = state_name

        state.save()

        return redirect('admin:p_app_state_changelist')

    return render(request, 'admin/custom_state_form.html', {'state': state, 'country': country})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def close_state(request):
    return redirect('admin:p_app_state_changelist')


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_vehicle_license_information_create(request):
    if request.method == 'POST':
        vi_vehicle_no = request.POST['vi_vehicle_no']
        vi_vehicle_image = request.FILES.getlist('vi_vehicle_image')
        vi_rc_book_image = request.FILES.getlist('vi_rc_book_image')

        print('-------------', vi_vehicle_no)
        print('-------------', vi_vehicle_image)
        print('-------------', vi_rc_book_image)

        vehicle_image_directory_name = os.path.join(os.getcwd(), 'media', 'captain', 'vehicleimage')
        rc_book_image_directory_name = os.path.join(os.getcwd(), 'media', 'captain', 'rcbookimage')
        if not os.path.exists(vehicle_image_directory_name):
            os.makedirs(vehicle_image_directory_name)

        if not os.path.exists(rc_book_image_directory_name):
            os.makedirs(rc_book_image_directory_name)

        if vi_vehicle_image:
            for image in vi_vehicle_image:
                file_path = os.path.join(vehicle_image_directory_name, image.name.replace(' ', ''))
                with open(file_path, "wb") as f:
                    f.write(image.file.read())

        if vi_rc_book_image:
            for image in vi_rc_book_image:
                file_path = os.path.join(rc_book_image_directory_name, image.name.replace(' ', ''))
                with open(file_path, "wb") as f:
                    f.write(image.file.read())

        url_path = request.META['HTTP_HOST']
        vehicle_url = [
            'http://' + url_path + '/media/Captain/vehicleimage/' + image.name.replace(' ', '').replace('(',
                                                                                                        '').replace(
                ')',
                '')
            for image in vi_vehicle_image]

        rc_book_url = [
            'http://' + url_path + '/media/Captain/rcbookimage/' + image.name.replace(' ', '').replace('(',
                                                                                                       '').replace(
                ')',
                '')
            for image in vi_rc_book_image]

        VehicleLicenseInformation.objects.create(
            vi_vehicle_no=vi_vehicle_no,
            vi_vehicle_image=vehicle_url,
            vi_rc_book_image=rc_book_url
        )
        return redirect('admin:p_app_vehiclelicenseinformation_changelist')
    return render(request, 'admin/custom_vehicle_license_information_form.html', )


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_vehicle_license_information_change(request, pk):
    vehicle_data = VehicleLicenseInformation.objects.get(vi_id=pk)
    if request.method == 'POST':
        vi_vehicle_no = request.POST.get('vi_vehicle_no', '')
        vi_vehicle_image = request.FILES.getlist('vi_vehicle_image', '')
        vi_rc_book_image = request.FILES.getlist('vi_rc_book_image', '')
        vehicle_directory_name = os.path.join(os.getcwd(), 'media', 'Captain', 'vehicleimage')
        rc_book_directory_name = os.path.join(os.getcwd(), 'media', 'Captain', 'rcbookimages')
        print('------=>', vi_vehicle_image)
        if vi_vehicle_image:
            for image in vi_vehicle_image:
                print('====>', image)
                file_path = os.path.join(vehicle_directory_name,
                                         image.name.replace(' ', '').replace('(', '').replace(')', ''))
                with open(file_path, "wb") as f:
                    f.write(image.file.read())

        if vi_rc_book_image:
            for image in vi_rc_book_image:
                file_path = os.path.join(rc_book_directory_name,
                                         image.name.replace(' ', '').replace('(', '').replace(')', ''))
                with open(file_path, "wb") as f:
                    f.write(image.file.read())

        url_path = request.META['HTTP_HOST']
        vehicle_url = [
            'http://' + url_path + '/media/Captain/vehicleimage/' + image.name.replace(' ', '').replace('(',
                                                                                                        '').replace(
                ')',
                '')
            for image in vi_vehicle_image]

        rc_book_url = [
            'http://' + url_path + '/media/Captain/rcbookimages/' + image.name.replace(' ', '').replace('(',
                                                                                                        '').replace(
                ')',
                '')
            for image in vi_rc_book_image]

        if vi_vehicle_no != '':
            vehicle_data.vi_vehicle_no = vi_vehicle_no

        if vi_vehicle_image != '':
            vehicle_data.vi_vehicle_image = vehicle_url

        if vi_rc_book_image != '':
            vehicle_data.vi_rc_book_image = rc_book_url

        vehicle_data.save()

        return redirect('admin:p_app_vehiclelicenseinformation_changelist')

    else:
        return render(request, 'admin/custom_vehicle_license_information_form.html', {'vehicle_data': vehicle_data})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def close_vehiclelicenseinformation(request):
    return redirect('admin:p_app_vehiclelicenseinformation_changelist')


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def close_assign_device(request):
    return redirect('admin:p_app_assigndevice_changelist')


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_country_create(request):
    if request.method == 'POST':
        country_name = request.POST['country_name']
        user = User.objects.get(username=request.user)
        user_details = UserDetails.objects.get(user=user)
        Country.objects.create(
            country_name=country_name,
            created_by=user_details
        )
        return redirect('admin:p_app_country_changelist')

    return render(request, 'admin/custom_country_form.html')


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def custom_country_change(request, pk):
    country = Country.objects.get(country_id=pk)
    if request.method == 'POST':
        country_name = request.POST.get('country_name', '')

        if country_name != '':
            country.country_name = country_name

        country.save()
        return redirect('admin:p_app_country_changelist')
    return render(request, 'admin/custom_country_form.html', {'country': country})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def close_country(request):
    return redirect('admin:p_app_country_changelist')


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def setting(request):
    return render(request, 'volt/pages/settings.html')
