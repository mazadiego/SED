from rest_framework import serializers
from apps.recaudopresupuestal.models import Recaudopresupuestal


from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.ingresopresupuestal.api.serializers import Ingresopresupuestalserializers
from apps.tiporecaudo.api.serializers import TiporecaudoSerializer
from apps.periodo.models import Periodo

class Recaudopresupuestalserializers(serializers.ModelSerializer):

    class Meta:
        model = Recaudopresupuestal
        fields = ['id','institucioneducativaid','consecutivo','fecha','ingresopresupuestalid','tiporecaudoid','documentorecaudo','observacion','valor','objeto','estado']
        
    
    def validate_valor(self, value):
        if value <=0 or value== None:
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

    def to_representation(self, instance):
        ingresopresupuestal = super().to_representation(instance)
        ingresopresupuestal['institucioneducativaid'] = InstitucioneducativaSerializer(instance.institucioneducativaid).data
        ingresopresupuestal['ingresopresupuestalid'] = Ingresopresupuestalserializers(instance.ingresopresupuestalid).data
        ingresopresupuestal['tiporecaudoid'] = TiporecaudoSerializer(instance.tiporecaudoid).data
        return ingresopresupuestal