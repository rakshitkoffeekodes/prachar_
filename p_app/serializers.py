from rest_framework import serializers
from .models import *


class UserRegisterSerializer(serializers.ModelSerializer):  # OK
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    contact_no = serializers.IntegerField()
    address = serializers.CharField()

    class Meta:
        model = UserDetails
        fields = ['ud_id', 'username', 'password', 'first_name', 'last_name', 'contact_no', 'address']


class CampaignSerializer(serializers.ModelSerializer):
    video_urls = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = ['campaign_id', 'cm_geo_fencing', 'cm_ad_video_file', 'video_urls']

    def get_video_urls(self, obj):
        return obj.cm_ad_video_file


class VehicleLicenseInformationSerializer(serializers.ModelSerializer):  # OK
    class Meta:
        model = VehicleLicenseInformation
        fields = '__all__'


class AssignDeviceSerializer(serializers.ModelSerializer):  # OK
    class Meta:
        model = AssignDevice
        fields = '__all__'


class CaptaindataSerializer(serializers.ModelSerializer):  # OK
    vehicle_license_info = serializers.SerializerMethodField()
    assign_device = serializers.SerializerMethodField()

    class Meta:
        model = Captain
        fields = '__all__'

    def get_vehicle_license_info(self, obj):
        vehicle_license_info = VehicleLicenseInformation.objects.filter(captain=obj)
        if vehicle_license_info.exists():
            return VehicleLicenseInformationSerializer(vehicle_license_info.first()).data
        return None

    def get_assign_device(self, obj):
        assign_device = AssignDevice.objects.filter(captain=obj)
        if assign_device.exists():
            return AssignDeviceSerializer(assign_device.first()).data
        return None


class EarnPointSerializer(serializers.ModelSerializer):  # OK
    class Meta:
        model = EarnPoint
        fields = '__all__'


class CaptainOTPSerializer(serializers.Serializer):
    c_contact_no = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=4)
