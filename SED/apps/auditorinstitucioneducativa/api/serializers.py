from rest_framework import serializers
from apps.auditorinstitucioneducativa.models import Auditoriainstitucioneducativa
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.user.api.serializers import UserListSerializer

class AuditoriainstitucioneducativaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Auditoriainstitucioneducativa
        fields = ['id','institucioneducativaid', 'usuarioid']

    def to_representation(self, instance):
        auditoriainstitucioneducativa = super().to_representation(instance)
        auditoriainstitucioneducativa['institucioneducativaid'] = InstitucioneducativaSerializer(instance.institucioneducativaid).data
        auditoriainstitucioneducativa['usuarioid'] = UserListSerializer(instance.usuarioid).data
        return auditoriainstitucioneducativa