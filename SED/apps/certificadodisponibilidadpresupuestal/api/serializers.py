from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from apps.certificadodisponibilidadpresupuestal.models import Certificadodisponibilidadpresupuestal
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.periodo.models import Periodo
from apps.solicitudpresupuestalcabecera.api.api import saldosolicitud_por_cdp
from apps.solicitudpresupuestalcabecera.api.serializers import SolicitudpresupuestalcabeceraSerializers

class CertificadodisponibilidadpresupuestalSerializers(serializers.ModelSerializer):

    class Meta:
        model= Certificadodisponibilidadpresupuestal
        fields=['id','institucioneducativaid','consecutivo','fecha','diasvalidez','observacion','valor','objeto','estado','solicitudpresupuestalcabeceraid']

    def validate_valor(selft,value):
        if value == None or value<=0:
            raise serializers.ValidationError("Debe ingresar un valor mayor que cero (0)")
        return value

    def validate_diasvalidez(selft,value):
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
        if 'valor' not in data.keys():
            raise serializers.ValidationError({
                "valor": "falta el nodo  valor."            
            })

        if 'solicitudpresupuestalcabeceraid' not in data.keys():
            raise serializers.ValidationError({
                "solicitudpresupuestalcabeceraid": "falta el nodo  solicitudpresupuestalcabeceraid."            
            })
        
        solicitudpresupuestalcabecera = data['solicitudpresupuestalcabeceraid']

        if solicitudpresupuestalcabecera.estado != 'Procesado':
            raise serializers.ValidationError({
                "solicitud presupuestal": "la solicitud debe tener estado Procesado para poder ser relacionada al documento CDP."            
            })

        saldo = saldosolicitud_por_cdp(solicitudpresupuestalcabecera) - data['valor']
        

        if saldo < 0:
            raise serializers.ValidationError({
                "solicitud presupuestal": "El valor ingresado sobrepasa el saldo del docuemnto solicitud relacionado."            
            })
            
        
        return data

    def to_representation(self, instance):
        cdp = super().to_representation(instance)
        cdp['institucioneducativaid']= InstitucioneducativaSerializer(instance.institucioneducativaid).data
        cdp['solicitudpresupuestalcabeceraid']= SolicitudpresupuestalcabeceraSerializers(instance.solicitudpresupuestalcabeceraid).data
        
        return cdp