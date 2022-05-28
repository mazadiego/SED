from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.consecutivo.api.api import consultarconsecutivo
from apps.consecutivo.api.api import actualizarconsecutivo

from apps.obligacionpresupuestal.models import Obligacionpresupuestal
from apps.obligacionpresupuestal.api.serializers import ObligacionpresupuestalSerializers
from apps.institucioneducativa.models import Institucioneducativa
from apps.registropresupuestal.models import Registropresupuestal
from apps.periodo.models import Periodo
from django.db.models.deletion import RestrictedError
from django.db.models import Count,Sum
from apps.pagopresupuestal.models import Pagopresupuestal


@api_view(['GET','POST'])
def obligacionpresupuestal_api_view(request):

    if request.method =='GET':
        obligacionpresupuestal = buscar_obligacionpresupuestal_all(request)
        obligacionpresupuestal =  ObligacionpresupuestalSerializers(obligacionpresupuestal, many = True)
        return Response(obligacionpresupuestal.data,status = status.HTTP_200_OK)

    if request.method =='POST':
        institucioneducativa = Institucioneducativa()
        
        rp = Registropresupuestal()
        consecutivo = 0
        consecutivorp = 0
        
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

        if 'registropresupuestalid' in request.data.keys():
            registropresupuestalid = request.data.pop('registropresupuestalid')
            if 'consecutivo' in registropresupuestalid.keys():
                consecutivorp = registropresupuestalid['consecutivo']
                
                rp = Registropresupuestal.objects.filter(institucioneducativaid = institucioneducativa.id, consecutivo = consecutivorp).first() 
                if rp:
                    request.data.update({"registropresupuestalid": rp.id})
                else:
                    return Response("Registro Presupuestal no existe",status = status.HTTP_400_BAD_REQUEST)                     
            else:
                return Response("falta el nodo consecutivo para consultar Registro presupuestal",status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response("falta el nodo registropresupuestalid",status = status.HTTP_400_BAD_REQUEST) 

        consecutivo = consultarconsecutivo(6,institucioneducativa.id)
        request.data['consecutivo'] = consecutivo

        obligacionpresupuestal_serializers = ObligacionpresupuestalSerializers(data=request.data)

        if obligacionpresupuestal_serializers.is_valid():
            obligacionpresupuestal_serializers.save()
            actualizarconsecutivo(6,institucioneducativa.id,consecutivo)
            return Response(obligacionpresupuestal_serializers.data,status = status.HTTP_201_CREATED)
        return Response(obligacionpresupuestal_serializers.errors,status = status.HTTP_400_BAD_REQUEST) 

@api_view(['GET','DELETE'])
def obligacionpresupuestal_consecutivo_api_view(request): 
    obligacionpresupuestal = buscar_op_consecutivo(request) 
    if obligacionpresupuestal:
        if request.method =='GET': 
            obligacionpresupuestal_serializers = ObligacionpresupuestalSerializers(obligacionpresupuestal)
            return Response(obligacionpresupuestal_serializers.data,status = status.HTTP_200_OK)
        elif request.method == 'DELETE':
            
            try:
                obligacionpresupuestal.delete()
                return Response('Documento Eliminado Correctamente',status = status.HTTP_200_OK)
            except RestrictedError:
                return Response('RP no puede ser eliminado esta asociado a un Pago Presupuestal',status = status.HTTP_400_BAD_REQUEST)            
    return Response('Documento no exite',status = status.HTTP_400_BAD_REQUEST) 

def buscar_op_consecutivo(request):
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
    
    obligacionpresupuestal = Obligacionpresupuestal.objects.filter(institucioneducativaid = institucioneducativaid, consecutivo = consecutivo).first()
    return obligacionpresupuestal

def buscar_obligacionpresupuestal_all(request):
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
        
    
    obligacionpresupuestal = Obligacionpresupuestal.objects.filter(institucioneducativaid = institucioneducativaid, fecha__year = codigoperiodo).all()
    return obligacionpresupuestal

def saldo_opresu_por_pagopresu(opresuid):
    totalopresu=0
    totalpagopresu=0
    saldo = 0
    opresu = Obligacionpresupuestal.objects.filter(id=opresuid).first()
    if opresu:
        totalopresu = opresu.valor
        pagopresu = Pagopresupuestal.objects.filter(obligacionpresupuestalid = opresu.id).values('obligacionpresupuestalid').annotate(total=Sum('valor'))
        if pagopresu:
            totalpagopresu = pagopresu[0]['total']

    saldo = totalopresu - totalpagopresu
    return saldo

def saldo_opresu_por_pagopresu_consecutivo(institucioneducativaid,consecutivo):
    saldo = 0
    opresu = Obligacionpresupuestal.objects.filter(institucioneducativaid=institucioneducativaid,consecutivo=consecutivo).first()
    if opresu:
        saldo = saldo_opresu_por_pagopresu(opresu.id)
    
    return saldo

@api_view(['GET'])
def saldo_opresu_por_pagopresu_api_view(request):  
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
                
                return Response(saldo_opresu_por_pagopresu_consecutivo(institucioneducativa_parametros.id,consecutivo),status = status.HTTP_200_OK)
            else:
                return Response('institucion educativa no existe',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('institucion educativa no existe',status = status.HTTP_400_BAD_REQUEST)