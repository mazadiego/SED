from operator import truediv
from tkinter.tix import Tree
from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apps.recaudopresupuestal.models import Recaudopresupuestal
from apps.periodo.models import Periodo
from apps.institucioneducativa.models import Institucioneducativa
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.recaudopresupuestal.api.serializers import Recaudopresupuestalserializers
from apps.tiporecaudo.models import Tiporecaudo
from apps.ingresopresupuestal.models import Ingresopresupuestal
from apps.consecutivo.api.api import consultarconsecutivo
from apps.consecutivo.api.api import actualizarconsecutivo
from apps.ingresopresupuestal.api.api import saldoingresoporrecaudo,saldoingresoporrecaudo_mod
from django.db.utils import IntegrityError
from apps.proyeccionpresupuestaldetalle.models import Proyeccionpresupuestaldetalle
from apps.rubropresupuestal.api.api import buscarrubro_solicitud,buscar_rubro_cdp

@api_view(['GET','POST'])
def recaudopresupuestal_api_view(request):  
     
    if request.method =='GET':
        recaudopresupuestal = buscarrecaudopresupuestal(request)
        recaudopresupuestal_serializers =  Recaudopresupuestalserializers(recaudopresupuestal, many = True)
        return Response(recaudopresupuestal_serializers.data,status = status.HTTP_200_OK)

    elif request.method =='POST':
        institucioneducativa = Institucioneducativa()
        tiporecaudo = Tiporecaudo()
        ingresopresupuestal = Ingresopresupuestal()
        consecutivoingreso = 0 
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

        if 'tiporecaudoid' in request.data.keys():
            tiporecaudoid = request.data.pop('tiporecaudoid')
            if 'codigo' in tiporecaudoid.keys():
                tiporecaudo = Tiporecaudo.objects.filter(codigo = tiporecaudoid['codigo']).first()
                if tiporecaudo:
                    request.data.update({"tiporecaudoid": tiporecaudo.id})
                else:
                    return Response("tiporecaudo no existe",status = status.HTTP_400_BAD_REQUEST)            
            else:
                return Response("falta el nodo codigo para consultar tipo recaudo",status = status.HTTP_400_BAD_REQUEST)       
        else:
            return Response("falta el nodo tiporecaudoid",status = status.HTTP_400_BAD_REQUEST)   

        if 'ingresopresupuestalid' in request.data.keys():
            ingresopresupuestalid = request.data.pop('ingresopresupuestalid')
            if 'consecutivo' in ingresopresupuestalid.keys():                
                consecutivoingreso = ingresopresupuestalid['consecutivo']
                ingresopresupuestal = Ingresopresupuestal.objects.filter(institucioneducativaid = institucioneducativa.id, consecutivo = consecutivoingreso).first()
                if ingresopresupuestal:
                    if ingresopresupuestal.estado =='Procesado':
                        request.data.update({"ingresopresupuestalid": ingresopresupuestal.id})
                    else:
                        return Response("Documento ingreso presupuestal no se puede relacionar en estado Anulado",status = status.HTTP_400_BAD_REQUEST)           
                else:
                    return Response("Documento ingreso presupuestal no existe",status = status.HTTP_400_BAD_REQUEST)           
            else:
                return Response("falta el nodo consecutivo para consultar el ingreso presupuestal",status = status.HTTP_400_BAD_REQUEST)       
        else:
            return Response("falta el nodo ingresopresupuestalid",status = status.HTTP_400_BAD_REQUEST)   
        
                
        consecutivo = consultarconsecutivo(2,institucioneducativa.id)
        request.data['consecutivo'] = consecutivo
        recaudopresupuestal_serializers =  Recaudopresupuestalserializers(data = request.data)
        if validarsaldoingresoporrecaudo(institucioneducativa.id,consecutivoingreso,request.data['valor'])==True:
            if recaudopresupuestal_serializers.is_valid():
                try:
                    recaudopresupuestal_serializers.save()
                    actualizarconsecutivo(2,institucioneducativa.id,consecutivo)
                    return Response(recaudopresupuestal_serializers.data,status = status.HTTP_201_CREATED)
                except IntegrityError:
                    return Response('error recaudo presupuestal documento duplicado para institucion educativa seleccionada',status = status.HTTP_400_BAD_REQUEST)
            return Response(recaudopresupuestal_serializers.errors,status = status.HTTP_400_BAD_REQUEST)  
        else:
            return Response("el valor del recaudo supera el saldo por recaudo del documento de ingreso presupuestal relacionado",status = status.HTTP_400_BAD_REQUEST) 
          
