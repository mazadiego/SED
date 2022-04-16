from contextlib import nullcontext
from dataclasses import fields
from statistics import mode
from rest_framework import serializers
from apps.consecutivo.models import Consecutivo

class Consecutivoserializers(serializers.ModelSerializer):
    

    class Meta:
        model = Consecutivo
        fields = ['id','tipodocumento', 'institucioneducativaid','consecutivo']
    
   