from dataclasses import fields
from pyexpat import model
from statistics import mode
from rest_framework import serializers
from apps.periodo.models import Periodo

class Periodoserializers(serializers.ModelSerializer):

    class Meta:
        model = Periodo
        fields = ['id','periodo','activo']
