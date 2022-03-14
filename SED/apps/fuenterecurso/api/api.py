from itertools import count
from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from apps.fuenterecurso.models import Fuenterecurso
from apps.fuenterecurso.api.serializers import Fuenterecursoserializers
from django.db.models.deletion import RestrictedError


@api_view(['GET','POST'])
def fuenterecurso_api_view(request):

    if request.method =='GET':
        fuenterecurso = Fuenterecurso.objects.all()
        fuenterecurso_serializer = Fuenterecursoserializers (fuenterecurso, many = True)
        return Response(fuenterecurso_serializer.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        if 'idpadre' in request.data.keys():
            idpadre = request.data.pop('idpadre')
            if 'codigo' in idpadre.keys():
                fuentepadre = Fuenterecurso.objects.filter(codigo = idpadre['codigo']).first()
                if fuentepadre:
                    idpadre_serializers = Fuenterecursoserializers(fuentepadre)
                    idpadre = dict(idpadre_serializers.data)
                    request.data.update({'idpadre':idpadre['id']})

                    fuenterecurso_serializer = Fuenterecursoserializers(data = request.data)
                    if fuenterecurso_serializer.is_valid():
                        fuenterecurso_serializer.save()
                        return Response(fuenterecurso_serializer.data,status = status.HTTP_201_CREATED)
                    return Response(fuenterecurso_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                return Response('fuente recurso padre ingresado no existe',status = status.HTTP_400_BAD_REQUEST)
            return Response('falta nodo codigo de la fuente recurso padre',status = status.HTTP_400_BAD_REQUEST)
        else: 
            if Fuenterecurso.objects.all().count()==0:          
                fuenterecurso_serializer = Fuenterecursoserializers(data = request.data)
                if fuenterecurso_serializer.is_valid():
                    fuenterecurso_serializer.save()
                    return Response(fuenterecurso_serializer.data,status = status.HTTP_201_CREATED)
                return Response(fuenterecurso_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response('solo puede exitir una fuente de recuerso de cabecera',status = status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','PUT','DELETE'])
def fuenterecurso_details_api_view(request, codigo = None):
    
    fuenterecurso = Fuenterecurso.objects.filter(codigo=codigo).first()
    if fuenterecurso:
        if request.method == 'GET':            
            fuenterecurso_serializers = Fuenterecursoserializers(fuenterecurso)
            return Response(fuenterecurso_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT':            
            if 'codigo' in request.data.keys(): 
                request.data['codigo'] = codigo          
                if 'idpadre' in request.data.keys():
                    idpadre = request.data.pop('idpadre')
                    if 'codigo' in idpadre.keys():
                        fuentepadre = Fuenterecurso.objects.filter(codigo = idpadre['codigo']).first()
                        if fuentepadre:
                            idpadre_serializers = Fuenterecursoserializers(fuentepadre)
                            idpadre = dict(idpadre_serializers.data)
                            request.data.update({'idpadre':idpadre['id']})

                            fuenterecurso_serializer = Fuenterecursoserializers(fuenterecurso,data = request.data)
                            if fuenterecurso_serializer.is_valid():
                                fuenterecurso_serializer.save()
                                return Response(fuenterecurso_serializer.data,status = status.HTTP_201_CREATED)
                            return Response(fuenterecurso_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                        return Response('fuente recurso padre ingresado no existe',status = status.HTTP_400_BAD_REQUEST)
                    return Response('falta nodo codigo de la fuente recurso padre',status = status.HTTP_400_BAD_REQUEST)
                else:                    
                    fuenterecurso_serializer = Fuenterecursoserializers(fuenterecurso,data = request.data)
                    if fuenterecurso_serializer.is_valid():
                        fuenterecurso_serializer.save()
                        return Response(fuenterecurso_serializer.data,status = status.HTTP_201_CREATED)
                    return Response(fuenterecurso_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo codigo',status = status.HTTP_400_BAD_REQUEST) 
        elif request.method == 'DELETE':
            try:
                fuenterecurso.delete()
                return Response('fuente recurso eliminado Correctamente',status = status.HTTP_200_OK)
            except RestrictedError:
                return Response('fuente recurso no puede ser eliminado esta asociado a un documento',status = status.HTTP_400_BAD_REQUEST)            
    return Response('fuente recurso no existe',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def fuenterecurso_final_api_view(request):

    if request.method =='GET':
        data = Fuenterecurso.objects.all()        
        fuenterecurso_serializer = Fuenterecursoserializers(data, many=True)
        list_fuentes = [fuente for fuente in fuenterecurso_serializer.data if Fuenterecurso.objects.filter(idpadre = fuente['id']).count() == 0]  
        return Response(list_fuentes,status = status.HTTP_200_OK)

        
    

      

