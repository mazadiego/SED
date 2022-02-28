from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from apps.institucioneducativa.models import Institucioneducativa
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.usuario.models import Usuario
from apps.usuario.api.serializers import UsuarioSerializer


@api_view(['GET','POST'])
def institucioneducativa_api_view(request):

    if request.method =='GET':
        institucioneducativa = Institucioneducativa.objects.all()
        institucioneducativa_serializer = InstitucioneducativaSerializer (institucioneducativa, many = True)
        return Response(institucioneducativa_serializer.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        data = request.data        
        usuarioid = data.pop('usuarioid')
        usuario = Usuario.objects.filter(codigo = usuarioid['codigo']).first() 
        if usuario:
            usuarioid_serializer = UsuarioSerializer(usuario)
            usuarioid = dict(usuarioid_serializer.data)
            data.update({"usuarioid": usuarioid['id'] })
            institucioneducativa_serializer = InstitucioneducativaSerializer(data = request.data)            
            
            if institucioneducativa_serializer.is_valid():
                institucioneducativa_serializer.save()
                return Response(institucioneducativa_serializer.data,status = status.HTTP_201_CREATED)
            return Response(institucioneducativa_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'Mensaje':'Usuario Ingresado No Existe'},status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def institucioneducativa_details_api_view(request, codigo = None):
    institucioneducativa = Institucioneducativa.objects.filter(codigo=codigo).first()

    if institucioneducativa:
        if request.method == 'GET':            
            institucioneducativa_serializers = InstitucioneducativaSerializer(institucioneducativa)
            return Response(institucioneducativa_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT':
            data = request.data        
            usuarioid = data.pop('usuarioid')
            usuario = Usuario.objects.filter(codigo = usuarioid['codigo']).first()
            if usuario:
                usuarioid_serializer = UsuarioSerializer(usuario)
                usuarioid = dict(usuarioid_serializer.data)
                data.update({"usuarioid": usuarioid['id'] })             
                institucioneducativa_serializers = InstitucioneducativaSerializer(institucioneducativa, data = request.data)            
                if institucioneducativa_serializers.is_valid():
                    institucioneducativa_serializers.save()
                    return Response(institucioneducativa_serializers.data,status = status.HTTP_200_OK)
                return Response(institucioneducativa_serializers.errors,status = status.HTTP_400_BAD_REQUEST)
            return Response({'Mensaje':'Usuario Ingresado No Existe'},status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            institucioneducativa.delete()
            return Response({'Mensaje':'Eliminado Correctamente'},status = status.HTTP_200_OK)
    return Response({'Mensaje':'No Existe'},status = status.HTTP_400_BAD_REQUEST)

