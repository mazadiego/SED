from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from apps.certificadodisponibilidadpresupuestal.models import Certificadodisponibilidadpresupuestal
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.rubropresupuestal.api.serializers import Rubropresupuestalserializers
from apps.rubropresupuestal.api.api import saldo_rubro_solicitud,saldo_rubro_cdp,saldo_rubro_recaudos
from apps.periodo.models import Periodo

class CertificadodisponibilidadpresupuestalSerializers(serializers.ModelSerializer):

    class Meta:
        model= Certificadodisponibilidadpresupuestal
        fields=['id','institucioneducativaid','consecutivo','fecha','diasvalidez','rubropresupuestalid','observacion','valor']

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
        saldo = 0
        saldosolicitud = 0
        saldosrecaudos = 0
        if 'institucioneducativaid' not in data.keys():
            raise serializers.ValidationError({
                "institucioneducativaid": "falta el nodo institucioneducativaid."
            })
        
        if 'rubropresupuestalid' not in data.keys():
            raise serializers.ValidationError({
                "rubropresupuestalid": "falta el nodo  rubropresupuestalid."            
            })
        
        if 'valor' not in data.keys():
            raise serializers.ValidationError({
                "valor": "falta el nodo  valor."            
            })
        
        
        saldosolicitud = saldo_rubro_solicitud(data['institucioneducativaid'].id,data['rubropresupuestalid'].id)
        saldocdp = saldo_rubro_cdp(data['institucioneducativaid'].id,data['rubropresupuestalid'].id)        
        saldosrecaudos = saldo_rubro_recaudos(data['institucioneducativaid'].id,data['rubropresupuestalid'].id)

        #saldo CDP vs los recuados por rubro presupuestal
        saldo = saldosrecaudos - (saldocdp + data['valor'])
        print(saldo)
        if saldo < 0:
            raise serializers.ValidationError("El valor ingresado sobrepasa el saldo por recaudos del rubro presupuestal seleccionado")

        
        #saldo CDP vs solicitud por rubro presupuestal
        saldo = saldosolicitud - (saldocdp + data['valor'])
        print(saldo)
        if saldo < 0:
            raise serializers.ValidationError("El valor ingresado sobrepasa el saldo por soicitud del rubro presupuestal seleccionado")
       
        return data

    def to_representation(self, instance):
        cdp = super().to_representation(instance)
        cdp['institucioneducativaid']= InstitucioneducativaSerializer(instance.institucioneducativaid).data
        cdp['rubropresupuestalid'] = Rubropresupuestalserializers(instance.rubropresupuestalid).data
        return cdp