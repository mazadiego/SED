from rest_framework import serializers

from apps.proyeccionpresupuestaldetalle.models import Proyeccionpresupuestaldetalle
from apps.fuenterecurso.api.serializers import Fuenterecursoserializers
from apps.rubropresupuestal.api.serializers import Rubropresupuestalserializers

class ProyeccionpresupuestaldetalleSerializers(serializers.ModelSerializer):
    
    
    class Meta:
        model = Proyeccionpresupuestaldetalle
        fields = ['id','proyeccionpresupuestalid', 'fuenterecursoid','rubropresupuestalid','valor']

    def validate_valor(self, value):
        if value <=0 or value== None:
            raise serializers.ValidationError("Debe ingresar un valor mayor que cero (0)")
        return value
   
    def to_representation(self, instance):
       proyeccionpresupuestaldetalle = super().to_representation(instance)
       proyeccionpresupuestaldetalle['fuenterecursoid'] = Fuenterecursoserializers(instance.fuenterecursoid).data
       proyeccionpresupuestaldetalle['rubropresupuestalid'] = Rubropresupuestalserializers(instance.rubropresupuestalid).data
       return proyeccionpresupuestaldetalle  