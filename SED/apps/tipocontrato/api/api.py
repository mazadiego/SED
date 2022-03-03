from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from apps.tipocontrato.models import Tipocontrato
from apps.tipocontrato.api.serializers import TipocontratoSerializer
from django.db.models.deletion import RestrictedError


@api_view(['GET','POST'])
def tipocontrato_api_view(request):

    if request.method =='GET':
        tipocontrato = Tipocontrato.objects.all()
        tipocontrato_serializer = TipocontratoSerializer (tipocontrato, many = True)
        return Response(tipocontrato_serializer.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        tipocontrato_serializer = TipocontratoSerializer(data = request.data)
        if tipocontrato_serializer.is_valid():
            tipocontrato_serializer.save()
            return Response(tipocontrato_serializer.data,status = status.HTTP_201_CREATED)
        return Response(tipocontrato_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def tipocontrato_details_api_view(request, codigo = None):
    
    tipocontrato = Tipocontrato.objects.filter(codigo=codigo).first()
    if tipocontrato:
        if request.method == 'GET':            
            tipocontrato_serializers = TipocontratoSerializer(tipocontrato)
            return Response(tipocontrato_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT': 
            if 'codigo' in request.data.keys(): 
                request.data['codigo'] = codigo          
                tipocontrato_serializers = TipocontratoSerializer(tipocontrato, data = request.data)            
                if tipocontrato_serializers.is_valid():
                    tipocontrato_serializers.save()
                    return Response(tipocontrato_serializers.data,status = status.HTTP_200_OK)
                return Response(tipocontrato_serializers.errors,status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo codigo',status = status.HTTP_400_BAD_REQUEST) 
        elif request.method == 'DELETE':
            try:
                tipocontrato.delete()
                return Response('Tipo contrato eliminado Correctamente',status = status.HTTP_200_OK)
            except RestrictedError:
                return Response('Tipo contrato no puede ser eliminado esta asociado a un documento',status = status.HTTP_400_BAD_REQUEST)            
    return Response('Tipocontrato No Existe',status = status.HTTP_400_BAD_REQUEST)
    

