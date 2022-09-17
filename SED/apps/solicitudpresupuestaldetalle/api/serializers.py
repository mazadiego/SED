from rest_framework import serializers

from apps.solicitudpresupuestaldetalle.models import Solicitudpresupuestaldetalle
from apps.rubropresupuestal.api.serializers import Rubropresupuestalserializers
from apps.fuenterecurso.api.serializers import Fuenterecursoserializers
from apps.rubropresupuestal.api.api import saldorubroporproyeccion
from apps.fuenterecurso.api.api import saldo_fuente_recaudos
class SolicitudpresupuestaldetalleSerializers(serializers.ModelSerializer):
        
    class Meta:
        model = Solicitudpresupuestaldetalle
        fields = ['id','solicitudpresupuestalcabeceraid', 'rubropresupuestalid','valor','fuenterecursoid']

    def validate_valor(self, value):
        if value <=0 or value== None:
            raise serializers.ValidationError("Debe ingresar un valor mayor que cero (0)")
        return value

    def validate(self, data):
        saldo = 0
        if 'solicitudpresupuestalcabeceraid' not in data.keys():
            raise serializers.ValidationError({
                "solicitudpresupuestalcabeceraid": "Debe ingresar solicitudpresupuestalcabeceraid."
            })
        
        if 'fuenterecursoid' not in data.keys():
            raise serializers.ValidationError({
                "fuenterecursoid": "Debe ingresar fuenterecursoid."            
            })

        if 'rubropresupuestalid' not in data.keys():
            raise serializers.ValidationError({
                "rubropresupuestalid": "Debe ingresar rubropresupuestalid."            
            })

        fuenterecurso = data['fuenterecursoid']
        rubropresupuestal = data['rubropresupuestalid']
        solicitudpresupuestalcabecera = data['solicitudpresupuestalcabeceraid']  

        if solicitudpresupuestalcabecera.estado != 'Procesado': 
            raise serializers.ValidationError({
                "Estado" : "No se puede agregar valores al documento en este estado"            
            })         
        
        saldo = saldo_fuente_recaudos(solicitudpresupuestalcabecera.institucioneducativaid.id,fuenterecurso.id) - data['valor']

        if saldo < 0:
            raise serializers.ValidationError({
                "Fuente Recurso": "el valor de la fuente de recurso supera el saldo recaudado"            
            })

        saldo = saldorubroporproyeccion(solicitudpresupuestalcabecera.institucioneducativaid.id,rubropresupuestal.id) - data['valor']
        
        if saldo < 0:
            raise serializers.ValidationError({
                "rubro presupuestal": "el valor del rubro presupuestal supera el saldo proyectado"            
            })
            
        return data
   
    def to_representation(self, instance):
       solicitudpresupuestaldetalle = super().to_representation(instance)
       solicitudpresupuestaldetalle['rubropresupuestalid'] = Rubropresupuestalserializers(instance.rubropresupuestalid).data
       solicitudpresupuestaldetalle['fuenterecursoid'] = Fuenterecursoserializers(instance.fuenterecursoid).data
       return solicitudpresupuestaldetalle  