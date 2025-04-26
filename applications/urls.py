from django.urls import path
from .views import GetPassportInfoFromGov, ApplicationCreateAPIView

urlpatterns = [
    path('get-passport-info/', GetPassportInfoFromGov.as_view(), name='passport-info-from-gov'),
    path('create/', ApplicationCreateAPIView.as_view(), name='application-create'),
]
