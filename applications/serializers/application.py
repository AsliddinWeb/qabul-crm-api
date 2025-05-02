from rest_framework import serializers
from applications.models import Application, PassportInfo, DiplomInfo
from programs.models import TuitionFee
from .passport import PassportInfoSerializer
from .diplom import DiplomInfoSerializer

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'tuition_fee',
            'admission_type',
            'study_year'
        ]

    def create(self, validated_data):
        user = self.context['request'].user

        passport = PassportInfo.objects.filter(user=user).first()
        diplom = DiplomInfo.objects.filter(user=user).first()

        if not passport:
            raise serializers.ValidationError("Pasport ma’lumoti topilmadi.")
        if not diplom:
            raise serializers.ValidationError("Diplom ma’lumoti topilmadi.")

        # ✅ Oldindan ariza mavjudmi – tekshir
        if Application.objects.filter(passport=passport).exists():
            raise serializers.ValidationError("Bu pasportga bog‘langan ariza allaqachon mavjud.")

        return Application.objects.create(
            user=user,
            passport=passport,
            diplom=diplom,
            **validated_data
        )

class ApplicationDetailSerializer(serializers.ModelSerializer):
    passport = PassportInfoSerializer()
    diplom = DiplomInfoSerializer()

    class Meta:
        model = Application
        fields = [
            'id',
            'passport',
            'diplom',
            'tuition_fee',
            'admission_type',
            'study_year',
            'status'
        ]