
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from apps.adjuntos.models import Adjuntos
from apps.adjuntos.api.serializers import AdjuntosSerializers,DescargarAdjuntosSerializers
from apps.institucioneducativa.models import Institucioneducativa


@api_view(['GET','POST'])
def adjuntos_api_view(request):

    if request.method =='GET':
        institucioneducativaid = 0
        codigoinstitucioneducativa = ""
        parametros = dict(request.query_params)

        if 'codigoinstitucioneducativa' in parametros.keys():
            codigoinstitucioneducativa = str(parametros["codigoinstitucioneducativa"][0])
            codigoinstitucioneducativa = codigoinstitucioneducativa.upper() 
        
        institucioneducativa = Institucioneducativa.objects.filter(codigo =codigoinstitucioneducativa).first()

        if institucioneducativa:            
           institucioneducativaid = institucioneducativa.id

        adjuntos = Adjuntos.objects.filter(institucioneducativaid = institucioneducativaid).all()

        if adjuntos:
            adjuntos_serializer = AdjuntosSerializers (adjuntos, many = True)       
            return Response(adjuntos_serializer.data,status = status.HTTP_200_OK)
        return Response("no existen datos para los parametros ingresados",status = status.HTTP_400_BAD_REQUEST)

    elif request.method =='POST':

        if 'institucioneducativaid' in request.data.keys():
            institucioneducativaid = request.data.pop('institucioneducativaid')
            if 'codigo' in institucioneducativaid.keys():
                institucioneducativa = Institucioneducativa.objects.filter(codigo = institucioneducativaid['codigo']).first() 
                if institucioneducativa:
                    request.data.update({"institucioneducativaid": institucioneducativa.id})
                else:
                    return Response("institucion educativa ingresada no existe",status = status.HTTP_400_BAD_REQUEST)                     
            else:
                return Response("falta el nodo codigo para institucion educativa",status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response("falta el nodo institucioneducativaid",status = status.HTTP_400_BAD_REQUEST) 

        adjuntos_serializer = AdjuntosSerializers(data = request.data)

        if adjuntos_serializer.is_valid():
            adjuntos_serializer.save()
            return Response(adjuntos_serializer.data,status = status.HTTP_200_OK)
        return Response(adjuntos_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
  
@api_view(['GET','DELETE'])
def adjuntos_api_id_view(request, id = None):

    adjuntos = Adjuntos.objects.filter(id = id).first()

    if adjuntos:
        if request.method =='GET':
            adjuntos_serializer = AdjuntosSerializers (adjuntos)       
            return Response(adjuntos_serializer.data,status = status.HTTP_200_OK)
        if request.method =='DELETE':
            adjuntos.archivobase64.delete(save=True)
            adjuntos.delete()
            return Response('archivo eliminado correctamente',status = status.HTTP_400_BAD_REQUEST)

    return Response('archivo no existen en base de datos',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def adjuntos_api_descargar_id_view(request, id = None):

    adjuntos = Adjuntos.objects.filter(id = id).first()

    if adjuntos:
        if request.method =='GET':
            adjuntos_serializer = DescargarAdjuntosSerializers (adjuntos)       
            return Response(adjuntos_serializer.data,status = status.HTTP_200_OK)
    return Response('archivo no existen en base de datos',status = status.HTTP_400_BAD_REQUEST)


    

