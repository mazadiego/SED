from rest_framework import serializers
from apps.tipoidentificacion.models import Tipoidentificacion

class TipoidentificacionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tipoidentificacion
        fields = ['id','codigo', 'nombre']