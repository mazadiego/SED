from rest_framework import serializers

from apps.modificacionproyeccionpresupuestaldetalle.models import Modificacionproyeccionpresupuestaldetalle
from apps.fuenterecurso.api.serializers import Fuenterecursoserializers
from apps.rubropresupuestal.api.serializers import Rubropresupuestalserializers

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