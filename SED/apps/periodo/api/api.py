from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from apps.periodo.models import Periodo
from apps.periodo.api.serializers import Periodoserializers 
from django.db.models.deletion import RestrictedError


@api_view(['GET','POST'])
def periodo_api_view(request):

    if request.method =='GET':
        periodo = Periodo.objects.all()
        periodo_serializer = Periodoserializers (periodo, many = True)
        return Response(periodo_serializer.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        periodo_serializer = Periodoserializers(data = request.data)
        if periodo_serializer.is_valid():
            periodo_serializer.save()
            return Response(periodo_serializer.data,status = status.HTTP_201_CREATED)
        return Response(periodo_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def periodo_details_api_view(request, codigo = None):
    
    objperiodo = Periodo.objects.filter(codigo=codigo).first()
    if objperiodo:
        if request.method == 'GET':            
            periodo_serializers = Periodoserializers(objperiodo)
            return Response(periodo_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT':             
            if 'codigo' in request.data.keys(): 
                request.data['codigo'] = codigo
                periodo_serializers = Periodoserializers(objperiodo, data = request.data)            
                if periodo_serializers.is_valid():
                    periodo_serializers.save()
                    return Response(periodo_serializers.data,status = status.HTTP_200_OK)
                return Response(periodo_serializers.errors,status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo codigo',status = status.HTTP_400_BAD_REQUEST) 
        elif request.method == 'DELETE':
            try:
                objperiodo.delete()
                return Response('periodo eliminado Correctamente',status = status.HTTP_200_OK)
            except RestrictedError:
                return Response('periodo no puede ser eliminado esta asociado a un documento',status = status.HTTP_400_BAD_REQUEST)            
    return Response('Periodo No Existe',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def periodos_activos_api_view(request):

    if request.method =='GET':
        periodo = Periodo.objects.filter(activo = True).all()
        periodo_serializer = Periodoserializers (periodo, many = True)
        return Response(periodo_serializer.data,status = status.HTTP_200_OK)
    

