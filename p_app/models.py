import uuid
import pyotp
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from typing import Optional
import qrcode
import qrcode.image.svg


class CampaignStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    RUNNING = 'Running', 'Running'
    COMPLETED = 'Completed', 'Completed'


class DeviceStatus(models.TextChoices):
    ACTIVATE = 'Activate', 'Activate'
    DEACTIVATE = 'Deactivate', 'Deactivate'


class TwoFactorData(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='two_factor_auth_data',
        on_delete=models.CASCADE
    )
    otp_secret = models.CharField(max_length=255, verbose_name='OTP Secret')
    session_identifier = models.UUIDField(blank=True, null=True, verbose_name='Session Identifier')

    def generate_qr_code(self, name: Optional[str] = None, username: Optional[str] = None) -> str:
        totp = pyotp.TOTP(self.otp_secret)
        qr_uri = totp.provisioning_uri(name=name, issuer_name=username)
        image_factory = qrcode.image.svg.SvgPathImage
        qr_code_image = qrcode.make(qr_uri, image_factory=image_factory)
        return qr_code_image.to_string().decode('utf_8')

    def validate_otp(self, otp: str) -> bool:
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(otp)

    def rotate_session_identifier(self):
        self.session_identifier = uuid.uuid4()
        self.save(update_fields=["session_identifier"])

    def regenerate_otp_secret(self):
        self.otp_secret = pyotp.random_base32()
        self.rotate_session_identifier()
        self.save(update_fields=["otp_secret", "session_identifier"])


class UserDetails(models.Model):
    ud_id = models.AutoField(primary_key=True, verbose_name='Id')
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    contact_no = models.CharField(max_length=15, verbose_name='Contact Number')  # Changed to field
    address = models.CharField(max_length=200, verbose_name='Address')

    class Meta:
        verbose_name_plural = 'User Details'


class Country(models.Model):
    country_id = models.AutoField(primary_key=True, verbose_name='Id')
    country_name = models.CharField(max_length=50, verbose_name='Name')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, verbose_name='Created By',
                                   db_column='created_by',
                                   null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Country'
        unique_together = ['country_name']

    def __str__(self):
        return self.country_name


class State(models.Model):
    state_id = models.AutoField(primary_key=True, verbose_name='Id')
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='Country')
    state_name = models.CharField(max_length=50, verbose_name='Name')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, verbose_name='Created By',
                                   db_column='created_by',
                                   null=True, blank=True)

    class Meta:
        verbose_name_plural = 'State'
        constraints = [
            models.UniqueConstraint(fields=['country', 'state_name'], name='unique_state_name')
        ]

    def __str__(self):
        return self.state_name


class City(models.Model):
    city_id = models.AutoField(primary_key=True, verbose_name='Id')
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name='State')
    city_name = models.CharField(max_length=50, verbose_name='Name')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, verbose_name='Created By',
                                   db_column='created_by',
                                   null=True, blank=True)

    class Meta:
        verbose_name_plural = 'City'
        constraints = [
            models.UniqueConstraint(fields=['state', 'city_name'], name='unique_city_name')
        ]

    def __str__(self):
        return self.city_name


class VehicleLicenseInformation(models.Model):
    vi_id = models.AutoField(primary_key=True, verbose_name='Id')
    vi_vehicle_no = models.CharField(max_length=50, verbose_name='Vehicle Number')
    vi_vehicle_image = models.JSONField(verbose_name='Vehicle Image')
    vi_rc_book_image = models.JSONField(verbose_name='RC Book Image')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, verbose_name='Created By',
                                   db_column='created_by',
                                   null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Vehicle License Information'


class AssignDevice(models.Model):
    ad_id = models.AutoField(primary_key=True, verbose_name='Id')
    ad_brand_name = models.CharField(max_length=50, verbose_name='Brand Name')
    ad_model_no = models.CharField(max_length=20, verbose_name='Model Number')
    ad_mac_address = models.CharField(max_length=50, verbose_name='Mac Address')
    ad_device_status = models.CharField(max_length=50, choices=DeviceStatus.choices, verbose_name='Device Status')
    ad_assign_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Assign', 'Assign')],
                                        null=True, default='Pending', verbose_name='ASSIGN STATUS')
    ad_created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, verbose_name='Created By',
                                   db_column='created_by',
                                   null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Assign Device'
        constraints = [
            models.UniqueConstraint(fields=['ad_brand_name', 'ad_model_no', 'ad_mac_address'], name='unique_device')
        ]


