from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from apps.tipoidentificacion.models import Tipoidentificacion
from apps.tipoidentificacion.api.serializers import TipoidentificacionSerializer
from django.db.models.deletion import RestrictedError


@api_view(['GET','POST'])
def tipoidentificacion_api_view(request):

    if request.method =='GET':
        tipoidentificacion = Tipoidentificacion.objects.all()
        tipoidentificacion_serializer = TipoidentificacionSerializer (tipoidentificacion, many = True)
        return Response(tipoidentificacion_serializer.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        tipoidentificacion_serializer = TipoidentificacionSerializer(data = request.data)
        if tipoidentificacion_serializer.is_valid():
            tipoidentificacion_serializer.save()
            return Response(tipoidentificacion_serializer.data,status = status.HTTP_201_CREATED)
        return Response(tipoidentificacion_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def tipoidentificacion_details_api_view(request, codigo = None):
    
    tipoidentificacion = Tipoidentificacion.objects.filter(codigo=codigo).first()
    if tipoidentificacion:
        if request.method == 'GET':            
            tipoidentificacion_serializers = TipoidentificacionSerializer(tipoidentificacion)
            return Response(tipoidentificacion_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT': 
            if 'codigo' in request.data.keys(): 
                request.data['codigo'] = codigo          
                tipoidentificacion_serializers = TipoidentificacionSerializer(tipoidentificacion, data = request.data)            
                if tipoidentificacion_serializers.is_valid():
                    tipoidentificacion_serializers.save()
                    return Response(tipoidentificacion_serializers.data,status = status.HTTP_200_OK)
                return Response(tipoidentificacion_serializers.errors,status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo codigo',status = status.HTTP_400_BAD_REQUEST) 
        elif request.method == 'DELETE':
            try:
                tipoidentificacion.delete()
                return Response('Tipo identificacion eliminado Correctamente',status = status.HTTP_200_OK)
            except RestrictedError:
                return Response('Tipo identificacion no puede ser eliminado esta asociado a un tercero',status = status.HTTP_400_BAD_REQUEST)            
    return Response('Tipoi dentificacion no Existe',status = status.HTTP_400_BAD_REQUEST)
    

