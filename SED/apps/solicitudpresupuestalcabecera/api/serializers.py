from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from apps.solicitudpresupuestalcabecera.models import Solicitudpresupuestalcabecera
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.personalplanta.api.serializers import Personalplantaserializers
from apps.solicitudpresupuestaldetalle.api.serializers import SolicitudpresupuestaldetalleSerializers
from apps.periodo.models import Periodo

class SolicitudpresupuestalcabeceraSerializers(serializers.ModelSerializer):
    solicitudpresupuestaldetalle = SolicitudpresupuestaldetalleSerializers(many=True, read_only=True)
    class Meta:
        model = Solicitudpresupuestalcabecera
        fields=['id','institucioneducativaid','consecutivo','fecha','observacion','personalplantaidsolicitante','personalplantaidsolicitado','solicitudpresupuestaldetalle','objeto','estado']

    def validate_fecha(selft,value):
        periodo = Periodo.objects.filter(activo = True).first()

        if periodo:
            if value.year != periodo.codigo:
                raise serializers.ValidationError("la fecha no corresponde al periodo actual")
        else:
            raise serializers.ValidationError("No Exite un periodo abierto")
        
        return value

    def to_representation(self, instance):
        solicitudpresupuestalcabecera = super().to_representation(instance) 
        solicitudpresupuestalcabecera['institucioneducativaid'] = InstitucioneducativaSerializer(instance.institucioneducativaid).data
        solicitudpresupuestalcabecera['personalplantaidsolicitante'] = Personalplantaserializers(instance.personalplantaidsolicitante).data
        solicitudpresupuestalcabecera['personalplantaidsolicitado'] = Personalplantaserializers(instance.personalplantaidsolicitado).data        
        return solicitudpresupuestalcabecera  
