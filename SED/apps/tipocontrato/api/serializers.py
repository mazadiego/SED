from rest_framework import serializers
from apps.tipocontrato.models import Tipocontrato

class TipocontratoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tipocontrato
        fields = ['id','codigo', 'nombre']