from rest_framework import serializers
from apps.tiporecaudo.models import Tiporecaudo

class TiporecaudoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tiporecaudo
        fields = ['id','codigo', 'nombre']