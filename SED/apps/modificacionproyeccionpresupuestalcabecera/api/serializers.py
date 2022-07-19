from rest_framework import serializers
from apps.modificacionproyeccionpresupuestalcabecera.models import Modificacionproyeccionpresupuestalcabecera
from apps.periodo.api.serializers import Periodoserializers
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.modificacionproyeccionpresupuestaldetalle.api.serializers import ModificacionproyeccionpresupuestaldetalleSerializers
from apps.periodo.models import Periodo

class ModificacionproyeccionpresupuestalcabeceraSerializers(serializers.ModelSerializer):
    modificacionproyeccionpresupuestaldetalle = ModificacionproyeccionpresupuestaldetalleSerializers(many=True, read_only=True)
    
    
    class Meta:
        model = Modificacionproyeccionpresupuestalcabecera
        fields = ['id','periodoid', 'institucioneducativaid','observacion','objeto','estado','modificacionproyeccionpresupuestaldetalle']


    def validate_periodoid(selft,value):
        periodo = Periodo.objects.filter(activo = True).first()

        if periodo:
            if value.id != periodo.id:
                raise serializers.ValidationError("la fecha no corresponde al periodo actual")
        else:
            raise serializers.ValidationError("No Exite un periodo abierto")
        
        return value
   
    def to_representation(self, instance):
       modificacionproyeccionpresupuestalcabecera = super().to_representation(instance)
       modificacionproyeccionpresupuestalcabecera['periodoid'] = Periodoserializers(instance.periodoid).data
       modificacionproyeccionpresupuestalcabecera['institucioneducativaid'] = InstitucioneducativaSerializer(instance.institucioneducativaid).data
       return modificacionproyeccionpresupuestalcabecera  
    