@api_view(['GET','DELETE','PUT'])
def recaudopresupuestal_consecutivo_api_view(request): 
    recaudopresupuestal = buscarrecaudopresupuestalconsecutivo(request) 
    if recaudopresupuestal:
        if request.method =='GET': 
            recaudopresupuestal_serializers = Recaudopresupuestalserializers(recaudopresupuestal)
            return Response(recaudopresupuestal_serializers.data,status = status.HTTP_200_OK)
        elif request.method == 'DELETE':
            #if validar_recaudo_cdp(recaudopresupuestal.institucioneducativaid,recaudopresupuestal.ingresopresupuestalid.fuenterecursoid.id)==False:
            if validar_recaudo_solicitud(recaudopresupuestal.institucioneducativaid,recaudopresupuestal.ingresopresupuestalid.fuenterecursoid.id)==False:
                if recaudopresupuestal.estado =='Procesado':
                    recaudopresupuestal.estado ='Anulado' 
                    recaudopresupuestal.save()
                    return Response('Documento Anulado Correctamente',status = status.HTTP_200_OK)
                return Response('Recaudo presupuestal no puede ser anulado en este Estado',status = status.HTTP_400_BAD_REQUEST)
            return Response("Recaudo no puede ser eliminado, rubro asociado esta asigando a una solicitud presupuestal",status = status.HTTP_400_BAD_REQUEST)
            #return Response("Recaudo no puede ser eliminado, fuente asociado esta asigando a un CDP",status = status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PUT':
            consecutivoingreso = 0 
            if validar_recaudo_solicitud(recaudopresupuestal.institucioneducativaid,recaudopresupuestal.ingresopresupuestalid.fuenterecursoid.id)==False:
                if recaudopresupuestal.estado =='Procesado':
                    if 'institucioneducativaid' in request.data.keys():
                        request.data['institucioneducativaid'] = recaudopresupuestal.institucioneducativaid.id
                    else:
                        return Response("falta el nodo institucioneducativaid",status = status.HTTP_400_BAD_REQUEST) 

                    if 'consecutivo' in request.data.keys():
                        request.data['consecutivo'] = recaudopresupuestal.consecutivo
                    else:
                        return Response("falta el nodo consecutivo",status = status.HTTP_400_BAD_REQUEST)

                    if 'fecha' in request.data.keys():
                        request.data['fecha'] = recaudopresupuestal.fecha
                    else:
                        return Response("falta el nodo fecha",status = status.HTTP_400_BAD_REQUEST)
                    
                    if 'estado' in request.data.keys():
                        request.data['estado'] = recaudopresupuestal.estado 

                    if 'tiporecaudoid' in request.data.keys():
                        tiporecaudoid = request.data.pop('tiporecaudoid')
                        if 'codigo' in tiporecaudoid.keys():
                            tiporecaudo = Tiporecaudo.objects.filter(codigo = tiporecaudoid['codigo']).first()
                            if tiporecaudo:
                                request.data.update({"tiporecaudoid": tiporecaudo.id})
                            else:
                                return Response("tiporecaudo no existe",status = status.HTTP_400_BAD_REQUEST)            
                        else:
                            return Response("falta el nodo codigo para consultar tipo recaudo",status = status.HTTP_400_BAD_REQUEST)       
                    else:
                        return Response("falta el nodo tiporecaudoid",status = status.HTTP_400_BAD_REQUEST) 

                    if 'ingresopresupuestalid' in request.data.keys():
                        ingresopresupuestalid = request.data.pop('ingresopresupuestalid')
                        if 'consecutivo' in ingresopresupuestalid.keys():                
                            consecutivoingreso = ingresopresupuestalid['consecutivo']
                            ingresopresupuestal = Ingresopresupuestal.objects.filter(institucioneducativaid = recaudopresupuestal.institucioneducativaid.id, consecutivo = consecutivoingreso).first()
                            if ingresopresupuestal:
                                if ingresopresupuestal.estado =='Procesado':
                                    request.data.update({"ingresopresupuestalid": ingresopresupuestal.id})
                                else:
                                    return Response("Documento ingreso presupuestal no se puede relacionar en estado Anulado",status = status.HTTP_400_BAD_REQUEST)           
                            else:
                                return Response("Documento ingreso presupuestal no existe",status = status.HTTP_400_BAD_REQUEST)           
                        else:
                            return Response("falta el nodo consecutivo para consultar el ingreso presupuestal",status = status.HTTP_400_BAD_REQUEST)       
                    else:
                        return Response("falta el nodo ingresopresupuestalid",status = status.HTTP_400_BAD_REQUEST)
                        
                    recaudopresupuestal_serializers =  Recaudopresupuestalserializers(recaudopresupuestal,data = request.data)
                    if recaudopresupuestal_serializers.is_valid(): 
                        if recaudopresupuestal.ingresopresupuestalid.consecutivo != consecutivoingreso or recaudopresupuestal.valor != request.data['valor']:
                            if validarsaldoingresoporrecaudo_mod(recaudopresupuestal,consecutivoingreso,request.data['valor'])==True:                            
                                recaudopresupuestal_serializers.save()
                                return Response(recaudopresupuestal_serializers.data,status = status.HTTP_201_CREATED)                                                            
                            else:
                                return Response("el valor del recaudo supera el saldo por recaudo del documento de ingreso presupuestal relacionado",status = status.HTTP_400_BAD_REQUEST) 
                        else:                                                
                            recaudopresupuestal_serializers.save()
                            return Response(recaudopresupuestal_serializers.data,status = status.HTTP_201_CREATED)                            
                    return Response(recaudopresupuestal_serializers.errors,status = status.HTTP_400_BAD_REQUEST)


                return Response('Recaudo presupuestal no puede ser actualizado en este Estado',status = status.HTTP_400_BAD_REQUEST)
            return Response("Recaudo no puede ser Actualizado, rubro asociado esta asigando a una solicitud presupuestal",status = status.HTTP_400_BAD_REQUEST)
    return Response('Documento no exite',status = status.HTTP_400_BAD_REQUEST)
    
