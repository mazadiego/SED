from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from apps.usuario.models import Usuario
from apps.usuario.api.serializers import UsuarioSerializer


@api_view(['GET','POST'])
def usuario_api_view(request):

    if request.method =='GET':
        usuario = Usuario.objects.all()
        usuario_serializer = UsuarioSerializer (usuario, many = True)
        return Response(usuario_serializer.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        usuario_serializer = UsuarioSerializer(data = request.data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return Response(usuario_serializer.data,status = status.HTTP_201_CREATED)
        return Response(usuario_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def usuario_details_api_view(request, codigo = None):
    usuario = Usuario.objects.filter(codigo=codigo).first()

    if usuario:
        if request.method == 'GET':            
            usuario_serializers = UsuarioSerializer(usuario)
            return Response(usuario_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT':            
            usuario_serializers = UsuarioSerializer(usuario, data = request.data)            
            if usuario_serializers.is_valid():
                usuario_serializers.save()
                return Response(usuario_serializers.data,status = status.HTTP_200_OK)
            return Response(usuario_serializers.errors,status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            usuario.delete()
            return Response({'Mensaje':'Eliminado Correctamente'},status = status.HTTP_200_OK)
    return Response({'Mensaje':'No Existe'},status = status.HTTP_400_BAD_REQUEST)

