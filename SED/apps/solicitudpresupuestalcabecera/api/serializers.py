from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from apps.solicitudpresupuestalcabecera.models import Solicitudpresupuestalcabecera
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.personalplanta.api.serializers import Personalplantaserializers
from apps.tercero.api.serializers import TerceroSerializer
from apps.tipocontrato.api.serializers import TipocontratoSerializer
from apps.solicitudpresupuestaldetalle.api.serializers import SolicitudpresupuestaldetalleSerializers

class SolicitudpresupuestalcabeceraSerializers(serializers.ModelSerializer):
    solicitudpresupuestaldetalle = SolicitudpresupuestaldetalleSerializers(many=True, read_only=True)
    class Meta:
        model = Solicitudpresupuestalcabecera
        fields=['id','institucioneducativaid','consecutivo','fecha','observacion','personalplantaidsolicitante','personalplantaidsolicitado','terceroid','tipocontratoid','fechainiciocontrato','fechafincontrato','contratonumero','solicitudpresupuestaldetalle']

    def to_representation(self, instance):
        solicitudpresupuestalcabecera = super().to_representation(instance) 
        solicitudpresupuestalcabecera['institucioneducativaid'] = InstitucioneducativaSerializer(instance.institucioneducativaid).data
        solicitudpresupuestalcabecera['personalplantaidsolicitante'] = Personalplantaserializers(instance.personalplantaidsolicitante).data
        solicitudpresupuestalcabecera['personalplantaidsolicitado'] = Personalplantaserializers(instance.personalplantaidsolicitado).data
        solicitudpresupuestalcabecera['terceroid'] =TerceroSerializer(instance.terceroid).data
        solicitudpresupuestalcabecera['tipocontratoid'] = TipocontratoSerializer(instance.tipocontratoid).data
        return solicitudpresupuestalcabecera  
