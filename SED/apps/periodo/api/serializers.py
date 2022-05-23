from dataclasses import fields
from pyexpat import model
from statistics import mode
from rest_framework import serializers
from apps.periodo.models import Periodo

class Periodoserializers(serializers.ModelSerializer):

    class Meta:
        model = Periodo
        fields = ['id','codigo','activo']

    def validate_activo(selft,value):  
        periodo = Periodo.objects.filter(activo = True).first()

        if periodo and value==True: 
            raise serializers.ValidationError("ya existe un periodo activo")
        return value
