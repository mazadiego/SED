from rest_framework import serializers


from apps.modificacionproyeccionpresupuestaldetalle.models import Modificacionproyeccionpresupuestaldetalle
from apps.fuenterecurso.api.serializers import Fuenterecursoserializers
from apps.rubropresupuestal.api.serializers import Rubropresupuestalserializers
from apps.proyeccionpresupuestalcabecera.models import Proyeccionpresupuestalcabecera
from apps.proyeccionpresupuestaldetalle.models import Proyeccionpresupuestaldetalle
from apps.fuenterecurso.api.api import saldofuenterecursoporingreso
from apps.rubropresupuestal.api.api import saldorubroporproyeccion

class ModificacionproyeccionpresupuestaldetalleSerializers(serializers.ModelSerializer):
    
    
    class Meta:
        model = Modificacionproyeccionpresupuestaldetalle
        fields = ['id','modificacionproyeccionpresupuestalid', 'fuenterecursoid','rubropresupuestalid','valor']

    def validate_valor(self, value):
        if value == 0 or value== None:
            raise serializers.ValidationError("Debe ingresar un valor diferente a cero (0)")
        return value
    

    def to_representation(self, instance):
       modificacionproyeccionpresupuestaldetalle = super().to_representation(instance)
       modificacionproyeccionpresupuestaldetalle['fuenterecursoid'] = Fuenterecursoserializers(instance.fuenterecursoid).data
       modificacionproyeccionpresupuestaldetalle['rubropresupuestalid'] = Rubropresupuestalserializers(instance.rubropresupuestalid).data
       return modificacionproyeccionpresupuestaldetalle 

class ValidarModificacionproyeccionpresupuestaldetalleSerializers(serializers.ModelSerializer):
    
    
    class Meta:
        model = Modificacionproyeccionpresupuestaldetalle
        fields = ['id','modificacionproyeccionpresupuestalid', 'fuenterecursoid','rubropresupuestalid','valor']

    def validate(self, data):
        saldo = 0
        if data['valor']<0:
            if 'modificacionproyeccionpresupuestalid' not in data.keys():
                raise serializers.ValidationError({
                    "modificacionproyeccionpresupuestalid": "Debe ingresar modificacionproyeccionpresupuestalid."
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
            modificacionproyeccionpresupuestal = data['modificacionproyeccionpresupuestalid']           
                        
            if not validarfuenterubro_modificacion(modificacionproyeccionpresupuestal,fuenterecurso,rubropresupuestal):        
                raise serializers.ValidationError({
                    "Modificacion fuente y rubro": "la fuente y rubro no tiene valor proyectado "            
                })
            
            if not saldofuenterecursoporingreso(fuenterecurso.id,modificacionproyeccionpresupuestal.institucioneducativaid.id,abs(data['valor'])):
                raise serializers.ValidationError({
                    "Fuente Recurso": "fuente recurso supera el valor de la proyeccion presupuestal asignada para el periodo"            
                })

            
            saldo = saldorubroporproyeccion(modificacionproyeccionpresupuestal.institucioneducativaid.id,rubropresupuestal.id) - abs(data['valor'])
        
            if saldo < 0:
                raise serializers.ValidationError({
                    "rubro presupuestal": "el valor del rubro presupuestal el valor de la proyeccion presupuestal asignada para el periodo"            
                })
            
        return data

def validarfuenterubro_modificacion(modificacionproyeccionpresupuestalcabecera,fuenterecurso,rubropresupuestal):
    
    validar = False
    
    proyeccionpresupuestalcabecera = Proyeccionpresupuestalcabecera.objects.filter(institucioneducativaid = modificacionproyeccionpresupuestalcabecera.institucioneducativaid.id,periodoid = modificacionproyeccionpresupuestalcabecera.periodoid.id).first()
    if proyeccionpresupuestalcabecera:
        proyeccionpresupuestaldetalle = Proyeccionpresupuestaldetalle.objects.filter(proyeccionpresupuestalid = proyeccionpresupuestalcabecera.id,fuenterecursoid = fuenterecurso.id,rubropresupuestalid = rubropresupuestal.id).first()
        if proyeccionpresupuestaldetalle:
            validar = True
    
    if validar == False:
        modificacionproyeccionpresupuestaldetalle = Modificacionproyeccionpresupuestaldetalle.objects.filter(modificacionproyeccionpresupuestalid = modificacionproyeccionpresupuestalcabecera.id,fuenterecursoid = fuenterecurso.id,rubropresupuestalid= rubropresupuestal.id, valor__gt = 0).first()
        if modificacionproyeccionpresupuestaldetalle:
            validar = True
    return validar