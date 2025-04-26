from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('verify/', views.VerifyCodeView.as_view(), name="verify"),
    path('resend/', views.ResendVerificationCodeView.as_view(), name="resend"),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.MeAPIView.as_view(), name='getMe'),
]
