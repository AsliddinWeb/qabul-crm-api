from rest_framework import serializers
from applications.models import Application, PassportInfo, DiplomInfo
from programs.models import TuitionFee

class PassportInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportInfo
        fields = '__all__'

class DiplomInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiplomInfo
        fields = '__all__'

class ApplicationCreateSerializer(serializers.ModelSerializer):
    passport = PassportInfoSerializer()
    diplom = DiplomInfoSerializer()

    class Meta:
        model = Application
        fields = [
            'passport', 'diplom', 'tuition_fee',
            'admission_type', 'study_year'
        ]

    def create(self, validated_data):
        passport_data = validated_data.pop('passport')
        diplom_data = validated_data.pop('diplom')
        user = self.context['request'].user

        passport = PassportInfo.objects.create(**passport_data)
        diplom = DiplomInfo.objects.create(**diplom_data)

        application = Application.objects.create(
            user=user,
            passport=passport,
            diplom=diplom,
            **validated_data
        )
        return application
