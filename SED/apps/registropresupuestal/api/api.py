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
            #hay que meter una restriccion cuando se cree el documento de obligacion presupuestal
            #try:
                registropresupuestal.delete()
                return Response('Documento Eliminado Correctamente',status = status.HTTP_200_OK)
            #except RestrictedError:
            #    return Response('CDP no puede ser eliminado esta asociado a un Registro Presupuestal',status = status.HTTP_400_BAD_REQUEST)            
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

