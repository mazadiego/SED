from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.institucioneducativa.models import Institucioneducativa
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from django.db.models.deletion import RestrictedError
from apps.user.models import User


@api_view(['GET','POST'])
def institucioneducativa_api_view(request):

    if request.method =='GET':
        institucioneducativa = Institucioneducativa.objects.all()
        institucioneducativa_serializer = InstitucioneducativaSerializer (institucioneducativa, many = True)
        return Response(institucioneducativa_serializer.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        data = request.data  
        if 'usuarioid' in data.keys():
            usuarioid = data.pop('usuarioid')
            if 'username' in usuarioid.keys():
                usuario = User.objects.filter(username = usuarioid['username']).first() 
                if usuario:                    
                    data.update({"usuarioid": usuario.id })
                    institucioneducativa_serializer = InstitucioneducativaSerializer(data = request.data)            
                    
                    if institucioneducativa_serializer.is_valid():
                        institucioneducativa_serializer.save()
                        return Response(institucioneducativa_serializer.data,status = status.HTTP_201_CREATED)
                    return Response(institucioneducativa_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                return Response('Usuario Ingresado No Existe',status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo username para el usuario registrado',status = status.HTTP_400_BAD_REQUEST) 
        return Response('falta el nodo usuarioid',status = status.HTTP_400_BAD_REQUEST) 

@api_view(['GET','PUT','DELETE'])
def institucioneducativa_details_api_view(request, codigo = None):
    institucioneducativa = Institucioneducativa.objects.filter(codigo=codigo).first()

    if institucioneducativa:
        if request.method == 'GET':            
            institucioneducativa_serializers = InstitucioneducativaSerializer(institucioneducativa)
            return Response(institucioneducativa_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT':
            data = request.data
            if 'codigo' in data.keys():
                data['codigo'] = codigo 
                if 'usuarioid' in data.keys():        
                    usuarioid = data.pop('usuarioid')
                    if 'username' in usuarioid.keys():
                        usuario = User.objects.filter(username = usuarioid['username']).first()
                        if usuario:
                            data.update({"usuarioid": usuario.id })             
                            institucioneducativa_serializers = InstitucioneducativaSerializer(institucioneducativa, data = request.data)            
                            if institucioneducativa_serializers.is_valid():
                                institucioneducativa_serializers.save()
                                return Response(institucioneducativa_serializers.data,status = status.HTTP_200_OK)
                            return Response(institucioneducativa_serializers.errors,status = status.HTTP_400_BAD_REQUEST)
                        return Response('Usuario Ingresado No Existe',status = status.HTTP_400_BAD_REQUEST)
                    return Response('Falta el nodo username para el usuario registrado',status = status.HTTP_400_BAD_REQUEST) 
                return Response('Falta el nodo usuarioid',status = status.HTTP_400_BAD_REQUEST) 
            return Response('Falta el nodo codigo',status = status.HTTP_400_BAD_REQUEST) 
        elif request.method == 'DELETE':
            try:
                institucioneducativa.delete()
                return Response('Eliminado Correctamente',status = status.HTTP_200_OK)
            except RestrictedError:
                return Response('Institucion Educativa no puede ser eliminar ya esta asociado a documento o personal del sistema',status = status.HTTP_400_BAD_REQUEST)           
            
    return Response('Institucion educativa no Existe',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def institucioneducativa_usuario_details_api_view(request, username = None):
    usuario = User.objects.filter(username=username).first()
    if usuario:
        institucioneducativa = Institucioneducativa.objects.filter(usuarioid=usuario.id).first()
        
        if institucioneducativa:
            if request.method == 'GET':            
                institucioneducativa_serializers = InstitucioneducativaSerializer(institucioneducativa)
            return Response(institucioneducativa_serializers.data,status = status.HTTP_200_OK)
        return Response('usuario no tiene institucion educativa asignada',status = status.HTTP_400_BAD_REQUEST)

    return Response('Usuario Ingresado No Existe',status = status.HTTP_400_BAD_REQUEST)

