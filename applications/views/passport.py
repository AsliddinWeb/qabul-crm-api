from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from applications.models.passport import Region, District, PassportInfo
from applications.serializers.passport import RegionSerializer, DistrictSerializer, PassportInfoSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegionListAPIView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(operation_description="Barcha viloyatlarni ro‘yxatini qaytaradi")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class DistrictByRegionAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('region_id', openapi.IN_QUERY, description="Viloyat ID si", type=openapi.TYPE_INTEGER)
        ],
        operation_description="Viloyat ID bo‘yicha tumanlar ro‘yxatini qaytaradi"
    )
    def get(self, request):
        region_id = request.query_params.get('region_id')
        if not region_id:
            return Response({"error": "region_id kiritilishi kerak"}, status=400)
        districts = District.objects.filter(region_id=region_id)
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data)

class PassportInfoCreateAPIView(generics.CreateAPIView):
    serializer_class = PassportInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Foydalanuvchi uchun yangi pasport ma’lumotlarini yaratish")
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PassportInfoRetrieveAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Bearer token orqali foydalanuvchining pasport ma’lumotlarini olish")
    def get(self, request):
        passport = PassportInfo.objects.filter(user=request.user).first()
        if passport:
            serializer = PassportInfoSerializer(passport)
            return Response(serializer.data)
        return Response({"detail": "Pasport ma’lumoti topilmadi"}, status=404)
