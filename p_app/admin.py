from django.contrib import admin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.urls import path, reverse
from django.utils.html import format_html
from .views import *
from super_admin.views import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


def view_qrcode(obj):
    view_url = reverse('view_qrcode', args=[obj.pk])

    return format_html("""
        <a class="button" href="{}" onclick="openModal('{}'); return false;">View</a>
        <div id="qrModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal()">&times;</span>
                <div id="qrCodeContainer"></div>
            </div>
        </div>
        <style>
            .modal {{
                display: none; 
                position: fixed; 
                z-index: 1; 
                left: 0;
                top: 0;
                width: 100%; 
                height: 100%; 
                overflow: auto; 
                background-color: rgba(0, 0, 0, 0.4); 
            }}
            .modal-content {{
                background-color: #fefefe;
                margin-left:45%;
                margin-top: 15%; 
                padding: 20px;
                border: 1px solid #888;
                width: 300px; /* Adjust the width */
                height: 300px; /* Adjust the height */
                position: relative;
                text-align: center;
            }}
            .close {{
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
                position: absolute;
                right: 10px;
                top: 5px;
            }}
            .close:hover,
            .close:focus {{
                color: black;
                text-decoration: none;
                cursor: pointer;
            }}
        </style>
        <script>
            function openModal(url) {{
                fetch(url)
                .then(response => response.json())
                .then(data => {{
                    const qrCodeContainer = document.getElementById("qrCodeContainer");
                    qrCodeContainer.innerHTML = '<div class="username">' + data.username + '</div>' +
                                                '<img src="data:image/png;base64,' + data.qr_code + '" alt="QR Code">';
                    document.getElementById("qrModal").style.display = "block";
                }});
            }}
            function closeModal() {{
                document.getElementById("qrModal").style.display = "none";
                document.getElementById("qrCodeContainer").innerHTML = "";
            }}
            window.onclick = function(event) {{
                if (event.target == document.getElementById("qrModal")) {{
                    closeModal();
                }}
            }}
        </script>
    """, view_url, view_url)


def regenerate_qr_code(obj):
    regenerate_url = reverse('regenerate_qr_code', args=[obj.pk])
    return format_html('<a class="button" href="{}">Regenerate</a>', regenerate_url)


view_qrcode.short_description = 'View Qrcode'
regenerate_qr_code.short_description = 'Regenerate QRCode'

first_otp = ''
second_otp = ''


def process_otp_secrets(first_otp_secret, second_otp_secret):
    global first_otp, second_otp
    print('first otp', first_otp, 'second otp', second_otp)
    print('first otp secret', first_otp_secret, 'second otp secret', second_otp_secret)

    if first_otp != first_otp_secret and second_otp != second_otp_secret:
        first_otp = first_otp_secret
        second_otp = second_otp_secret
    else:
        first_otp = ''
        second_otp = ''

    return True


class MyAdminSite(admin.AdminSite):
    site_header = 'My Custom Admin'
    site_title = 'Admin'
    index_title = 'My Models'

    def get_urls(self):
        base_urlpatterns = super().get_urls()
        extra_urlpatterns = [
            path('setup-2fa/', self.admin_view(AdminSetupTwoFactorAuthView.as_view()), name='setup-2fa'),
            path('confirm-2fa/', self.admin_view(AdminConfirmTwoFactorAuthView.as_view()), name='confirm-2fa'),
            path('regenerate_qr_code/<int:user_id>/', self.admin_view(regenerate_qr_code_view),
                 name='regenerate_qr_code'),
        ]
        return extra_urlpatterns + base_urlpatterns

    def login(self, request, *args, **kwargs):
        if request.method != 'POST':
            return super().login(request, *args, **kwargs)

        username = request.POST.get('username')
        two_factor_auth_data = TwoFactorData.objects.filter(user__username=username).first()
        if not two_factor_auth_data:
            request.POST._mutable = True
            request.POST[REDIRECT_FIELD_NAME] = reverse("admin:setup-2fa")
            request.POST._mutable = False

        elif first_otp and second_otp and (second_otp == two_factor_auth_data.otp_secret):
            request.POST._mutable = True
            request.POST[REDIRECT_FIELD_NAME] = reverse("admin:setup-2fa")
            request.POST._mutable = False

        else:
            request.POST._mutable = True
            request.POST[REDIRECT_FIELD_NAME] = reverse("admin:confirm-2fa")
            request.POST._mutable = False

        return super().login(request, *args, **kwargs)

    login_form = AuthenticationForm

    def has_permission(self, request):
        return request.user.is_active


