from rest_framework import serializers

from apps.proyeccionpresupuestaldetalle.models import Proyeccionpresupuestaldetalle
from apps.fuenterecurso.api.serializers import Fuenterecursoserializers
from apps.rubropresupuestal.api.serializers import Rubropresupuestalserializers

class ProyeccionpresupuestaldetalleSerializers(serializers.ModelSerializer):
    
    
    class Meta:
        model = Proyeccionpresupuestaldetalle
        fields = ['id','proyeccionpresupuestalid', 'fuenterecursoid','rubropresupuestalid','valor']

   
    def to_representation(self, instance):
       proyeccionpresupuestaldetalle = super().to_representation(instance)
       proyeccionpresupuestaldetalle['fuenterecursoid'] = Fuenterecursoserializers(instance.fuenterecursoid).data
       proyeccionpresupuestaldetalle['rubropresupuestalid'] = Rubropresupuestalserializers(instance.rubropresupuestalid).data
       return proyeccionpresupuestaldetalle  