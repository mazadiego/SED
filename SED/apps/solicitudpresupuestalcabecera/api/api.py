from operator import truediv
from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apps.solicitudpresupuestalcabecera.models import Solicitudpresupuestalcabecera
from apps.solicitudpresupuestalcabecera.api.serializers import SolicitudpresupuestalcabeceraSerializers
from apps.institucioneducativa.models import Institucioneducativa
from apps.personalplanta.models import Personalplanta
from apps.periodo.models import Periodo
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.consecutivo.api.api import consultarconsecutivo
from apps.consecutivo.api.api import actualizarconsecutivo
from django.db.models.deletion import RestrictedError
from apps.solicitudpresupuestaldetalle.models import Solicitudpresupuestaldetalle
from apps.certificadodisponibilidadpresupuestal.models import Certificadodisponibilidadpresupuestal
from django.db.models import Count,Sum

@api_view(['GET','POST'])
def solicitudpresupuestalcabecera_api_view(request): 
    if request.method =='GET':
        solicitudpresupuestal = buscarsolicitudpresupuestal(request)
        solicitudpresupuestal_serializers =  SolicitudpresupuestalcabeceraSerializers(solicitudpresupuestal, many = True)
        return Response(solicitudpresupuestal_serializers.data,status = status.HTTP_200_OK)
        
    elif request.method =='POST':
        institucioneducativa = Institucioneducativa()
        personalplantasolicitante =  Personalplanta()
        personalplantasolicitado =Personalplanta() 
        consecutivo = 0

        if 'estado' in request.data.keys():
            request.data['estado'] = 'Procesado'

        if 'institucioneducativaid' in request.data.keys():
            institucioneducativaid = request.data.pop('institucioneducativaid')
            if 'codigo' in institucioneducativaid.keys():
                institucioneducativa = Institucioneducativa.objects.filter(codigo = institucioneducativaid['codigo']).first() 
                if institucioneducativa:
                    request.data.update({"institucioneducativaid": institucioneducativa.id})
                else:
                    return Response("institucion educativa ingresada no existe",status = status.HTTP_400_BAD_REQUEST)                     
            else:
                return Response("falta el nodo codigo para tipo institucion educativa",status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response("falta el nodo institucioneducativaid",status = status.HTTP_400_BAD_REQUEST)   

        

        if 'personalplantaidsolicitante' in request.data.keys():
            personalplantaidsolicitante = request.data.pop('personalplantaidsolicitante')
            if 'codigo' in personalplantaidsolicitante.keys():
                personalplantasolicitante = Personalplanta.objects.filter(codigo = personalplantaidsolicitante['codigo']).first()
                if personalplantasolicitante:
                    request.data.update({"personalplantaidsolicitante": personalplantasolicitante.id})
                else:
                    return Response("personal planta no existe",status = status.HTTP_400_BAD_REQUEST)            
            else:
                return Response("falta el nodo codigo para consultar personal solicitante",status = status.HTTP_400_BAD_REQUEST)       
        else:
            return Response("falta el nodo personalplantaidsolicitante",status = status.HTTP_400_BAD_REQUEST)   

        if 'personalplantaidsolicitado' in request.data.keys():
            personalplantaidsolicitado = request.data.pop('personalplantaidsolicitado')
            if 'codigo' in personalplantaidsolicitado.keys():
                personalplantasolicitado = Personalplanta.objects.filter(codigo = personalplantaidsolicitado['codigo']).first()
                if personalplantasolicitado:
                    request.data.update({"personalplantaidsolicitado": personalplantasolicitado.id})
                else:
                    return Response("personal planta no existe",status = status.HTTP_400_BAD_REQUEST)            
            else:
                return Response("falta el nodo codigo para consultar personal solicitado",status = status.HTTP_400_BAD_REQUEST)       
        else:
            return Response("falta el nodo personalplantaidsolicitado",status = status.HTTP_400_BAD_REQUEST)   

                
        consecutivo = consultarconsecutivo(3,institucioneducativa.id)
        request.data['consecutivo'] = consecutivo

        solicitudpresupuestal_serializers =  SolicitudpresupuestalcabeceraSerializers(data = request.data)
        
        if solicitudpresupuestal_serializers.is_valid():        
            solicitudpresupuestal_serializers.save()
            actualizarconsecutivo(3,institucioneducativa.id,consecutivo)
            return Response(solicitudpresupuestal_serializers.data,status = status.HTTP_201_CREATED)        
        return Response(solicitudpresupuestal_serializers.errors,status = status.HTTP_400_BAD_REQUEST)  

@api_view(['GET','DELETE'])
def solicitudpresupuestal_consecutivo_api_view(request): 
    solicitudpresupuestal = buscarsolicitudpresupuestalconsecutivo(request) 
    if solicitudpresupuestal:
        if request.method =='GET': 
            solicitudpresupuestal_serializers = SolicitudpresupuestalcabeceraSerializers(solicitudpresupuestal)
            return Response(solicitudpresupuestal_serializers.data,status = status.HTTP_200_OK)
        elif request.method == 'DELETE':            
            if Certificadodisponibilidadpresupuestal.objects.filter(solicitudpresupuestalcabeceraid = solicitudpresupuestal.id, estado = 'Procesado').count() == 0:
                if solicitudpresupuestal.estado =='Procesado':                    
                    solicitudpresupuestal.estado ='Anulado' 
                    solicitudpresupuestal.save()
                    return Response('Documento Anulado Correctamente',status = status.HTTP_200_OK)                      
                return Response('Ingreso presupuestal no puede ser anulado en este Estado',status = status.HTTP_400_BAD_REQUEST)  
            return Response('Solicitud presupuestal no puede ser Anulada documento relacionado a un CDP',status = status.HTTP_400_BAD_REQUEST)          
    return Response('Documento no exite',status = status.HTTP_400_BAD_REQUEST)      
          
def buscarsolicitudpresupuestal(request):
    parametros = dict(request.query_params)
    codigoperiodo = 0
    codigoinstitucioneducativa = ""
    institucioneducativa_parametros = ""    

    periodo = Periodo.objects.filter(activo = True).first()

    if periodo:
        codigoperiodo = periodo.codigo
    
    
    if 'codigoinstitucioneducativa' in parametros.keys():
        codigoinstitucioneducativa = str(parametros["codigoinstitucioneducativa"][0])
        codigoinstitucioneducativa = codigoinstitucioneducativa.upper() 
        
        institucioneducativa_parametros = Institucioneducativa.objects.filter(codigo =codigoinstitucioneducativa).first()
        
        if institucioneducativa_parametros:            
            institucioneducativa_parametros_serializer = InstitucioneducativaSerializer(institucioneducativa_parametros)
            institucioneducativa_parametros = dict(institucioneducativa_parametros_serializer.data)
        else:
            institucioneducativa_parametros = dict({"id":0})
    else:
        institucioneducativa_parametros = dict({"id":0})
    
    solicitudpresupuestal = Solicitudpresupuestalcabecera.objects.filter(institucioneducativaid = institucioneducativa_parametros['id'], fecha__year = codigoperiodo).all()
    return solicitudpresupuestal

def buscarsolicitudpresupuestalconsecutivo(request):
    parametros = dict(request.query_params)
    consecutivo = 0
    codigoinstitucioneducativa = ""
    institucioneducativa_parametros = ""  

    if 'consecutivo' in parametros.keys():
        consecutivo = parametros["consecutivo"][0]
    
    
    if 'codigoinstitucioneducativa' in parametros.keys():
        codigoinstitucioneducativa = str(parametros["codigoinstitucioneducativa"][0])
        codigoinstitucioneducativa = codigoinstitucioneducativa.upper() 
        
        institucioneducativa_parametros = Institucioneducativa.objects.filter(codigo =codigoinstitucioneducativa).first()
        
        if institucioneducativa_parametros:            
            institucioneducativa_parametros_serializer = InstitucioneducativaSerializer(institucioneducativa_parametros)
            institucioneducativa_parametros = dict(institucioneducativa_parametros_serializer.data)
        else:
            institucioneducativa_parametros = dict({"id":0})
    else:
        institucioneducativa_parametros = dict({"id":0})
    
    solicitudpresupuestal = Solicitudpresupuestalcabecera.objects.filter(institucioneducativaid = institucioneducativa_parametros['id'], consecutivo = consecutivo).first()
    return solicitudpresupuestal

def buscarsolicitudpresupuestalconsecutivo_dict(parametros):
 
    consecutivo = 0
    codigoinstitucioneducativa = ""
    institucioneducativa_parametros = 0 

    if 'consecutivo' in parametros.keys():
        consecutivo = parametros["consecutivo"]


    if 'codigoinstitucioneducativa' in parametros.keys():
        codigoinstitucioneducativa = str(parametros["codigoinstitucioneducativa"])
        codigoinstitucioneducativa = codigoinstitucioneducativa.upper()     
        institucioneducativa = Institucioneducativa.objects.filter(codigo =codigoinstitucioneducativa).first()        
        if institucioneducativa:            
            institucioneducativa_parametros = institucioneducativa.id
    
    solicitudpresupuestal = Solicitudpresupuestalcabecera.objects.filter(institucioneducativaid = institucioneducativa_parametros, consecutivo = consecutivo).first()
    return solicitudpresupuestal

def saldosolicitud_por_cdp(solicitudpresupuestal):
    totalsolicitud=0
    saldo = 0
    totalcdp = 0

    solicitudpresupuestaldetalle = Solicitudpresupuestaldetalle.objects.filter(solicitudpresupuestalcabeceraid = solicitudpresupuestal.id).values('solicitudpresupuestalcabeceraid').annotate(total = Sum('valor'))
    if solicitudpresupuestaldetalle :
        totalsolicitud = solicitudpresupuestaldetalle[0]['total']

    cdp = Certificadodisponibilidadpresupuestal.objects.filter(solicitudpresupuestalcabeceraid = solicitudpresupuestal.id, estado = 'Procesado').values('solicitudpresupuestalcabeceraid').annotate(total = Sum('valor'))
    
    if cdp:
        totalcdp = cdp[0]['total']
    saldo = totalsolicitud - totalcdp

    return saldo

@api_view(['GET'])
def saldosolicitud_por_cdp_api_view(request):  
    parametros = dict(request.query_params)
    if request.method =='GET':
        codigoinstitucioneducativa = ""
        institucioneducativa = Institucioneducativa()
        consecutivo = 0

        if 'consecutivo' in parametros.keys():
            consecutivo = parametros["consecutivo"][0]

        if 'codigoinstitucioneducativa' in parametros.keys():
            codigoinstitucioneducativa = str(parametros["codigoinstitucioneducativa"][0])
            codigoinstitucioneducativa = codigoinstitucioneducativa.upper() 
            
            institucioneducativa = Institucioneducativa.objects.filter(codigo =codigoinstitucioneducativa).first()
            if institucioneducativa: 
                solicitudpresupuestal = Solicitudpresupuestalcabecera.objects.filter(institucioneducativaid = institucioneducativa.id, consecutivo = consecutivo ).first()
                if solicitudpresupuestal:
                    return Response(saldosolicitud_por_cdp(solicitudpresupuestal),status = status.HTTP_200_OK)
                else:
                    return Response('Documento solicitud no existe',status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response('institucion educativa no existe',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('institucion educativa no existe',status = status.HTTP_400_BAD_REQUEST)
