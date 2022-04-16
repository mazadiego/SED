from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from apps.ingresopresupuestal.models import Ingresopresupuestal

from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.fuenterecurso.api.serializers import Fuenterecursoserializers
from apps.tercero.api.serializers import TerceroSerializer

class Ingresopresupuestalserializers(serializers.ModelSerializer):

    class Meta:
        model = Ingresopresupuestal
        fields = ['id','institucioneducativaid','consecutivo','fecha','terceroid','fuenterecursoid','observacion','valor','fechaproyeccionrecaudo']

    
    def validate_valor(self, value):
        if value <=0 or value== None:
            raise serializers.ValidationError("Debe ingresar un valor mayor que cero (0)")
        return value

    def to_representation(self, instance):
        ingresopresupuestal = super().to_representation(instance)
        ingresopresupuestal['institucioneducativaid'] = InstitucioneducativaSerializer(instance.institucioneducativaid).data
        ingresopresupuestal['terceroid'] = TerceroSerializer(instance.terceroid).data
        ingresopresupuestal['fuenterecursoid'] = Fuenterecursoserializers(instance.fuenterecursoid).data
        return ingresopresupuestal
        