class Captain(models.Model):
    captain_id = models.AutoField(primary_key=True, verbose_name='Id')  # change field name
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='user', null=True, blank=True)  # New Add
    c_name = models.CharField(max_length=100, verbose_name='Name')
    c_email = models.EmailField(unique=True, verbose_name='Email')
    c_contact_no = models.CharField(max_length=15, verbose_name='Contact Number')  # Changed to field
    c_address = models.CharField(max_length=100, verbose_name='Address')
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name='State')  # change field name
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='City')  # change field name
    c_documents = models.JSONField(verbose_name='Documents', null=True, default=dict)
    c_license_no = models.CharField(max_length=50, verbose_name='License Number')
    c_license_image = models.JSONField(verbose_name='License Image')
    VehicleLicense_Information = models.ForeignKey(VehicleLicenseInformation, on_delete=models.PROTECT,
                                                   verbose_name='VEHICLE LICENSE', null=True)
    Assign_Device = models.ForeignKey(AssignDevice, on_delete=models.PROTECT, verbose_name='ASSIGN DEVICE', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, verbose_name='Created By',
                                   db_column='created_by',
                                   null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Captain'

    def __str__(self):
        return self.c_name


class Client(models.Model):
    client_id = models.AutoField(primary_key=True, verbose_name='Id')
    cl_contact_person_name = models.CharField(max_length=100, verbose_name='Name')
    cl_email = models.EmailField(unique=True, verbose_name='Email')
    cl_contact_no = models.CharField(max_length=15, verbose_name='Contact Number')  # Changed to field
    cl_secondary_contact_no = models.CharField(max_length=15, verbose_name='Secondary Contact Number', null=True,
                                               blank=True)  # Changed to field
    cl_address = models.CharField(max_length=200, verbose_name='Address')
    cl_gst_no = models.CharField(max_length=50, verbose_name='GST Number')
    cl_firm_name = models.CharField(max_length=100, verbose_name='Firm Name')
    cl_firm_address = models.CharField(max_length=200, verbose_name='Firm Address')
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name='State')
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='City')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, verbose_name='Created By',
                                   db_column='created_by',
                                   null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Client'
        constraints = [
            models.UniqueConstraint(fields=['cl_gst_no'], name='unique_gst_no')
        ]

    def __str__(self):
        return self.cl_contact_person_name


class Campaign(models.Model):
    campaign_id = models.AutoField(primary_key=True, verbose_name='Id')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Client')
    cm_geo_fencing = models.TextField(verbose_name='Geo Fencing')
    cm_ad_video_file = models.JSONField(verbose_name='Ad Video File')
    cm_no_of_repetition = models.IntegerField(verbose_name='No of repetition')
    cm_start_date = models.DateField(verbose_name='Start Date')
    cm_tenure = models.IntegerField(verbose_name='Tenure')
    cm_end_date = models.DateField(verbose_name='End Date', editable=False)
    cm_amount = models.IntegerField(verbose_name='Amount')
    cm_status = models.CharField(max_length=50, choices=CampaignStatus.choices, verbose_name='Status', editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, verbose_name='Created By',
                                   db_column='created_by',
                                   null=True, blank=True, editable=False)

    class Meta:
        verbose_name_plural = 'Campaign'

    def __str__(self):
        return f"Campaign {self.campaign_id} for {self.client}"


class Area(models.Model):
    area_id = models.AutoField(primary_key=True, verbose_name='Id')
    name = models.CharField(max_length=100, verbose_name='Name')
    latitude = models.FloatField(verbose_name='Latitude')
    longitude = models.FloatField(verbose_name='Longitude')
    radius = models.IntegerField(verbose_name='Radius')
    created_at = models.DateTimeField(auto_created=True, verbose_name='Created At')
    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, db_column='created_by',
                                   verbose_name='Created By')

    class Meta:
        verbose_name_plural = 'Area'


class EarnPoint(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Id')
    captain = models.ForeignKey(Captain, on_delete=models.PROTECT, verbose_name='Captain', null=True, blank=True)
    points = models.IntegerField(verbose_name='Points')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name='Updated At')

    class Meta:
        verbose_name_plural = 'Earn Points'

    def __str__(self):
        return f'{self.captain.c_name} - {self.points} points'


class CaptainTripStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    RUNNING = 'Running', 'Running'
    CLOSE = 'Close', 'Close'


class CaptainTrip(models.Model):
    id = models.AutoField(primary_key=True)
    captain = models.ForeignKey('Captain', on_delete=models.CASCADE, verbose_name='Captain')
    check_in = models.DateTimeField(auto_now_add=True, verbose_name='Check In')
    check_out = models.DateTimeField(null=True, blank=True, verbose_name='Check Out')
    total_hours = models.DurationField(null=True, blank=True, verbose_name='Total Hours')
    status = models.CharField(max_length=10, choices=CaptainTripStatus.choices, default=CaptainTripStatus.PENDING,
                              verbose_name='Status')

    class Meta:
        verbose_name_plural = 'Captain Trips'

    def __str__(self):
        return f"{self.captain.c_name} - {self.status}"


class VideoView(models.Model):
    captain = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Captain')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, verbose_name='Campaign')
    video_url = models.URLField(verbose_name='Video URL')
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name='Viewed At')

    class Meta:
        verbose_name_plural = 'Video Views'

    def __str__(self):
        return f"View by {self.captain} on {self.viewed_at}"