class CountryAdmin(admin.ModelAdmin):

    def edit_and_delete_button(obj):
        edit_url = reverse('custom_country_change', args=[obj.pk])
        delete_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])

        return format_html("""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            </head>
            <body>
                <a class="button" href="{}"><i class="fas fa-edit"></i></a>&nbsp;&nbsp;
                <a class="button" href="{}"><i class="fas fa-trash-alt"></i></a>
            </body>
            </html>""", edit_url, delete_url)

    edit_and_delete_button.short_description = 'Action'

    list_display = ['country_id', 'country_name', edit_and_delete_button]
    actions = None

    change_form_template = "admin/custom_country_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/', self.admin_site.admin_view(custom_country_create), name='custom_country_create')
        ]
        return custom_urls + urls


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_active', 'is_staff', 'is_superuser', view_qrcode,
                    regenerate_qr_code]
    list_filter = ['is_active', 'is_staff', 'is_superuser']

    def save_model(self, request, obj, form, change):
        if obj.password:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return True


class StateAdmin(admin.ModelAdmin):

    def edit_and_delete_button(obj):
        edit_url = reverse('custom_state_change', args=[obj.pk])
        delete_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])

        return format_html("""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            </head>
            <body>
                <a class="button" href="{}"><i class="fas fa-edit"></i></a>&nbsp;&nbsp;
                <a class="button" href="{}"><i class="fas fa-trash-alt"></i></a>
            </body>
            </html>""", edit_url, delete_url)

    edit_and_delete_button.short_description = 'Action'

    list_display = ['state_id', 'state_name', 'country', edit_and_delete_button]
    actions = None

    change_form_template = "admin/custom_state_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/', self.admin_site.admin_view(custom_state_create), name='custom_state_create')
        ]
        return custom_urls + urls


class CityAdmin(admin.ModelAdmin):

    def edit_and_delete_button(obj):
        edit_url = reverse('custom_city_change', args=[obj.pk])
        delete_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])

        return format_html("""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            </head>
            <body>
                <a class="button" href="{}"><i class="fas fa-edit"></i></a>&nbsp;&nbsp;
                <a class="button" href="{}"><i class="fas fa-trash-alt"></i></a>
            </body>
            </html>""", edit_url, delete_url)

    edit_and_delete_button.short_description = 'Action'

    list_display = ['city_id', 'city_name', 'state', edit_and_delete_button]
    actions = None

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/', self.admin_site.admin_view(custom_city_create), name='custom_city_create'),
        ]
        return custom_urls + urls


class ClientAdmin(admin.ModelAdmin):

    def edit_and_delete_button(obj):
        edit_url = reverse('custom_client_change', args=[obj.pk])
        delete_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])

        return format_html("""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            </head>
            <body>
                <a class="button" href="{}"><i class="fas fa-edit"></i></a>&nbsp;&nbsp;
                <a class="button" href="{}"><i class="fas fa-trash-alt"></i></a>
            </body>
            </html>""", edit_url, delete_url)

    edit_and_delete_button.short_description = 'Action'

    list_display = ['client_id', 'cl_contact_person_name', 'cl_email', 'cl_contact_no',
                    'cl_gst_no', 'cl_firm_name', 'state', 'city', edit_and_delete_button]
    actions = None

    change_form_template = "admin/p_app/client/custom_client_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/', self.admin_site.admin_view(custom_client_create), name='custom_client_create')
        ]
        return custom_urls + urls


