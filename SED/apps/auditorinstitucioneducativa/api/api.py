from typing import Any
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from apps.user.models import User
from apps.institucioneducativa.models import Institucioneducativa
from apps.auditorinstitucioneducativa.models import Auditoriainstitucioneducativa
from apps.auditorinstitucioneducativa.api.serializers import AuditoriainstitucioneducativaSerializer
from django.db.utils import IntegrityError
from apps.user.api.serializers import UserListSerializer

@api_view(['GET','POST'])
def auditoriainstitucioneducativa_api_view(request, username = None):
    if request.method == 'GET':
        auditoriainstitucioneducativa = Auditoriainstitucioneducativa.objects.filter(usuarioid__username = username).all()
        if auditoriainstitucioneducativa:
            auditoriainstitucioneducativa_serializers = AuditoriainstitucioneducativaSerializer(auditoriainstitucioneducativa, many = True)
            return Response(auditoriainstitucioneducativa_serializers.data,status = status.HTTP_200_OK)
        return Response("no existen datos para los parametros ingresados",status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':

        if 'institucioneducativaid' in request.data.keys():
            institucioneducativaid = request.data.pop('institucioneducativaid')
            if 'codigo' in institucioneducativaid.keys():
                institucioneducativa = Institucioneducativa.objects.filter(codigo = institucioneducativaid['codigo']).first() 
                if institucioneducativa:
                    request.data.update({"institucioneducativaid": institucioneducativa.id})
                else:
                    return Response("institucion educativa ingresada no existe",status = status.HTTP_400_BAD_REQUEST)                     
            else:
                return Response("falta el nodo codigo para institucion educativa",status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response("falta el nodo institucioneducativaid",status = status.HTTP_400_BAD_REQUEST) 

        if 'usuarioid' in request.data.keys():
            usuarioid = request.data.pop('usuarioid')
            if 'username' in usuarioid.keys():
                usuario = User.objects.filter(username = usuarioid['username']).first() 
                if usuario:
                    request.data.update({"usuarioid": usuario.id})
                else:
                    return Response("usuario no existe",status = status.HTTP_400_BAD_REQUEST)                     
            else:
                return Response("falta el nodo username para usuario",status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response("falta el nodo usuarioid",status = status.HTTP_400_BAD_REQUEST) 

        auditoriainstitucioneducativa_serializers = AuditoriainstitucioneducativaSerializer(data=request.data)

        if auditoriainstitucioneducativa_serializers.is_valid():
            try:
                auditoriainstitucioneducativa_serializers.save()
                return Response(auditoriainstitucioneducativa_serializers.data,status = status.HTTP_200_OK)
            except IntegrityError:
                return Response('ya exite una configuracion para usuario e institucion educativa',status = status.HTTP_400_BAD_REQUEST)
        return Response(auditoriainstitucioneducativa_serializers.errors,status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])
def auditoriainstitucioneducativa_id_api_view(request, id = None):
    auditoriainstitucioneducativa = Auditoriainstitucioneducativa.objects.filter(id = id).first()

    if auditoriainstitucioneducativa:
        if request.method == 'GET':
            auditoriainstitucioneducativa_serializers = AuditoriainstitucioneducativaSerializer(auditoriainstitucioneducativa)
            return Response(auditoriainstitucioneducativa_serializers.data,status = status.HTTP_200_OK)
        elif request.method == 'DELETE':
            auditoriainstitucioneducativa.delete()
            return Response("Eliminado Correctamente",status = status.HTTP_200_OK)

    return Response("no existen datos para los parametros ingresados",status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def auditoriainstitucioneducativa_usuarios_api_view(request):
    if request.method == 'GET': 
        usuarios = User.objects.filter(rol= 'Auditor').all() 
        usuarioserializer = UserListSerializer(usuarios, many=True)
        return Response(usuarioserializer.data,status = status.HTTP_200_OK)