from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.personalplanta.models import Personalplanta
from apps.personalplanta.api.serializers import Personalplantaserializers
from apps.institucioneducativa.models import Institucioneducativa
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from django.db.models.deletion import RestrictedError


@api_view(['GET','POST'])
def personalplanta_api_view(request):

    if request.method =='GET':
        personalplanta = Personalplanta.objects.all()
        personalplanta_serializers = Personalplantaserializers(personalplanta, many = True)
        return Response(personalplanta_serializers.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        data = request.data  
        if 'institucioneducativaid' in data.keys():
            institucioneducativaid = data.pop('institucioneducativaid')
            if 'codigo' in institucioneducativaid.keys():
                institucioneducativa = Institucioneducativa.objects.filter(codigo = institucioneducativaid['codigo']).first() 
                if institucioneducativa:
                    institucioneducativaid_serializer = InstitucioneducativaSerializer(institucioneducativa)
                    institucioneducativaid = dict(institucioneducativaid_serializer.data)
                    data.update({"institucioneducativaid": institucioneducativaid['id'] })
                    personalplanta_serializers = Personalplantaserializers(data = request.data)            
                    
                    if personalplanta_serializers.is_valid():
                        personalplanta_serializers.save()
                        return Response(personalplanta_serializers.data,status = status.HTTP_201_CREATED)
                    return Response(personalplanta_serializers.errors, status = status.HTTP_400_BAD_REQUEST)
                return Response('institucion educativa ingresada no existe',status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo codigo para institucion educativa',status = status.HTTP_400_BAD_REQUEST) 
        return Response('falta el nodo institucioneducativaid',status = status.HTTP_400_BAD_REQUEST) 

@api_view(['GET','PUT','DELETE'])
def personalplanta_details_api_view(request, codigo = None):
    personalplanta = Personalplanta.objects.filter(codigo=codigo).first()

    if personalplanta:
        if request.method == 'GET':            
            personalplanta_serializers = Personalplantaserializers(personalplanta)
            return Response(personalplanta_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT':
            data = request.data
            if 'codigo' in data.keys():
                data['codigo'] = codigo 
                if 'institucioneducativaid' in data.keys():        
                    institucioneducativaid = data.pop('institucioneducativaid')
                    if 'codigo' in institucioneducativaid.keys():
                        institucioneducativa = Institucioneducativa.objects.filter(codigo = institucioneducativaid['codigo']).first() 
                        if institucioneducativa:
                            institucioneducativaid_serializer = InstitucioneducativaSerializer(institucioneducativa)
                            institucioneducativaid = dict(institucioneducativaid_serializer.data)
                            data.update({"institucioneducativaid": institucioneducativaid['id'] })  
                            
                            personalplanta_serializers = Personalplantaserializers(personalplanta,data = request.data)       
                            
                            if personalplanta_serializers.is_valid():
                                personalplanta_serializers.save()
                                return Response(personalplanta_serializers.data,status = status.HTTP_200_OK)
                            return Response(personalplanta_serializers.errors,status = status.HTTP_400_BAD_REQUEST)
                        return Response('institucion educativa no Existe',status = status.HTTP_400_BAD_REQUEST)
                    return Response('Falta el nodo codigo para institucion educativa',status = status.HTTP_400_BAD_REQUEST) 
                return Response('Falta el nodo institucioneducativaid',status = status.HTTP_400_BAD_REQUEST) 
            return Response('Falta el nodo codigo',status = status.HTTP_400_BAD_REQUEST) 
        elif request.method == 'DELETE':
            try:
                personalplanta.delete()
                return Response('Eliminado Correctamente',status = status.HTTP_200_OK)
            except RestrictedError:
                return Response('personal planta no puede ser eliminar ya esta asociado a documento del sistema',status = status.HTTP_400_BAD_REQUEST)
    return Response('Personal Planta no Existe',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def personalplanta_institucioneducativa_details_api_view(request, codigo = None):
    institucioneducativa = Institucioneducativa.objects.filter(codigo=codigo).first()

    if institucioneducativa:
        institucioneducativa_serializer = InstitucioneducativaSerializer(institucioneducativa)
        institucioneducativaid = dict(institucioneducativa_serializer.data)
        personalplanta = Personalplanta.objects.filter(institucioneducativaid=institucioneducativaid['id']).all()
        
        if personalplanta:
            if request.method == 'GET':            
                personalplanta_serializers = Personalplantaserializers(personalplanta, many = True)
            return Response(personalplanta_serializers.data,status = status.HTTP_200_OK)
        return Response('no existe personal asociados a esta institucion educativa',status = status.HTTP_400_BAD_REQUEST)

    return Response('institucion educativa ingresada no existe',status = status.HTTP_400_BAD_REQUEST)

