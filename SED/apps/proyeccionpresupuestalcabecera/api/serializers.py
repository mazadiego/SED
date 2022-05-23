from rest_framework import serializers
from apps.proyeccionpresupuestalcabecera.models import Proyeccionpresupuestalcabecera
from apps.periodo.api.serializers import Periodoserializers
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.proyeccionpresupuestaldetalle.api.serializers import ProyeccionpresupuestaldetalleSerializers
from apps.periodo.models import Periodo

class ProyeccionpresupuestalcabeceraSerializers(serializers.ModelSerializer):
    proyeccionpresupuestaldetalle = ProyeccionpresupuestaldetalleSerializers(many=True, read_only=True)
    
    class Meta:
        model = Proyeccionpresupuestalcabecera
        fields = ['id','periodoid', 'institucioneducativaid','observacion','proyeccionpresupuestaldetalle']


    def validate_periodoid(selft,value):
        periodo = Periodo.objects.filter(activo = True).first()

        if periodo:
            if value != periodo.id:
                raise serializers.ValidationError("la fecha no corresponde al periodo actual")
        else:
            raise serializers.ValidationError("No Exite un periodo abierto")
        
        return value
   
    def to_representation(self, instance):
       proyeccionpresupuestalcabecera = super().to_representation(instance)
       proyeccionpresupuestalcabecera['periodoid'] = Periodoserializers(instance.periodoid).data
       proyeccionpresupuestalcabecera['institucioneducativaid'] = InstitucioneducativaSerializer(instance.institucioneducativaid).data
       return proyeccionpresupuestalcabecera  
    