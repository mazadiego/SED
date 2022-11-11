from rest_framework import serializers
from apps.institucioneducativa.models import Institucioneducativa
from apps.user.api.serializers import UserListSerializer

class InstitucioneducativaSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Institucioneducativa
        fields = ['id','codigo', 'nombre','usuarioid']

   
    def to_representation(self, instance):
       institucioneducativa = super().to_representation(instance)
       institucioneducativa['usuarioid'] = UserListSerializer(instance.usuarioid).data
       return institucioneducativa  
    