from pyexpat import model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.certificadodisponibilidadpresupuestal.models import Certificadodisponibilidadpresupuestal
from apps.certificadodisponibilidadpresupuestal.api.serializers import CertificadodisponibilidadpresupuestalSerializers
from apps.periodo.models import Periodo
from apps.institucioneducativa.models import Institucioneducativa
from apps.consecutivo.api.api import consultarconsecutivo
from apps.consecutivo.api.api import actualizarconsecutivo
from django.db.models.deletion import RestrictedError
from apps.registropresupuestal.models import Registropresupuestal
from django.db.models import Count,Sum
from apps.solicitudpresupuestalcabecera.models import Solicitudpresupuestalcabecera

@api_view(['GET','POST'])
def certificadodisponibilidadpresupuestal_api_view(request):  
     
    if request.method =='GET':
        certificadodisponibilidadpresupuestal = buscar_cdp_all(request)
        certificadodisponibilidadpresupuestal =  CertificadodisponibilidadpresupuestalSerializers(certificadodisponibilidadpresupuestal, many = True)
        return Response(certificadodisponibilidadpresupuestal.data,status = status.HTTP_200_OK)
    elif request.method =='POST':
        institucioneducativa = Institucioneducativa()
        
        consecutivo = 0
        consecutivosolicitud = 0
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
                return Response("falta el nodo codigo para institucion educativa",status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response("falta el nodo institucioneducativaid",status = status.HTTP_400_BAD_REQUEST) 

        if 'solicitudpresupuestalcabeceraid' in request.data.keys():
            solicitudpresupuestalcabeceraid = request.data.pop('solicitudpresupuestalcabeceraid')
            if 'consecutivo' in solicitudpresupuestalcabeceraid.keys():
                solicitudpresupuestalcabecera = Solicitudpresupuestalcabecera.objects.filter(institucioneducativaid = institucioneducativa.id, consecutivo = solicitudpresupuestalcabeceraid['consecutivo']).first() 
                if solicitudpresupuestalcabecera:
                    request.data.update({"solicitudpresupuestalcabeceraid": solicitudpresupuestalcabecera.id})
                else:
                    return Response("solicitud presupuestal ingresada no existe",status = status.HTTP_400_BAD_REQUEST)                     
            else:
                return Response("falta el nodo consecutivo para consultar solicitud presupuestal",status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response("falta el nodo solicitudpresupuestalcabeceraid",status = status.HTTP_400_BAD_REQUEST) 


        consecutivo = consultarconsecutivo(4,institucioneducativa.id)
        request.data['consecutivo'] = consecutivo
        
        certificadodisponibilidadpresupuestal_Serializers = CertificadodisponibilidadpresupuestalSerializers(data = request.data)

        if certificadodisponibilidadpresupuestal_Serializers.is_valid(): 
            #return Response('guradando documento',status = status.HTTP_201_CREATED) 
            certificadodisponibilidadpresupuestal_Serializers.save()
            actualizarconsecutivo(4,institucioneducativa.id,consecutivo)
            return Response(certificadodisponibilidadpresupuestal_Serializers.data,status = status.HTTP_201_CREATED)        
        return Response(certificadodisponibilidadpresupuestal_Serializers.errors,status = status.HTTP_400_BAD_REQUEST) 

@api_view(['GET','DELETE'])
def certificadodisponibilidadpresupuestal_consecutivo_api_view(request): 
    certificadodisponibilidadpresupuestal = buscar_cdp_consecutivo(request) 
    if certificadodisponibilidadpresupuestal:
        if request.method =='GET': 
            certificadodisponibilidadpresupuestal_serializers = CertificadodisponibilidadpresupuestalSerializers(certificadodisponibilidadpresupuestal)
            return Response(certificadodisponibilidadpresupuestal_serializers.data,status = status.HTTP_200_OK)
        elif request.method == 'DELETE':
            if certificadodisponibilidadpresupuestal.estado =='Procesado':
                certificadodisponibilidadpresupuestal.estado ='Anulado'
                certificadodisponibilidadpresupuestal.save()
                return Response('Documento Anulado Correctamente',status = status.HTTP_200_OK)
                #try:
                #    certificadodisponibilidadpresupuestal.delete()
                #    return Response('Documento Eliminado Correctamente',status = status.HTTP_200_OK)
                #except RestrictedError:
                #    return Response('CDP no puede ser eliminado esta asociado a un Registro Presupuestal',status = status.HTTP_400_BAD_REQUEST)            
            return Response('CDP no puede ser eliminado en este Estado',status = status.HTTP_400_BAD_REQUEST)
    return Response('Documento no exite',status = status.HTTP_400_BAD_REQUEST) 
        

def buscar_cdp_all(request):
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
        
    
    certificadodisponibilidadpresupuestal = Certificadodisponibilidadpresupuestal.objects.filter(institucioneducativaid = institucioneducativaid, fecha__year = codigoperiodo).all()
    return certificadodisponibilidadpresupuestal

def buscar_cdp_consecutivo(request):
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
    
    certificadodisponibilidadpresupuestal = Certificadodisponibilidadpresupuestal.objects.filter(institucioneducativaid = institucioneducativaid, consecutivo = consecutivo).first()
    return certificadodisponibilidadpresupuestal

def saldocdp_por_rp(cdpid):
    totalcdp=0
    totalrp=0
    saldo = 0
    cdp = Certificadodisponibilidadpresupuestal.objects.filter(id=cdpid).first()
    if cdp:
        totalcdp = cdp.valor
        rp = Registropresupuestal.objects.filter(certificadodisponibilidadpresupuestalid = cdp.id).values('certificadodisponibilidadpresupuestalid').annotate(total=Sum('valor'))
        if rp:
            totalrp = rp[0]['total']

    saldo = totalcdp - totalrp
    return saldo

def saldocdp_por_rp_consecutivo(institucioneducativaid,consecutivo):
    saldo = 0
    cdp = Certificadodisponibilidadpresupuestal.objects.filter(institucioneducativaid=institucioneducativaid,consecutivo=consecutivo).first()
    if cdp:
        saldo = saldocdp_por_rp(cdp.id)
    
    return saldo

@api_view(['GET'])
def cdp_saldopor_rp_api_view(request):  
    parametros = dict(request.query_params)
    if request.method =='GET':
        codigoinstitucioneducativa = ""
        institucioneducativa_parametros = ""
        consecutivo = 0

        if 'consecutivo' in parametros.keys():
            consecutivo = parametros["consecutivo"][0]

        if 'codigoinstitucioneducativa' in parametros.keys():
            codigoinstitucioneducativa = str(parametros["codigoinstitucioneducativa"][0])
            codigoinstitucioneducativa = codigoinstitucioneducativa.upper() 
            
            institucioneducativa_parametros = Institucioneducativa.objects.filter(codigo =codigoinstitucioneducativa).first()
            if institucioneducativa_parametros:   
                
                return Response(saldocdp_por_rp_consecutivo(institucioneducativa_parametros.id,consecutivo),status = status.HTTP_200_OK)
            else:
                return Response('institucion educativa no existe',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('institucion educativa no existe',status = status.HTTP_400_BAD_REQUEST)

