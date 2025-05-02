from rest_framework import generics, permissions
from applications.models import Application
from applications.serializers.application import ApplicationCreateSerializer, ApplicationDetailSerializer
from drf_yasg.utils import swagger_auto_schema

class ApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Foydalanuvchi uchun yangi ariza (passport + diplom) ma’lumotlarini yaratish")
    def perform_create(self, serializer):
        serializer.save()


class ApplicationListAPIView(generics.ListAPIView):
    serializer_class = ApplicationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    @swagger_auto_schema(operation_description="Foydalanuvchining barcha arizalarini qaytaradi")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)