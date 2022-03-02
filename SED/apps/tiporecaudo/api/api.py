from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from apps.tiporecaudo.models import Tiporecaudo
from apps.tiporecaudo.api.serializers import TiporecaudoSerializer
from django.db.models.deletion import RestrictedError


@api_view(['GET','POST'])
def tiporecaudo_api_view(request):

    if request.method =='GET':
        tiporecaudo = Tiporecaudo.objects.all()
        tiporecaudo_serializer = TiporecaudoSerializer (tiporecaudo, many = True)
        return Response(tiporecaudo_serializer.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        tiporecaudo_serializer = TiporecaudoSerializer(data = request.data)
        if tiporecaudo_serializer.is_valid():
            tiporecaudo_serializer.save()
            return Response(tiporecaudo_serializer.data,status = status.HTTP_201_CREATED)
        return Response(tiporecaudo_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def tiporecaudo_details_api_view(request, codigo = None):
    
    tiporecaudo = Tiporecaudo.objects.filter(codigo=codigo).first()
    if tiporecaudo:
        if request.method == 'GET':            
            tiporecaudo_serializers = TiporecaudoSerializer(tiporecaudo)
            return Response(tiporecaudo_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT': 
            if 'codigo' in request.data.keys(): 
                request.data['codigo'] = codigo          
                tiporecaudo_serializers = TiporecaudoSerializer(tiporecaudo, data = request.data)            
                if tiporecaudo_serializers.is_valid():
                    tiporecaudo_serializers.save()
                    return Response(tiporecaudo_serializers.data,status = status.HTTP_200_OK)
                return Response(tiporecaudo_serializers.errors,status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo codigo',status = status.HTTP_400_BAD_REQUEST) 
        elif request.method == 'DELETE':
            try:
                tiporecaudo.delete()
                return Response('Tipo recaudo eliminado Correctamente',status = status.HTTP_200_OK)
            except RestrictedError:
                return Response('Tipo recaudo no puede ser eliminado esta asociado a un documento',status = status.HTTP_400_BAD_REQUEST)            
    return Response('Tiporecaudo No Existe',status = status.HTTP_400_BAD_REQUEST)
    

