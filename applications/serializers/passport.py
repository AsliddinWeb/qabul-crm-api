from rest_framework import serializers
from applications.models.passport import Region, District, PassportInfo

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'label': 'Viloyat nomi'}
        }

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'region']
        extra_kwargs = {
            'name': {'label': 'Tuman nomi'},
            'region': {'label': 'Tegishli viloyat'}
        }

class PassportInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportInfo
        fields = '__all__'
        read_only_fields = ['user']  # foydalanuvchi tomonidan kiritilmasin
        extra_kwargs = {
            'full_name': {'label': 'F.I.Sh'},
            'birth_date': {'label': 'Tug‘ilgan sana'},
            'passport_series': {'label': 'Pasport seriyasi'},
            'passport_number': {'label': 'Pasport raqami'},
            'given_by': {'label': 'Kim tomonidan berilgan'},
            'address': {'label': 'Yashash manzili'},
            'region': {'label': 'Viloyat'},
            'district': {'label': 'Tuman'},
            'image': {'label': 'Pasport rasmi'},
        }

