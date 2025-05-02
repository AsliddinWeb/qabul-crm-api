from django.urls import path
from .views import (
    GetPassportInfoFromGov,
    ApplicationCreateAPIView,
    RegionListAPIView,
    DistrictByRegionAPIView,
    PassportInfoRetrieveAPIView,
    PassportInfoCreateAPIView,
    DiplomInfoRetrieveAPIView,
    DiplomInfoCreateAPIView,
    ApplicationListAPIView
)

urlpatterns = [
    path('get-passport-info/', GetPassportInfoFromGov.as_view(), name='passport-info-from-gov'),

    path('', ApplicationListAPIView.as_view(), name='application-list'),
    path('create/', ApplicationCreateAPIView.as_view(), name='application-create'),

    # Passport APIs
    path('regions/', RegionListAPIView.as_view(), name='region-list'),
    path('districts/', DistrictByRegionAPIView.as_view(), name='district-by-region'),
    path('passport/', PassportInfoRetrieveAPIView.as_view(), name='passport-get'),
    path('passport/create/', PassportInfoCreateAPIView.as_view(), name='passport-create'),

    # Diplom APIs
    path('diplom/', DiplomInfoRetrieveAPIView.as_view(), name='diplom-get'),
    path('diplom/create/', DiplomInfoCreateAPIView.as_view(), name='diplom-create'),
]
