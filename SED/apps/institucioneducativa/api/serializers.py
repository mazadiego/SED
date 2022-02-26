from rest_framework import serializers
from apps.institucioneducativa.models import Institucioneducativa

class InstitucioneducativaSerializer(serializers.ModelSerializer):
   # usuarioid = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Institucioneducativa
        fields = ['codigo', 'nombre','usuarioid']
        #fields = "__all__"