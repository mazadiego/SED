from rest_framework import serializers

from apps.solicitudpresupuestaldetalle.models import Solicitudpresupuestaldetalle
from apps.rubropresupuestal.api.serializers import Rubropresupuestalserializers


class SolicitudpresupuestaldetalleSerializers(serializers.ModelSerializer):
        
    class Meta:
        model = Solicitudpresupuestaldetalle
        fields = ['id','solicitudpresupuestalcabeceraid', 'rubropresupuestalid','valor']

    def validate_valor(self, value):
        if value <=0 or value== None:
            raise serializers.ValidationError("Debe ingresar un valor mayor que cero (0)")
        return value
   
    def to_representation(self, instance):
       solicitudpresupuestaldetalle = super().to_representation(instance)
       solicitudpresupuestaldetalle['rubropresupuestalid'] = Rubropresupuestalserializers(instance.rubropresupuestalid).data
       return solicitudpresupuestaldetalle  