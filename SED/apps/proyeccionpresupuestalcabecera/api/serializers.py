from rest_framework import serializers
from apps.proyeccionpresupuestalcabecera.models import Proyeccionpresupuestalcabecera
from apps.periodo.api.serializers import Periodoserializers
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer

class ProyeccionpresupuestalcabeceraSerializers(serializers.ModelSerializer):
    
    
    class Meta:
        model = Proyeccionpresupuestalcabecera
        fields = ['id','periodoid', 'institucioneducativaid','observacion']

   
    def to_representation(self, instance):
       proyeccionpresupuestalcabecera = super().to_representation(instance)
       proyeccionpresupuestalcabecera['periodoid'] = Periodoserializers(instance.periodoid).data
       proyeccionpresupuestalcabecera['institucioneducativaid'] = InstitucioneducativaSerializer(instance.institucioneducativaid).data
       return proyeccionpresupuestalcabecera  
    