from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apps.registropresupuestal.models import Registropresupuestal
from apps.registropresupuestal.api.serializers import Registropresupuestalserializers
from apps.periodo.models import Periodo
from apps.institucioneducativa.models import Institucioneducativa
from apps.tercero.models import Tercero
from apps.tipoidentificacion.models import Tipoidentificacion
from apps.certificadodisponibilidadpresupuestal.models import Certificadodisponibilidadpresupuestal
from apps.obligacionpresupuestal.models import Obligacionpresupuestal
from django.db.models.deletion import RestrictedError
from django.db.models import Count,Sum
from apps.tipocontrato.models import Tipocontrato

from apps.consecutivo.api.api import consultarconsecutivo
from apps.consecutivo.api.api import actualizarconsecutivo

@api_view(['GET','POST'])
def registropresupuestal_api_view(request):  
     
    if request.method =='GET':
        registropresupuestal = buscar_registropresupuestal_all(request)
        registropresupuestal =  Registropresupuestalserializers(registropresupuestal, many = True)
        return Response(registropresupuestal.data,status = status.HTTP_200_OK)
    elif request.method =='POST':
        institucioneducativa = Institucioneducativa()
        tercero = Tercero()
        cdp = Certificadodisponibilidadpresupuestal()
        consecutivo = 0
        consecutivocdp = 0

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

        if 'terceroid' in request.data.keys():
            terceroid = request.data.pop('terceroid')
            if 'codigo' in terceroid.keys():  
                tercero = Tercero.objects.filter(codigo = terceroid['codigo']).first()
                if tercero:
                    request.data.update({"terceroid": tercero.id})
                else:
                    return Response("tercero no existe",status = status.HTTP_400_BAD_REQUEST)  
            else:
                return Response("falta el nodo codigo para consultar el tercero",status = status.HTTP_400_BAD_REQUEST)       
        else:
            return Response("falta el nodo terceroid",status = status.HTTP_400_BAD_REQUEST) 

        if 'certificadodisponibilidadpresupuestalid' in request.data.keys():
            certificadodisponibilidadpresupuestalid = request.data.pop('certificadodisponibilidadpresupuestalid')
            if 'consecutivo' in certificadodisponibilidadpresupuestalid.keys():
                consecutivocdp = certificadodisponibilidadpresupuestalid['consecutivo']                
                cdp = Certificadodisponibilidadpresupuestal.objects.filter(institucioneducativaid = institucioneducativa.id, consecutivo = consecutivocdp).first() 
                if cdp:
                    request.data.update({"certificadodisponibilidadpresupuestalid": cdp.id})
                else:
                    return Response("CDP no existe",status = status.HTTP_400_BAD_REQUEST)                     
            else:
                return Response("falta el nodo consecutivo para consultar CDP",status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response("falta el nodo certificadodisponibilidadpresupuestalid",status = status.HTTP_400_BAD_REQUEST) 

        if 'tipocontratoid' in request.data.keys():
            tipocontratoid = request.data.pop('tipocontratoid')
            if 'codigo' in tipocontratoid.keys():                              
                tipocontrato = Tipocontrato.objects.filter(codigo = tipocontratoid['codigo']).first() 
                if tipocontrato:
                    request.data.update({"tipocontratoid": tipocontrato.id})
                else:
                    return Response("Tipo contrato no existe",status = status.HTTP_400_BAD_REQUEST)                     
            else:
                return Response("falta el nodo codigo para consultar tipo contrato",status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response("falta el nodo tipocontratoid",status = status.HTTP_400_BAD_REQUEST) 

        consecutivo = consultarconsecutivo(5,institucioneducativa.id)
        request.data['consecutivo'] = consecutivo
        
        registropresupuestal_Serializers = Registropresupuestalserializers(data = request.data)

        if registropresupuestal_Serializers.is_valid(): 
            registropresupuestal_Serializers.save()
            actualizarconsecutivo(5,institucioneducativa.id,consecutivo)
            return Response(registropresupuestal_Serializers.data,status = status.HTTP_201_CREATED)        
        return Response(registropresupuestal_Serializers.errors,status = status.HTTP_400_BAD_REQUEST) 
@api_view(['GET','DELETE'])
def registropresupuestal_consecutivo_api_view(request): 
    registropresupuestal = buscar_rp_consecutivo(request) 
    if registropresupuestal:
        if request.method =='GET': 
            registropresupuestal_serializers = Registropresupuestalserializers(registropresupuestal)
            return Response(registropresupuestal_serializers.data,status = status.HTTP_200_OK)
        elif request.method == 'DELETE': 
            if Obligacionpresupuestal.objects.filter(registropresupuestalid = registropresupuestal.id, estado ='Procesado').count() == 0:
                if registropresupuestal.estado == 'Procesado': 
                    registropresupuestal.estado = 'Anulado'          
                    registropresupuestal.save()
                    return Response('Documento Anulado Correctamente',status = status.HTTP_200_OK)                    
                return Response('RP no puede ser eliminado en este Estado',status = status.HTTP_400_BAD_REQUEST)
            return Response('RP no puede ser eliminado esta asociado a un Obligacion Presupuestal',status = status.HTTP_400_BAD_REQUEST)            
            
    return Response('Documento no exite',status = status.HTTP_400_BAD_REQUEST) 

def buscar_rp_consecutivo(request):
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
    
    registropresupuestal = Registropresupuestal.objects.filter(institucioneducativaid = institucioneducativaid, consecutivo = consecutivo).first()
    return registropresupuestal

def buscar_registropresupuestal_all(request):
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
        
    
    registropresupuestal = Registropresupuestal.objects.filter(institucioneducativaid = institucioneducativaid, fecha__year = codigoperiodo).all()
    return registropresupuestal

def saldo_rp_por_op(rpid):
    totalrp=0
    totalop=0
    saldo = 0
    rp = Registropresupuestal.objects.filter(id=rpid).first()
    if rp:
        totalrp = rp.valor
        op = Obligacionpresupuestal.objects.filter(registropresupuestalid = rp.id, estado ='Procesado').values('registropresupuestalid').annotate(total=Sum('valor'))
        if op:
            totalop = op[0]['total']

    saldo = totalrp - totalop
    return saldo

def saldo_rp_por_op_consecutivo(institucioneducativaid,consecutivo):
    saldo = 0
    rp = Registropresupuestal.objects.filter(institucioneducativaid=institucioneducativaid,consecutivo=consecutivo).first()
    if rp:
        saldo = saldo_rp_por_op(rp.id)
    
    return saldo

@api_view(['GET'])
def rp_saldopor_op_api_view(request):  
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
                
                return Response(saldo_rp_por_op_consecutivo(institucioneducativa_parametros.id,consecutivo),status = status.HTTP_200_OK)
            else:
                return Response('institucion educativa no existe',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('institucion educativa no existe',status = status.HTTP_400_BAD_REQUEST)
