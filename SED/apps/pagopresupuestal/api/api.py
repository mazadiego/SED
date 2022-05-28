from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.consecutivo.api.api import consultarconsecutivo
from apps.consecutivo.api.api import actualizarconsecutivo

from apps.pagopresupuestal.models import Pagopresupuestal
from apps.pagopresupuestal.api.serializers import PagopresupuestalSerializers
from apps.institucioneducativa.models import Institucioneducativa
from apps.obligacionpresupuestal.models import Obligacionpresupuestal
from apps.periodo.models import Periodo


@api_view(['GET','POST'])
def pagopresupuestal_api_view(request):

    if request.method =='GET':
        pagopresupuestal = buscar_pagopresupuestal_all(request)
        pagopresupuestal =  PagopresupuestalSerializers(pagopresupuestal, many = True)
        return Response(pagopresupuestal.data,status = status.HTTP_200_OK)

    if request.method =='POST':
        institucioneducativa = Institucioneducativa()
        
        opresu = Obligacionpresupuestal()
        consecutivo = 0
        consecutivoopresu = 0
        
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

        if 'obligacionpresupuestalid' in request.data.keys():
            obligacionpresupuestalid = request.data.pop('obligacionpresupuestalid')
            if 'consecutivo' in obligacionpresupuestalid.keys():
                consecutivoopresu = obligacionpresupuestalid['consecutivo']
                
                opresu = Obligacionpresupuestal.objects.filter(institucioneducativaid = institucioneducativa.id, consecutivo = consecutivoopresu).first() 
                if opresu:
                    request.data.update({"obligacionpresupuestalid": opresu.id})
                else:
                    return Response("Obligacion Presupuestal no existe",status = status.HTTP_400_BAD_REQUEST)                     
            else:
                return Response("falta el nodo consecutivo para consultar Obligacion presupuestal",status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response("falta el nodo obligacionpresupuestalid",status = status.HTTP_400_BAD_REQUEST) 

        consecutivo = consultarconsecutivo(7,institucioneducativa.id)
        request.data['consecutivo'] = consecutivo

        pagopresupuestal_serializers = PagopresupuestalSerializers(data=request.data)

        if pagopresupuestal_serializers.is_valid():
            pagopresupuestal_serializers.save()
            actualizarconsecutivo(7,institucioneducativa.id,consecutivo)
            return Response(pagopresupuestal_serializers.data,status = status.HTTP_201_CREATED)
        return Response(pagopresupuestal_serializers.errors,status = status.HTTP_400_BAD_REQUEST) 

@api_view(['GET','DELETE'])
def pagopresupuestal_consecutivo_api_view(request): 
    pagopresupuestal = buscar_pagopresu_consecutivo(request) 
    if pagopresupuestal:
        if request.method =='GET': 
            pagopresupuestal_serializers = PagopresupuestalSerializers(pagopresupuestal)
            return Response(pagopresupuestal_serializers.data,status = status.HTTP_200_OK)
        elif request.method == 'DELETE':          
            pagopresupuestal.delete()
            return Response('Documento Eliminado Correctamente',status = status.HTTP_200_OK)            
    return Response('Documento no exite',status = status.HTTP_400_BAD_REQUEST) 

def buscar_pagopresu_consecutivo(request):
    parametros = dict(request.query_params)
    consecutivo = 0
    codigoinstitucioneducativa = ""
    institucioneducativaid =0

    if 'consecutivo' in parametros.keys():
        consecutivo = parametros["consecutivo"][0]
    
    
    if 'codigoinstitucioneducativa' in parametros.keys():
        codigoinstitucioneducativa = str(parametros["codigoinstitucioneducativa"][0])
        codigoinstitucioneducativa = codigoinstitucioneducativa.upper() 
        
        institucioneducativa = Institucioneducativa.objects.filter(codigo =codigoinstitucioneducativa).first()
        if institucioneducativa:            
           institucioneducativaid = institucioneducativa.id
    
    pagopresupuestal = Pagopresupuestal.objects.filter(institucioneducativaid = institucioneducativaid, consecutivo = consecutivo).first()
    return pagopresupuestal

def buscar_pagopresupuestal_all(request):
    parametros = dict(request.query_params)
    codigoperiodo = 0
    codigoinstitucioneducativa = ""
    institucioneducativa = ""    
    institucioneducativaid =0
    periodo = Periodo.objects.filter(activo = True).first()

    if periodo:
        codigoperiodo = periodo.codigo
    
    
    if 'codigoinstitucioneducativa' in parametros.keys():
        codigoinstitucioneducativa = str(parametros["codigoinstitucioneducativa"][0])
        codigoinstitucioneducativa = codigoinstitucioneducativa.upper() 
        
        institucioneducativa = Institucioneducativa.objects.filter(codigo =codigoinstitucioneducativa).first()
        if institucioneducativa:            
           institucioneducativaid = institucioneducativa.id
        
    
    pagopresupuestal = Pagopresupuestal.objects.filter(institucioneducativaid = institucioneducativaid, fecha__year = codigoperiodo).all()
    return pagopresupuestal