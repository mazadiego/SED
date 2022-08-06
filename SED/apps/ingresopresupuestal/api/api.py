from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.ingresopresupuestal.models import Ingresopresupuestal
from apps.ingresopresupuestal.api.serializers import Ingresopresupuestalserializers
from apps.institucioneducativa.models import Institucioneducativa
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from django.db.models.deletion import RestrictedError
from django.db.utils import IntegrityError
from apps.tercero.models import Tercero
from apps.tercero.api.serializers import TerceroSerializer
from apps.fuenterecurso.api.api import buscarfuenterecurso_final,saldofuenterecursoporingreso
from apps.fuenterecurso.api.serializers import Fuenterecursoserializers
from apps.periodo.models import Periodo
from apps.periodo.api.serializers import Periodoserializers
from apps.fuenterecurso.api.api import buscarfuenterecursoproyeccion
from apps.consecutivo.api.api import consultarconsecutivo
from apps.consecutivo.api.api import actualizarconsecutivo
from apps.tipoidentificacion.models import Tipoidentificacion
from apps.tipoidentificacion.api.serializers import TipoidentificacionSerializer
from apps.recaudopresupuestal.models import Recaudopresupuestal
from django.db.models import Count,Sum

@api_view(['GET','POST'])
def ingresopresupuestal_api_view(request):    
    if request.method =='GET':
        
        ingresopresupuestal = buscaringresopresupuestal(request)        
        ingresopresupuestal_serializers = Ingresopresupuestalserializers(ingresopresupuestal, many = True)
        return Response(ingresopresupuestal_serializers.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        data = request.data  

        if 'estado' in data.keys():
            data['estado'] = 'Procesado'
        
        if 'institucioneducativaid' in data.keys():
            institucioneducativaid = data.pop('institucioneducativaid')
            if 'codigo' in institucioneducativaid.keys():
                institucioneducativa = Institucioneducativa.objects.filter(codigo = institucioneducativaid['codigo']).first() 
                if institucioneducativa:
                    institucioneducativaid_serializer = InstitucioneducativaSerializer(institucioneducativa)
                    institucioneducativaid = dict(institucioneducativaid_serializer.data)
                    data.update({"institucioneducativaid": institucioneducativaid['id']})
                    if 'terceroid' in data.keys():
                        terceroid = data.pop('terceroid')
                        if 'codigo' in terceroid.keys():   
                                tercero = Tercero.objects.filter(codigo = terceroid['codigo']).first()
                                if tercero:
                                    terceroid_serializers = TerceroSerializer(tercero)
                                    terceroid = dict(terceroid_serializers.data)
                                    data.update({"terceroid" : terceroid['id']})

                                    if 'fuenterecursoid' in data.keys():
                                        fuenterecursoid = data.pop('fuenterecursoid')
                                        fuenterecurso = buscarfuenterecurso_final(fuenterecursoid)

                                        if fuenterecurso:
                                            
                                            fuenterecurso_serializers =Fuenterecursoserializers(fuenterecurso)
                                            fuenterecursoid = dict(fuenterecurso_serializers.data)
                                            data.update({"fuenterecursoid":fuenterecursoid['id']})
                                            if buscarfuenterecursoproyeccion(fuenterecursoid['id'],institucioneducativaid['id'])==True:
                                                consecutivo = consultarconsecutivo(1,institucioneducativaid['id'])
                                                data['consecutivo'] = consecutivo
                                                ingresopresupuestal_serializers = Ingresopresupuestalserializers(data = request.data)
                                                if saldofuenterecursoporingreso(fuenterecursoid['id'],institucioneducativaid['id'],data['valor'])==True:                                             
                                                    if ingresopresupuestal_serializers.is_valid():                                                
                                                        try:
                                                            ingresopresupuestal_serializers.save()
                                                            actualizarconsecutivo(1,institucioneducativaid['id'],consecutivo)
                                                            return Response(ingresopresupuestal_serializers.data,status = status.HTTP_201_CREATED)
                                                        except IntegrityError:
                                                            return Response('error ingreso presupuestal documento duplicado para institucion educativa',status = status.HTTP_400_BAD_REQUEST)
                                                    return Response(ingresopresupuestal_serializers.errors, status = status.HTTP_400_BAD_REQUEST)
                                                return Response('fuente recurso supera el valor de la proyeccion presupuestal asignada para el periodo',status = status.HTTP_400_BAD_REQUEST)
                                            return Response('fuente recurso no tiene proyeccion presupuestal asignada o el periodo esta cerrado',status = status.HTTP_400_BAD_REQUEST)
                                        return Response('fuente recurso no es de detalle',status = status.HTTP_400_BAD_REQUEST)
                                    return Response('falta el nodo fuenterecursoid para buscar la fuente de recurso',status = status.HTTP_400_BAD_REQUEST)                                
                                return Response('tercero no existe',status = status.HTTP_400_BAD_REQUEST)                                
                        return Response('falta el nodo codigo para el tercero',status = status.HTTP_400_BAD_REQUEST) 
                    return Response('falta el nodo terceroid',status = status.HTTP_400_BAD_REQUEST) 
                return Response('institucion educativa ingresada no existe',status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo codigo para tipo institucion educativa',status = status.HTTP_400_BAD_REQUEST) 
        return Response('falta el nodo institucioneducativaid',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])
def ingresopresupuestal_consecutivo_api_view(request): 
    ingresopresupuestal = buscaringresopresupuestalconsecutivo(request) 
    if ingresopresupuestal:
        if request.method =='GET': 
            ingresopresupuestal_serializers = Ingresopresupuestalserializers(ingresopresupuestal)
            return Response(ingresopresupuestal_serializers.data,status = status.HTTP_200_OK)
        elif request.method == 'DELETE':    
                  
            if Recaudopresupuestal.objects.filter(ingresopresupuestalid = ingresopresupuestal.id, estado ='Procesado').count()==0:
                if ingresopresupuestal.estado =='Procesado':
                    ingresopresupuestal.estado ='Anulado' 
                    ingresopresupuestal.save()
                    return Response('Documento Anulado Correctamente',status = status.HTTP_200_OK)
                return Response('Ingreso presupuestal no puede ser anulado en este Estado',status = status.HTTP_400_BAD_REQUEST) 
            return Response('Ingreso presupuestal no puede ser Anulado esta asociado a un documento de recaudo',status = status.HTTP_400_BAD_REQUEST)            
    return Response('Documento no exite',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def ingresopresupuestalsaldoporrecaudo_api_view(request):  
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
                return Response(saldoingresoporrecaudo(institucioneducativa_parametros.id,consecutivo),status = status.HTTP_200_OK)
            else:
                return Response('institucion educativa no existe',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('institucion educativa no existe',status = status.HTTP_400_BAD_REQUEST)

        

def buscaringresopresupuestal(request):
        parametros = dict(request.query_params)
        codigoperiodo = 0
        codigoinstitucioneducativa = ""
        institucioneducativa_parametros = ""    

        periodo = Periodo.objects.filter(activo = True).first()

        if periodo:
            periodo_serializers = Periodoserializers(periodo)
            periodo = dict(periodo_serializers.data)
            codigoperiodo = periodo['codigo']
        
        
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
        
        ingresopresupuestal = Ingresopresupuestal.objects.filter(institucioneducativaid = institucioneducativa_parametros['id'], fecha__year = codigoperiodo).all()
        return ingresopresupuestal

def buscaringresopresupuestalconsecutivo(request):
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
        
        ingresopresupuestal = Ingresopresupuestal.objects.filter(institucioneducativaid = institucioneducativa_parametros['id'], consecutivo = consecutivo).first()
        return ingresopresupuestal

def saldoingresoporrecaudo(institucioneducativaid,consecutivo):
    totalingreso = 0
    saldo = 0
    totalrecaudo = 0
    ingresopresupuestal = Ingresopresupuestal.objects.filter(institucioneducativaid = institucioneducativaid, consecutivo = consecutivo).first()
 
    if ingresopresupuestal:
        totalingreso = ingresopresupuestal.valor
        recaudopresupuestal = Recaudopresupuestal.objects.filter(ingresopresupuestalid = ingresopresupuestal.id, estado ='Procesado').values('ingresopresupuestalid').annotate(total=Sum('valor'))
        if recaudopresupuestal :
            totalrecaudo = recaudopresupuestal[0]['total']

    saldo = totalingreso  - totalrecaudo

    return saldo