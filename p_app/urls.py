from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )
from .views import *

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # GET REF TOKEN

    path('captain_profile/', get_captain_details),
    path('get_captain_earn_points/', get_captain_earn_points, name='get_captain_earn_points'),
    path('captain_check_in_out_trip/', captain_check_in_out, name='captain_check_in_out'),
    path('get_campaign_data/', get_campaign_data, name='get_campaign_data'),
    path('get_captain_trips_details/', get_captain_trips, name='get_captain_trips'),
    path('verify_contact/', verify_contact, name='verify_contact'),
    path('verify_otp/', verify_otp, name='verify_otp'),

]
