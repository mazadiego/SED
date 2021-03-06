from dataclasses import fields
from pyexpat import model
from rest_framework import serializers


from apps.registropresupuestal.models import Registropresupuestal
from apps.institucioneducativa.api.api import InstitucioneducativaSerializer
from apps.tercero.api.api import TerceroSerializer
from apps.certificadodisponibilidadpresupuestal.api.api import CertificadodisponibilidadpresupuestalSerializers
from apps.periodo.models import Periodo
from apps.certificadodisponibilidadpresupuestal.api.api import saldocdp_por_rp

class Registropresupuestalserializers(serializers.ModelSerializer):

    class Meta: 
        model=Registropresupuestal
        fields=['institucioneducativaid','consecutivo','fecha','terceroid','observacion','certificadodisponibilidadpresupuestalid','valor']

    def validate_valor(selft,value):        
        if value == None or value<=0:
            raise serializers.ValidationError("Debe ingresar un valor mayor que cero (0)")
        return value
    
    def validate_fecha(selft,value):
        periodo = Periodo.objects.filter(activo = True).first()

        if periodo:
            if value.year != periodo.codigo:
                raise serializers.ValidationError("la fecha no corresponde al periodo actual")
        else:
            raise serializers.ValidationError("No Exite un periodo abierto")
        
        return value
    def validate(self, data):
        saldocdp = 0
        if 'valor' not in data.keys():
            raise serializers.ValidationError({
                "valor": "falta el nodo  valor."            
            })
        
        if 'certificadodisponibilidadpresupuestalid' not in data.keys():
            raise serializers.ValidationError({
                "certificadodisponibilidadpresupuestalid": "falta el nodo  certificadodisponibilidadpresupuestalid."            
            })
        saldocdp = saldocdp_por_rp(data['certificadodisponibilidadpresupuestalid'].id) - data['valor']

        if saldocdp < 0:
            raise serializers.ValidationError("El valor ingresado sobrepasa el saldo del cdp expedido")

        return data

    def to_representation(self, instance):
        registropresupuestal = super().to_representation(instance)
        registropresupuestal['institucioneducativaid']=InstitucioneducativaSerializer(instance.institucioneducativaid).data
        registropresupuestal['terceroid']=TerceroSerializer(instance.terceroid).data
        registropresupuestal['certificadodisponibilidadpresupuestalid'] = CertificadodisponibilidadpresupuestalSerializers(instance.certificadodisponibilidadpresupuestalid).data
        return registropresupuestal