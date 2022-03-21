from rest_framework import serializers
from apps.proyeccionpresupuestalcabecera.models import Proyeccionpresupuestalcabecera
from apps.periodo.api.serializers import Periodoserializers
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.proyeccionpresupuestaldetalle.api.serializers import ProyeccionpresupuestaldetalleSerializers

class ProyeccionpresupuestalcabeceraSerializers(serializers.ModelSerializer):
    proyeccionpresupuestaldetalle = ProyeccionpresupuestaldetalleSerializers(many=True, read_only=True)
    
    class Meta:
        model = Proyeccionpresupuestalcabecera
        fields = ['id','periodoid', 'institucioneducativaid','observacion','proyeccionpresupuestaldetalle']

   
    def to_representation(self, instance):
       proyeccionpresupuestalcabecera = super().to_representation(instance)
       proyeccionpresupuestalcabecera['periodoid'] = Periodoserializers(instance.periodoid).data
       proyeccionpresupuestalcabecera['institucioneducativaid'] = InstitucioneducativaSerializer(instance.institucioneducativaid).data
       return proyeccionpresupuestalcabecera  
    