class CampaignAdmin(admin.ModelAdmin):

    def edit_and_delete_button(obj):
        edit_url = reverse('custom_campaign_change', args=[obj.pk])
        delete_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])

        return format_html("""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            </head>
            <body>
                <a class="button" href="{}"><i class="fas fa-edit"></i></a>&nbsp;&nbsp;
                <a class="button" href="{}"><i class="fas fa-trash-alt"></i></a>
            </body>
            </html>""", edit_url, delete_url)

    edit_and_delete_button.short_description = 'Action'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['show_map'] = True
        return super(CampaignAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['show_map'] = True
        return super(CampaignAdmin, self).add_view(request, form_url, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/', self.admin_site.admin_view(custom_campaign_create), name='custom_campaign_create'),
        ]
        return custom_urls + urls

    def clean_url(self, url_list):
        if isinstance(url_list, list):
            return [url.strip("[]").strip("'") for url in url_list]
        return [url_list]

    def ad_video_file_tag(self, obj):
        urls = self.clean_url(obj.cm_ad_video_file)
        if urls:
            links = [
                format_html(
                    '<a href="{}" target="_blank"><i class="fas fa-book"></i></a>',
                    url
                )
                for url in urls if url
            ]
            return format_html(' '.join(links))
        return '-'
    ad_video_file_tag.short_description = 'Video File'

    change_form_template = "admin/p_app/campaign/custom_campaign_form.html"

    list_display = ['campaign_id', 'client', 'cm_start_date', 'cm_end_date', 'cm_no_of_repetition', 'cm_status',
                    'cm_amount', 'ad_video_file_tag', edit_and_delete_button]
    actions = None


class CaptainAdmin(admin.ModelAdmin):

    def edit_and_delete_button(obj):
        edit_url = reverse('custom_captain_change', args=[obj.pk])
        delete_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])

        return format_html("""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            </head>
            <body>
                <a class="button" href="{}"><i class="fas fa-edit"></i></a>&nbsp;&nbsp;
                <a class="button" href="{}"><i class="fas fa-trash-alt"></i></a>
            </body>
            </html>""", edit_url, delete_url)

    edit_and_delete_button.short_description = 'Action'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/', self.admin_site.admin_view(custom_captain_create), name='custom_captain_create'),
        ]
        return custom_urls + urls

    def clean_url(self, url_list):
        if isinstance(url_list, list):
            return [url.strip("[]").strip("'") for url in url_list]
        return [url_list]

    def document_tag(self, obj):
        urls = self.clean_url(obj.c_documents)
        if urls:
            links = [
                format_html(
                    '<a href="{}" target="_blank"><i class="fas fa-book"></i></a>',
                    url
                )
                for url in urls if url
            ]
            return format_html(' '.join(links))
        return '-'
    document_tag.short_description = 'DOCUMENT'

    def license_image_tag(self, obj):
        urls = self.clean_url(obj.c_license_image)
        if urls:
            links = [
                format_html(
                    '<a href="{}" target="_blank"><i class="fas fa-book"></i></a>',
                    url
                )
                for url in urls if url
            ]
            return format_html(' '.join(links))
        return '-'
    license_image_tag.short_description = 'LICENSE IMAGE'

    list_display = ['captain_id', 'c_name', 'c_email', 'c_contact_no', 'c_address', 'state', 'city',
                    'c_license_no', 'document_tag', 'license_image_tag', edit_and_delete_button]
    actions = None
    change_form_template = "admin/custom_captain_form.html"


class AssignDeviceAdmin(admin.ModelAdmin):
    def edit_and_delete_button(obj):
        edit_url = reverse('custom_assign_device_change', args=[obj.pk])
        delete_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])

        return format_html("""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            </head>
            <body>
                <a class="button" href="{}"><i class="fas fa-edit"></i></a>&nbsp;&nbsp;
                <a class="button" href="{}"><i class="fas fa-trash-alt"></i></a>
            </body>
            </html>""", edit_url, delete_url)

    edit_and_delete_button.short_description = 'Action'

    list_display = ['ad_id', 'ad_brand_name', 'ad_model_no', 'ad_mac_address', 'ad_device_status', 'ad_assign_status',
                    edit_and_delete_button]
    actions = None

    change_form_template = "admin/custom_assign_device_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/', self.admin_site.admin_view(custom_assign_device_create), name='custom_assign_device_create'),
        ]
        return custom_urls + urls


