from operator import truediv
from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apps.solicitudpresupuestalcabecera.models import Solicitudpresupuestalcabecera
from apps.solicitudpresupuestalcabecera.api.serializers import SolicitudpresupuestalcabeceraSerializers
from apps.institucioneducativa.models import Institucioneducativa
from apps.personalplanta.models import Personalplanta
from apps.tercero.models import Tercero
from apps.tipoidentificacion.models import Tipoidentificacion
from apps.tipocontrato.models import Tipocontrato
from apps.periodo.models import Periodo
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from apps.consecutivo.api.api import consultarconsecutivo
from apps.consecutivo.api.api import actualizarconsecutivo
from django.db.models.deletion import RestrictedError

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
        tercero = Tercero()
        tipocontrato = Tipocontrato()

        
        consecutivo = 0
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
        
        if 'tipocontratoid' in request.data.keys():
            tipocontratoid = request.data.pop('tipocontratoid')
            if 'codigo' in tipocontratoid.keys():
                tipocontrato = Tipocontrato.objects.filter(codigo = tipocontratoid['codigo']).first()                
                if tipocontrato:
                    request.data.update({"tipocontratoid": tipocontrato.id})
                else:
                    return Response("tipo contrato no existe",status =status.HTTP_400_BAD_REQUEST)        
            else:
                return Response("falta el nodo codigo para consultar tipo contrato",status =status.HTTP_400_BAD_REQUEST)    
        else:
            return Response("falta el nodo tipocontratoid",status =status.HTTP_400_BAD_REQUEST)
                
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
            try:
                solicitudpresupuestal.delete()
                return Response('Documento Eliminado Correctamente',status = status.HTTP_200_OK)
            except RestrictedError:
                return Response('Solicitud presupuestal no puede ser eliminado',status = status.HTTP_400_BAD_REQUEST)            
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