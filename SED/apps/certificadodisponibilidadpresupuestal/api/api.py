from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.certificadodisponibilidadpresupuestal.models import Certificadodisponibilidadpresupuestal
from apps.certificadodisponibilidadpresupuestal.api.serializers import CertificadodisponibilidadpresupuestalSerializers
from apps.periodo.models import Periodo
from apps.institucioneducativa.models import Institucioneducativa
from apps.rubropresupuestal.models import Rubropresupuestal
from apps.consecutivo.api.api import consultarconsecutivo
from apps.consecutivo.api.api import actualizarconsecutivo

@api_view(['GET','POST'])
def certificadodisponibilidadpresupuestal_api_view(request):  
     
    if request.method =='GET':
        certificadodisponibilidadpresupuestal = buscar_cdp_all(request)
        certificadodisponibilidadpresupuestal =  CertificadodisponibilidadpresupuestalSerializers(certificadodisponibilidadpresupuestal, many = True)
        return Response(certificadodisponibilidadpresupuestal.data,status = status.HTTP_200_OK)
    elif request.method =='POST':
        institucioneducativa = Institucioneducativa()
        rubropresupuestal = Rubropresupuestal()
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
                return Response("falta el nodo codigo para institucion educativa",status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response("falta el nodo institucioneducativaid",status = status.HTTP_400_BAD_REQUEST) 

        if 'rubropresupuestalid' in request.data.keys():
            rubropresupuestalid = request.data.pop('rubropresupuestalid')
            if 'codigo' in rubropresupuestalid.keys():
                rubropresupuestal = Rubropresupuestal.objects.filter(codigo = rubropresupuestalid['codigo']).first() 
                if rubropresupuestal:
                    request.data.update({"rubropresupuestalid": rubropresupuestal.id})
                else:
                    return Response("rubro presupuestal ingresado no existe",status = status.HTTP_400_BAD_REQUEST)                     
            else:
                return Response("falta el nodo codigo para rubropresupuestal",status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response("falta el nodo rubropresupuestalid",status = status.HTTP_400_BAD_REQUEST) 

        consecutivo = consultarconsecutivo(4,institucioneducativa.id)
        request.data['consecutivo'] = consecutivo
        
        certificadodisponibilidadpresupuestal_Serializers = CertificadodisponibilidadpresupuestalSerializers(data = request.data)

        if certificadodisponibilidadpresupuestal_Serializers.is_valid(): 
            #return Response(request.data,status = status.HTTP_201_CREATED)        
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
            #try:
                certificadodisponibilidadpresupuestal.delete()
                return Response('Documento Eliminado Correctamente',status = status.HTTP_200_OK)
            #except RestrictedError:
            #    return Response('Solicitud presupuestal no puede ser eliminado',status = status.HTTP_400_BAD_REQUEST)            
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

