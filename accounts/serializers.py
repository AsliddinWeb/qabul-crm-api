import re
from django.utils import timezone
import random

from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User, PhoneVerification
from .utils.eskiz import send_sms


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['phone', 'password']

    def validate_phone(self, value):
        # +998 bilan boshlanadigan O'zbek raqami uchun regex
        pattern = r'^\+998\d{9}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Telefon raqami formati noto‘g‘ri. Masalan: +998901234567")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=68, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(phone=obj['phone'])
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        user = auth.authenticate(phone=phone, password=password)

        if not user:
            raise AuthenticationFailed('Login yoki parol noto‘g‘ri.')
        if not user.is_active:
            raise AuthenticationFailed('Foydalanuvchi bloklangan.')
        if not user.is_verified:
            raise AuthenticationFailed('Telefon raqami tasdiqlanmagan.')

        return {
            'phone': user.phone,
            'tokens': self.get_tokens({'phone': user.phone})
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('Token noto‘g‘ri yoki muddati tugagan.')

class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        code = attrs.get('code')

        verification = PhoneVerification.objects.filter(phone=phone).last()

        if not verification:
            raise serializers.ValidationError("Tasdiqlash kodi topilmadi.")
        if verification.code != code:
            raise serializers.ValidationError("Tasdiqlash kodi noto‘g‘ri.")
        if verification.is_expired():
            raise serializers.ValidationError("Tasdiqlash kodi eskirgan.")

        return attrs

    def save(self, **kwargs):
        phone = self.validated_data['phone']
        user = User.objects.get(phone=phone)
        user.is_verified = True
        user.save()
        PhoneVerification.objects.filter(phone=phone).delete()
        self.user = user
        return user

    def to_representation(self, instance):
        return {
            "detail": "Telefon raqami tasdiqlandi!",
            "tokens": self.get_tokens(self.user)
        }

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class ResendVerificationCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        try:
            user = User.objects.get(phone=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Bu telefon raqam ro‘yxatdan o‘tmagan.")
        if user.is_verified:
            raise serializers.ValidationError("Bu raqam allaqachon tasdiqlangan.")
        return value

    def save(self, **kwargs):
        phone = self.validated_data['phone']
        code = str(random.randint(1000, 9999))
        message = f"Xalqaro innovatsion universiteti qabul tizimiga kirish kodingiz: {code}"
        PhoneVerification.objects.update_or_create(phone=phone, defaults={'code': code})
        send_sms(phone=phone.replace("+", ""), message=message)
        return code
    
class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'full_name', 'role', 'is_verified']
