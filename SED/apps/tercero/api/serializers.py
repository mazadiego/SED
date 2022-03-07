from rest_framework import serializers
from apps.tercero.models import Tercero
from apps.tipoidentificacion.api.serializers import TipoidentificacionSerializer

class TerceroSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tercero
        fields = ['id','codigo', 'nombre','tipoidentificacionid']


    def to_representation(self, instance):
        tercero = super().to_representation(instance)
        tercero['tipoidentificacionid'] = TipoidentificacionSerializer(instance.tipoidentificacionid).data
        return tercero