from django.contrib.admin import apps


class CustomAdminConfig(apps.SimpleAdminConfig):
    default_site = "p_app.sites.AdminSite"
    name = 'p_app'


