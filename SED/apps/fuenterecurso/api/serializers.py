from contextlib import nullcontext
from dataclasses import fields
from statistics import mode
from rest_framework import serializers
from apps.fuenterecurso.models import Fuenterecurso

class Fuenterecursoserializers(serializers.ModelSerializer):
    

    class Meta:
        model = Fuenterecurso
        fields = ['id','codigo','nombre','idpadre']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'codigo': instance.codigo,
            'nombre': instance.nombre,
            'idpadre': Fuenterecursoserializers(Fuenterecurso.objects.filter(id = instance.idpadre).first()).data if instance.idpadre is not None else 0
        }