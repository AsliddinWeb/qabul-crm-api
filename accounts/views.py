import random
from rest_framework import generics, status, permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, VerifyCodeSerializer, ResendVerificationCodeSerializer, UserMeSerializer
from .models import PhoneVerification

from accounts.utils.eskiz import send_sms

from drf_yasg.utils import swagger_auto_schema


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Ro'yxatdan o'tish",
        operation_description="Yangi foydalanuvchini telefon raqam orqali ro'yxatdan o'tkazadi va tasdiqlash kodini SMS orqali yuboradi.",
        tags=['Auth']
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 4 xonali random tasdiqlash kodi generatsiya qilinadi
        code = str(random.randint(1000, 9999))

        # Eskiz orqali yuboriladigan xabar
        message = f"Xalqaro innovatsion universiteti qabul tizimiga kirish kodingiz: {code}"

        # Eski kodni yangilash yoki yangi yozuv yaratish
        PhoneVerification.objects.create(
            phone=user.phone,
            code=code
        )

        send_sms(phone=user.phone.replace("+", ""), message=message)

        return Response(
            {"detail": "Foydalanuvchi yaratildi. Tasdiqlash kodi yuborildi."},
            status=status.HTTP_201_CREATED
        )

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Kirish",
        operation_description="Telefon raqam va parol orqali login qilish. JWT token qaytaradi.",
        tags=['Auth']
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Chiqish",
        operation_description="Refresh tokenni blacklist qiladi va chiqadi.",
        tags=['Auth']
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VerifyCodeView(generics.GenericAPIView):
    serializer_class = VerifyCodeSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Tasdiqlash kodi orqali kirish",
        operation_description="Tasdiqlash kodi to‘g‘ri bo‘lsa, foydalanuvchini faollashtiradi va JWT tokenlarni qaytaradi.",
        tags=['Auth']
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResendVerificationCodeView(generics.GenericAPIView):
    serializer_class = ResendVerificationCodeSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Kod qayta yuborish",
        operation_description="Tasdiqlash kodi eskirgan bo‘lsa, yangisini yuboradi.",
        tags=['Auth']
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Tasdiqlash kodi qayta yuborildi."}, status=status.HTTP_200_OK)

class MeAPIView(RetrieveAPIView):
    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user