class VehicleLicenseInformationAdmin(admin.ModelAdmin):

    def edit_and_delete_button(obj):
        edit_url = reverse('custom_vehicle_license_information_change', args=[obj.pk])
        delete_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])

        return format_html(
            """<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            </head>
            <body>
                <a class="button" href="{}"><i class="fas fa-edit"></i></a>&nbsp;&nbsp;
                <a class="button" href="{}"><i class="fas fa-trash-alt"></i></a>
            </body>
            </html>""", edit_url, delete_url )

    edit_and_delete_button.short_description = 'Actions'

    change_form_template = "admin/custom_vehicle_license_information_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/', self.admin_site.admin_view(custom_vehicle_license_information_create),
                 name='custom_vehicle_license_information_create'),
        ]
        return custom_urls + urls

    def clean_url(self, url_list):
        if isinstance(url_list, list):
            return [url.strip("[]").strip("'") for url in url_list]
        return [url_list]

    def vehicle_image_tag(self, obj):
        urls = self.clean_url(obj.vi_vehicle_image)
        if urls:
            links = [
                format_html(
                    '<a href="{}" target="_blank"><i class="fas fa-image"></i></a>',
                    url
                )
                for url in urls if url
            ]
            return format_html(' '.join(links))
        return '-'

    vehicle_image_tag.short_description = 'Vehicle Image'

    def rc_book_image_tag(self, obj):
        urls = self.clean_url(obj.vi_rc_book_image)
        if urls:
            links = [
                format_html(
                    '<a href="{}" target="_blank"><i class="fas fa-book"></i></a>',
                    url
                )
                for url in urls if url
            ]
            return format_html(' '.join(links))
        return '-'

    rc_book_image_tag.short_description = 'RC Book Image'

    list_display = ['vi_id', 'vi_vehicle_no', 'vehicle_image_tag', 'rc_book_image_tag', edit_and_delete_button]
    actions = None


class UserCreationForm(forms.ModelForm):
    contact_no = forms.IntegerField(label='Contact Number')
    address = forms.CharField(label='Address', max_length=200)

    class Meta:
        model = User
        fields = (
            'username', 'password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'first_name',
            'last_name',
            'email', 'is_staff', 'is_active', 'date_joined')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user_details = UserDetails(user=user, contact_no=self.cleaned_data['contact_no'],
                                   address=self.cleaned_data['address'])
        if commit:
            user.save()
            user_details.save()
        return user


class UserDetailsInline(admin.StackedInline):
    model = UserDetails
    can_delete = False
    verbose_name_plural = 'User Details'


class UserAdmin(BaseUserAdmin):
    inlines = [UserDetailsInline]
    list_display = ['id', 'username', 'is_active', 'is_staff', 'is_superuser', view_qrcode, regenerate_qr_code]
    list_filter = []
    actions = None

    add_form = UserCreationForm
    form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'contact_no', 'address', 'last_login', 'is_superuser', 'groups',
                       'user_permissions', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'contact_no', 'address')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_superuser', 'groups', 'user_permissions', 'is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and hasattr(obj, 'userdetails'):
            form.base_fields['contact_no'].initial = obj.userdetails.contact_no
            form.base_fields['address'].initial = obj.userdetails.address
        return form

    def save_model(self, request, obj, form, change):
        if obj.password:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

        if not change:
            UserDetails.objects.create(user=obj, contact_no=form.cleaned_data['contact_no'],
                                       address=form.cleaned_data['address'])
        else:
            obj.userdetails.contact_no = form.cleaned_data['contact_no']
            obj.userdetails.address = form.cleaned_data['address']
            obj.userdetails.save()

    def has_change_permission(self, request, obj=None):
        return True


class AreaAdmin(admin.ModelAdmin):
    change_form_template = "admin/area.html"


admin_site = MyAdminSite(name="myadmin")
admin.site.unregister(User)
admin_site.register(User, UserAdmin)
admin_site.register(Group)
admin_site.register(Country, CountryAdmin)
admin_site.register(State, StateAdmin)
admin_site.register(City, CityAdmin)
admin_site.register(Captain, CaptainAdmin)
admin_site.register(VehicleLicenseInformation, VehicleLicenseInformationAdmin)
admin_site.register(AssignDevice, AssignDeviceAdmin)
admin_site.register(Client, ClientAdmin)
admin_site.register(Campaign, CampaignAdmin)
admin_site.register(VideoView)
admin_site.register(Area, AreaAdmin)