def buscarrecaudopresupuestalconsecutivo(request):
    parametros = dict(request.query_params)
        
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
            institucioneducativa_parametros_serializer = InstitucioneducativaSerializer(institucioneducativa_parametros)
            institucioneducativa_parametros = dict(institucioneducativa_parametros_serializer.data)
        else:
            institucioneducativa_parametros = dict({"id":0})
    else:
        institucioneducativa_parametros = dict({"id":0})
    
    recaudopresupuestal = Recaudopresupuestal.objects.filter(institucioneducativaid = institucioneducativa_parametros['id'], consecutivo = consecutivo).first()
    return recaudopresupuestal

def buscarrecaudopresupuestal(request):
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
        
        recaudopresupuestal = Recaudopresupuestal.objects.filter(institucioneducativaid = institucioneducativa_parametros['id'], fecha__year = codigoperiodo).all()
        return recaudopresupuestal

def validarsaldoingresoporrecaudo(institucioneducativaid,consecutivoingreso,valoractual):
    saldo = 0
    saldo = saldoingresoporrecaudo (institucioneducativaid,consecutivoingreso) - valoractual

    if saldo >=0:
        return True
    else:
        return False

def validarsaldoingresoporrecaudo_mod(recaudopresupuestal,consecutivoingreso,valoractual):
    saldo = 0
    saldo = saldoingresoporrecaudo_mod (recaudopresupuestal,consecutivoingreso) - valoractual

    if saldo >=0:
        return True
    else:
        return False



def validar_recaudo_solicitud(institucioneducativaid,fuenterecursoid):

    validar = False
    periodo = Periodo.objects.filter(activo = True).first()
    if periodo:
        rubros = Proyeccionpresupuestaldetalle.objects.select_related('proyeccionpresupuestalid','proyeccionpresupuestalid__periodoid').values('rubropresupuestalid').filter(proyeccionpresupuestalid__estado = 'Aprobado',proyeccionpresupuestalid__institucioneducativaid =institucioneducativaid,fuenterecursoid=fuenterecursoid,proyeccionpresupuestalid__periodoid__id=periodo.id).all()

        for rubro in rubros:
            if buscarrubro_solicitud(institucioneducativaid.id,rubro['rubropresupuestalid']):
                validar = True                
                break
    return validar

def validar_recaudo_cdp(institucioneducativaid,fuenterecursoid):
    validar = False
    periodo = Periodo.objects.filter(activo = True).first()
    if periodo:
        rubros = Proyeccionpresupuestaldetalle.objects.select_related('proyeccionpresupuestalid','proyeccionpresupuestalid__periodoid').values('rubropresupuestalid').filter(proyeccionpresupuestalid__estado = 'Aprobado',proyeccionpresupuestalid__institucioneducativaid =institucioneducativaid,fuenterecursoid=fuenterecursoid,proyeccionpresupuestalid__periodoid__id=periodo.id).all()

        for rubro in rubros:
            if buscar_rubro_cdp(institucioneducativaid.id,rubro['rubropresupuestalid']):
                validar = True                
                break
    return validar

    