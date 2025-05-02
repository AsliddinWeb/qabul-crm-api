from rest_framework import serializers
from applications.models.diplom import DiplomInfo

class DiplomInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiplomInfo
        fields = '__all__'
        read_only_fields = ['user']
        extra_kwargs = {
            'institution_name': {'label': 'Muassasa nomi'},
            'diplom_number': {'label': 'Diplom raqami'},
            'graduation_year': {'label': 'Bitirgan yil'},
            'degree_level': {'label': 'Daraja turi'},
            'diplom_file': {'label': 'Diplom fayli'}
        }
