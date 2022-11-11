from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.user.models import User
from apps.user.api.serializers import UserSerializer, UserListSerializer
from django.db.models.deletion import RestrictedError


@api_view(['GET','POST'])
def usuario_api_view(request):

    if request.method =='GET':
        usuario = User.objects.all()
        usuario_serializer = UserListSerializer (usuario, many = True)
        return Response(usuario_serializer.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        usuario_serializer = UserSerializer(data = request.data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return Response(usuario_serializer.data,status = status.HTTP_201_CREATED)
        return Response(usuario_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def usuario_details_api_view(request, username = None):
    
    usuario = User.objects.filter(username=username).first()

    if usuario:
        if request.method == 'GET':            
            usuario_serializers = UserListSerializer(usuario)
            return Response(usuario_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT': 
            if 'username' in request.data.keys():
                request.data['username'] = username          
                usuario_serializers = UserSerializer(usuario, data = request.data)            
                if usuario_serializers.is_valid():
                    usuario_serializers.save()
                    return Response(usuario_serializers.data,status = status.HTTP_200_OK)
                return Response(usuario_serializers.errors,status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo username',status = status.HTTP_400_BAD_REQUEST) 
        elif request.method == 'DELETE':
                    
            usuario.is_active = False      
            usuario.save()
            return Response('Usuario Desactivado Correctamente',status = status.HTTP_200_OK)
           
    return Response('Usuario No Existe',status = status.HTTP_400_BAD_REQUEST)

