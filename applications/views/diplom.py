from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from applications.models.diplom import DiplomInfo
from applications.serializers.diplom import DiplomInfoSerializer
from drf_yasg.utils import swagger_auto_schema

class DiplomInfoCreateAPIView(generics.CreateAPIView):
    serializer_class = DiplomInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Foydalanuvchi uchun yangi diplom ma’lumotlarini yaratish")
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DiplomInfoRetrieveAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Bearer token orqali foydalanuvchining diplom ma’lumotlarini olish")
    def get(self, request):
        diplom = DiplomInfo.objects.filter(user=request.user).first()
        if diplom:
            serializer = DiplomInfoSerializer(diplom)
            return Response(serializer.data)
        return Response({"detail": "Diplom ma’lumoti topilmadi"}, status=404)
