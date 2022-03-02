from rest_framework import serializers
from apps.institucioneducativa.models import Institucioneducativa
from apps.usuario.api.serializers import UsuarioSerializer

class InstitucioneducativaSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Institucioneducativa
        fields = ['id','codigo', 'nombre','usuarioid']

   
    def to_representation(self, instance):
       institucioneducativa = super().to_representation(instance)
       institucioneducativa['usuarioid'] = UsuarioSerializer(instance.usuarioid).data
       return institucioneducativa  
    