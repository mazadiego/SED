from dataclasses import fields
from statistics import mode
from rest_framework import serializers
from apps.personalplanta.models import Personalplanta
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer


class Personalplantaserializers(serializers.ModelSerializer):

    class Meta:
        model = Personalplanta
        fields = ['id','codigo','nombre','cargo','institucioneducativaid']


    def to_representation(self, instance):
        personalplanta = super().to_representation(instance)
        personalplanta['institucioneducativaid'] = InstitucioneducativaSerializer(instance.institucioneducativaid).data
        return personalplanta