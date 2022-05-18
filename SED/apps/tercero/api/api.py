from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.tercero.models import Tercero
from apps.tercero.api.serializers import TerceroSerializer
from apps.tipoidentificacion.models import Tipoidentificacion
from apps.tipoidentificacion.api.serializers import TipoidentificacionSerializer
from django.db.models.deletion import RestrictedError
from django.db.utils import IntegrityError


@api_view(['GET','POST'])
def tercero_api_view(request):    
    if request.method =='GET':
        tercero = Tercero.objects.all()
        tercero_serializers = TerceroSerializer(tercero, many = True)
        return Response(tercero_serializers.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        data = request.data  
        if 'tipoidentificacionid' in data.keys():
            tipoidentificacionid = data.pop('tipoidentificacionid')
            if 'codigo' in tipoidentificacionid.keys():
                tipoidentificacion = Tipoidentificacion.objects.filter(codigo = tipoidentificacionid['codigo']).first() 
                if tipoidentificacion:
                    tipoidentificacionid_serializer = TipoidentificacionSerializer(tipoidentificacion)
                    tipoidentificacionid = dict(tipoidentificacionid_serializer.data)
                    data.update({"tipoidentificacionid": tipoidentificacionid['id'] })
                    tercero_serializers = TerceroSerializer(data = request.data)            
                    
                    if tercero_serializers.is_valid():
                        try:
                            tercero_serializers.save()
                            return Response(tercero_serializers.data,status = status.HTTP_201_CREATED)
                        except IntegrityError:
                            return Response('ya existe un tercero con el tipo de identificacion ingresado en el sistema',status = status.HTTP_400_BAD_REQUEST)
                    return Response(tercero_serializers.errors, status = status.HTTP_400_BAD_REQUEST)
                return Response('tipo identificacion ingresada no existe',status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo codigo para tipo identificacion',status = status.HTTP_400_BAD_REQUEST) 
        return Response('falta el nodo tipoidentificacionid',status = status.HTTP_400_BAD_REQUEST) 

@api_view(['GET','PUT','DELETE'])
def tercero_details_api_view(request, codigo = None):    
    
    tercero = Tercero.objects.filter(codigo=codigo).first()   

    if tercero:
        if request.method == 'GET':            
            tercero_serializers = TerceroSerializer(tercero)
            return Response(tercero_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT':
            data = request.data
            if 'codigo' in data.keys():
                data['codigo'] = codigo 
                if 'tipoidentificacionid' in data.keys():        
                    tipoidentificacionid = data.pop('tipoidentificacionid')
                    if 'codigo' in tipoidentificacionid.keys():
                        tipoidentificacion = Tipoidentificacion.objects.filter(codigo = tipoidentificacionid['codigo']).first() 
                        if tipoidentificacion:
                            tipoidentificacionid_serializer = TipoidentificacionSerializer(tipoidentificacion)
                            tipoidentificacionid = dict(tipoidentificacionid_serializer.data)
                            data.update({"tipoidentificacionid": tipoidentificacionid['id'] })  
                            
                            tercero_serializers = TerceroSerializer(tercero,data = request.data)       
                            
                            if tercero_serializers.is_valid():
                                try:
                                    tercero_serializers.save()
                                    return Response(tercero_serializers.data,status = status.HTTP_200_OK)
                                except IntegrityError:
                                    return Response('ya existe un tercero con el tipo de identificacion ingresado en el sistema',status = status.HTTP_400_BAD_REQUEST)
                            return Response(tercero_serializers.errors,status = status.HTTP_400_BAD_REQUEST)
                        return Response('tipo identificacion no Existe',status = status.HTTP_400_BAD_REQUEST)
                    return Response('Falta el nodo codigo para tipo identificacion',status = status.HTTP_400_BAD_REQUEST) 
                return Response('Falta el nodo tipoidentificacionid',status = status.HTTP_400_BAD_REQUEST) 
            return Response('Falta el nodo codigo',status = status.HTTP_400_BAD_REQUEST) 
        elif request.method == 'DELETE':
            try:
                tercero.delete()
                return Response('Eliminado Correctamente',status = status.HTTP_200_OK)
            except RestrictedError:
                return Response('tercero no puede ser eliminar ya esta asociado a documentos del sistema',status = status.HTTP_400_BAD_REQUEST)
    return Response('tercero no Existe',status = status.HTTP_400_BAD_REQUEST)
