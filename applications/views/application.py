from rest_framework import generics, permissions

from applications.models import Application
from applications.serializers.application import ApplicationCreateSerializer

class ApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
