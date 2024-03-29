from operator import truediv
from urllib import response
from django.apps import apps
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from apps.solicitudpresupuestalcabecera.models import Solicitudpresupuestalcabecera

from apps.solicitudpresupuestalcabecera.api.api import buscarsolicitudpresupuestalconsecutivo
from apps.solicitudpresupuestalcabecera.api.api import buscarsolicitudpresupuestalconsecutivo_dict
from apps.rubropresupuestal.models import Rubropresupuestal
from apps.rubropresupuestal.api.api import Rubropresupuestalserializers
from apps.solicitudpresupuestaldetalle.models import Solicitudpresupuestaldetalle
from apps.solicitudpresupuestaldetalle.api.serializers import SolicitudpresupuestaldetalleSerializers
from apps.rubropresupuestal.api.api import buscarrubropresupuestal_final
from apps.rubropresupuestal.api.api import saldorubroporproyeccion
from apps.institucioneducativa.models import Institucioneducativa
from apps.rubropresupuestal.api.api import buscar_rubro_cdp
from apps.fuenterecurso.models import Fuenterecurso
from apps.fuenterecurso.api.api import buscarfuenterecurso_final
from apps.certificadodisponibilidadpresupuestal.models import Certificadodisponibilidadpresupuestal

@api_view(['GET','POST'])
def solicitudpresupuestaldetalle_api_view(request):
    if request.method =='POST':
        solicitudpresupuestalcabecera = Solicitudpresupuestalcabecera()
        solicitudpresupuestalcabeceraid = ""
        if 'solicitudpresupuestalcabeceraid' in request.data.keys():
            solicitudpresupuestalcabeceraid = request.data.pop('solicitudpresupuestalcabeceraid')
            if 'consecutivo' in solicitudpresupuestalcabeceraid.keys() and 'codigoinstitucioneducativa' in solicitudpresupuestalcabeceraid.keys() :
                solicitudpresupuestalcabecera = buscarsolicitudpresupuestalconsecutivo_dict(solicitudpresupuestalcabeceraid)
                if solicitudpresupuestalcabecera:
                    request.data.update({"solicitudpresupuestalcabeceraid":solicitudpresupuestalcabecera.id})
                else:
                    return Response("documento No existe",status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response("falta el nodo consecutivo/codigoinstitucioneducativa consultar documento",status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("falta el nodo solicitudpresupuestalcabeceraid consultar documento",status = status.HTTP_400_BAD_REQUEST)   

        if 'rubropresupuestalid' in request.data.keys():
            rubropresupuestalid =  request.data.pop('rubropresupuestalid') 
            if 'codigo' in rubropresupuestalid.keys():
                rubropresupuestal = buscarrubropresupuestal_final(rubropresupuestalid)                
                if rubropresupuestal:
                    request.data.update({"rubropresupuestalid":rubropresupuestal.id})
                else:
                    return Response("rubro presupuestal no existe",status = status.HTTP_400_BAD_REQUEST)                             
            else:
                return Response("falta el nodo codigo para consultar rubro presupuestal",status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("falta el nodo rubropresupuestalid consultar rubro presupuestal",status = status.HTTP_400_BAD_REQUEST)  

        if 'fuenterecursoid' in request.data.keys():
            fuenterecursoid =  request.data.pop('fuenterecursoid') 
            if 'codigo' in fuenterecursoid.keys():
                fuenterecurso = buscarfuenterecurso_final(fuenterecursoid)                
                if fuenterecurso:
                    request.data.update({"fuenterecursoid":fuenterecurso.id})
                else:
                    return Response("fuente recurso no existe",status = status.HTTP_400_BAD_REQUEST)                             
            else:
                return Response("falta el nodo codigo para consultar fuente de recurso",status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("falta el nodo fuenterecursoid consultar fuente de recurso",status = status.HTTP_400_BAD_REQUEST) 

        
        solicitudpresupuestaldetalle_serializers = SolicitudpresupuestaldetalleSerializers(data=request.data)
        
        if solicitudpresupuestaldetalle_serializers.is_valid():
            solicitudpresupuestaldetalle_serializers.save()
            return Response(solicitudpresupuestaldetalle_serializers.data,status = status.HTTP_201_CREATED)
        return Response(solicitudpresupuestaldetalle_serializers.errors,status = status.HTTP_400_BAD_REQUEST)
        
    elif request.method =='GET':              
        solicitudpresupuestal = buscarsolicitudpresupuestalconsecutivo(request)
        if solicitudpresupuestal: 
            solicitudpresupuestaldetalle = Solicitudpresupuestaldetalle.objects.filter( solicitudpresupuestalcabeceraid = solicitudpresupuestal.id).all() 
            if solicitudpresupuestaldetalle:
                solicitudpresupuestaldetalle_serializers = SolicitudpresupuestaldetalleSerializers(solicitudpresupuestaldetalle, many = True)
                return Response(solicitudpresupuestaldetalle_serializers.data,status = status.HTTP_200_OK)
            return Response("No existe registro para los datos ingresados",status = status.HTTP_400_BAD_REQUEST)   
        return Response("No existe registro cabecera para los datos ingresados",status = status.HTTP_400_BAD_REQUEST) 

@api_view(['GET','DELETE'])
def solicitudpresupuestaldetalle_id_api_view(request, id = None):    
    solicitudpresupuestaldetalle = Solicitudpresupuestaldetalle.objects.filter(id= id).first()    
    if solicitudpresupuestaldetalle:
        if request.method =='GET':
            solicitudpresupuestaldetalle_serializers = SolicitudpresupuestaldetalleSerializers(solicitudpresupuestaldetalle)
            return Response(solicitudpresupuestaldetalle_serializers.data, status = status.HTTP_200_OK)
        elif request.method == 'DELETE':
            if solicitudpresupuestaldetalle.solicitudpresupuestalcabeceraid.estado == 'Procesado':                
                if Certificadodisponibilidadpresupuestal.objects.filter(solicitudpresupuestalcabeceraid = solicitudpresupuestaldetalle.solicitudpresupuestalcabeceraid.id, estado = 'Procesado').count() == 0:
                    solicitudpresupuestaldetalle.delete()
                    return Response('Eliminado Correctamente', status= status.HTTP_200_OK)
                return Response('No se puede se eliminado detalle documento relacionado a un CDP',status = status.HTTP_400_BAD_REQUEST)  
            return Response('No se puede se eliminado detalle con documento en este Estado',status = status.HTTP_400_BAD_REQUEST)  
    return Response('no Existe datos para el id seleccionado',status = status.HTTP_400_BAD_REQUEST)  

def buscarsolicitudpresupuestaldetalle(request,solicitudpresupuestalid):
    parametros = dict(request.query_params)
    
    codigorubropresupuestal = ""
    rubropresupuestal_parametros = ""

    if 'codigorubropresupuestal' in parametros.keys():
        codigorubropresupuestal = parametros['codigorubropresupuestal'][0]
        rubropresupuestal_parametros = Rubropresupuestal.objects.filter(codigo = codigorubropresupuestal).first()

        if rubropresupuestal_parametros:
            rubropresupuestal_parametros_serializers = Rubropresupuestalserializers(rubropresupuestal_parametros)
            rubropresupuestal_parametros = dict(rubropresupuestal_parametros_serializers.data)
        else:
            rubropresupuestal_parametros = dict({"id":0})
    else:
        rubropresupuestal_parametros = dict({"id":0})

    solicitudpresupuestaldetalle = Solicitudpresupuestaldetalle.objects.filter(solicitudpresupuestalcabeceraid = solicitudpresupuestalid,rubropresupuestalid= rubropresupuestal_parametros['id']).first()
    return solicitudpresupuestaldetalle

def validarsaldorubroporproyeccion(codigoinstitucioneducativa,rubropresupuestalid,valoractual):
    saldo = 0
    institucioneducativa = Institucioneducativa.objects.filter(codigo=codigoinstitucioneducativa).first()
    if institucioneducativa:
        saldo = saldorubroporproyeccion(institucioneducativa.id,rubropresupuestalid) - valoractual

    if saldo >=0:
        return True
    else:
        return False