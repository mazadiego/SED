from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from apps.obligacionpresupuestal.models import Obligacionpresupuestal
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.registropresupuestal.api.serializers import Registropresupuestalserializers
from apps.periodo.models import Periodo
from apps.registropresupuestal.api.api import saldo_rp_por_op

class ObligacionpresupuestalSerializers(serializers.ModelSerializer):
    class Meta: 
        model=Obligacionpresupuestal
        fields=['institucioneducativaid','consecutivo','fecha','recibosatisfacion','observacion','registropresupuestalid','valor','objeto','estado']
        

    def validate_valor(selft,value):        
        if value == None or value<=0:
            raise serializers.ValidationError("Debe ingresar un valor mayor que cero (0)")
        return value
    
    def validate_objeto(selft,value):  
        if value == None or value =="":
            raise serializers.ValidationError({"objeto":"debe ingresar un valor"})
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

        if 'objeto' not in data.keys():
            raise serializers.ValidationError({
                "objeto": "falta el nodo  objeto."            
            })
        
        if 'registropresupuestalid' not in data.keys():
            raise serializers.ValidationError({
                "registropresupuestalid": "falta el nodo  registropresupuestalid."            
            })

        registropresupuestal = data['registropresupuestalid']

        if registropresupuestal.estado != 'Procesado':
            raise serializers.ValidationError({
                "estado":" el RP debe tener estado procesado para poder ser relacionado a una Obligacion Presupuestal"
            }
            )
            
        saldocdp = saldo_rp_por_op(registropresupuestal.id) - data['valor']

        if saldocdp < 0:
            raise serializers.ValidationError({
                "Registro Presupuestal":"El valor ingresado sobrepasa el saldo del RP expedido"
                })

        return data

    def to_representation(self, instance):
        obligacionpresupuestal = super().to_representation(instance)
        obligacionpresupuestal['institucioneducativaid'] = InstitucioneducativaSerializer(instance.institucioneducativaid).data
        obligacionpresupuestal['registropresupuestalid'] = Registropresupuestalserializers(instance.registropresupuestalid).data
        return obligacionpresupuestal
