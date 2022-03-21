from itertools import count
from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from apps.rubropresupuestal.models import Rubropresupuestal
from apps.rubropresupuestal.api.serializers import Rubropresupuestalserializers
from django.db.models.deletion import RestrictedError


@api_view(['GET','POST'])
def rubropresupuestal_api_view(request):

    if request.method =='GET':
        rubropresupuestal = Rubropresupuestal.objects.all()
        rubropresupuestal_serializer = Rubropresupuestalserializers (rubropresupuestal, many = True)
        return Response(rubropresupuestal_serializer.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        if 'idpadre' in request.data.keys():
            idpadre = request.data.pop('idpadre')
            if 'codigo' in idpadre.keys():
                rubropadre = Rubropresupuestal.objects.filter(codigo = idpadre['codigo']).first()
                if rubropadre:
                    idpadre_serializers = Rubropresupuestalserializers(rubropadre)
                    idpadre = dict(idpadre_serializers.data)
                    request.data.update({'idpadre':idpadre['id']})
                    rubropresupuestal_serializer = Rubropresupuestalserializers(data = request.data)
                    if rubropresupuestal_serializer.is_valid():
                        rubropresupuestal_serializer.save()
                        return Response(rubropresupuestal_serializer.data,status = status.HTTP_201_CREATED)
                    return Response(rubropresupuestal_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                return Response('rubro presupuestal padre ingresado no existe',status = status.HTTP_400_BAD_REQUEST)
            return Response('falta nodo codigo del rubro presupuestal padre',status = status.HTTP_400_BAD_REQUEST)
        else: 
            if Rubropresupuestal.objects.all().count()==0:          
                rubropresupuestal_serializer = Rubropresupuestalserializers(data = request.data)
                if rubropresupuestal_serializer.is_valid():
                    rubropresupuestal_serializer.save()
                    return Response(rubropresupuestal_serializer.data,status = status.HTTP_201_CREATED)
                return Response(rubropresupuestal_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response('solo puede exitir un rubro presupuetal de cabecera',status = status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','PUT','DELETE'])
def rubropresupuestal_details_api_view(request, codigo = None):
    
    rubropresupuestal = Rubropresupuestal.objects.filter(codigo=codigo).first()
    if rubropresupuestal:
        if request.method == 'GET':            
            rubropresupuestal_serializers = Rubropresupuestalserializers(rubropresupuestal)
            return Response(rubropresupuestal_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT':            
            if 'codigo' in request.data.keys(): 
                request.data['codigo'] = codigo          
                if 'idpadre' in request.data.keys():
                    idpadre = request.data.pop('idpadre')
                    if 'codigo' in idpadre.keys():
                        if codigo != idpadre['codigo']:
                            rubropadre = Rubropresupuestal.objects.filter(codigo = idpadre['codigo']).first()
                            if rubropadre:
                                idpadre_serializers = Rubropresupuestalserializers(rubropadre)
                                idpadre = dict(idpadre_serializers.data)
                                request.data.update({'idpadre':idpadre['id']})

                                rubropresupuestal_serializer = Rubropresupuestalserializers(rubropresupuestal,data = request.data)
                                if rubropresupuestal_serializer.is_valid():
                                    rubropresupuestal_serializer.save()
                                    return Response(rubropresupuestal_serializer.data,status = status.HTTP_201_CREATED)
                                return Response(rubropresupuestal_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                            return Response('rubro presupuestal padre ingresado no existe',status = status.HTTP_400_BAD_REQUEST)
                        return Response('rubro presupuestal padre ingresado no puede ser igual al codigo del rubro',status = status.HTTP_400_BAD_REQUEST)
                    return Response('falta nodo codigo del rubro presupuestal padre',status = status.HTTP_400_BAD_REQUEST)
                else:                    
                    rubropresupuestal_serializer = Rubropresupuestalserializers(rubropresupuestal,data = request.data)
                    if rubropresupuestal_serializer.is_valid():
                        rubropresupuestal_serializer.save()
                        return Response(rubropresupuestal_serializer.data,status = status.HTTP_201_CREATED)
                    return Response(rubropresupuestal_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo codigo',status = status.HTTP_400_BAD_REQUEST) 
        elif request.method == 'DELETE':
            rubropresupuestal_serializers = Rubropresupuestalserializers(rubropresupuestal)
            if Rubropresupuestal.objects.filter(idpadre = rubropresupuestal_serializers.data['id']).count() == 0:
                try:
                    rubropresupuestal.delete()
                    return Response('Rubro presupuestal eliminado Correctamente',status = status.HTTP_200_OK)
                except RestrictedError:
                    return Response('Rubro presupuestal no puede ser eliminado esta asociado a un documento',status = status.HTTP_400_BAD_REQUEST)
            return Response('Rubro presupuestal no puede ser eliminado esta asociado como padre a otro rubro',status = status.HTTP_400_BAD_REQUEST)            
    return Response('Rubro presupuestal No Existe',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def rubropresupuestal_final_api_view(request):

    if request.method =='GET':
        data = Rubropresupuestal.objects.all()        
        rubropresupuestal_serializer = Rubropresupuestalserializers(data, many=True)
        list_rubros = [rubro for rubro in rubropresupuestal_serializer.data if Rubropresupuestal.objects.filter(idpadre = rubro['id']).count() == 0]  
        return Response(list_rubros,status = status.HTTP_200_OK)

def buscarrubropresupuestal_final(data):
    rubropresupuestal = Rubropresupuestal.objects.filter(codigo = data['codigo']).first()
    if rubropresupuestal:
        if Rubropresupuestal.objects.filter(idpadre = rubropresupuestal.id).count()==0:
            return rubropresupuestal

        
    

      

