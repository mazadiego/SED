from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from apps.pagopresupuestal.models import Pagopresupuestal
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.obligacionpresupuestal.api.serializers import ObligacionpresupuestalSerializers
from apps.periodo.models import Periodo
from apps.obligacionpresupuestal.api.api import saldo_opresu_por_pagopresu

class PagopresupuestalSerializers(serializers.ModelSerializer):
    class Meta: 
        model=Pagopresupuestal
        fields=['institucioneducativaid','consecutivo','fecha','observacion','obligacionpresupuestalid','valor']
        

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
        
        if 'obligacionpresupuestalid' not in data.keys():
            raise serializers.ValidationError({
                "obligacionpresupuestalid": "falta el nodo  obligacionpresupuestalid."            
            })
        saldocdp = saldo_opresu_por_pagopresu(data['obligacionpresupuestalid'].id) - data['valor']

        if saldocdp < 0:
            raise serializers.ValidationError("El valor ingresado sobrepasa el saldo de la obligacion presupuestal expedida")

        return data

    def to_representation(self, instance):
        pagopresupuestal = super().to_representation(instance)
        pagopresupuestal['institucioneducativaid'] = InstitucioneducativaSerializer(instance.institucioneducativaid).data
        pagopresupuestal['obligacionpresupuestalid'] = ObligacionpresupuestalSerializers(instance.obligacionpresupuestalid).data
        return pagopresupuestal
