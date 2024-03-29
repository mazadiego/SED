from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.proyeccionpresupuestalcabecera.models import Proyeccionpresupuestalcabecera
from apps.proyeccionpresupuestalcabecera.api.serializers import ProyeccionpresupuestalcabeceraSerializers
from apps.institucioneducativa.models import Institucioneducativa
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from django.db.models.deletion import RestrictedError
from django.db.utils import IntegrityError
from apps.periodo.models import Periodo
from apps.periodo.api.serializers import Periodoserializers
from apps.proyeccionpresupuestaldetalle.models import Proyeccionpresupuestaldetalle

@api_view(['GET','POST','DELETE','PUT'])
def proyeccionpresupuestalcabecera_api_view(request):    
    if request.method =='GET':
        
        proyeccionpresupuestalcabecera = buscarproyeccionpresupuestalcabecera(request)        
        proyeccionpresupuestalcabecera_serializers = ProyeccionpresupuestalcabeceraSerializers(proyeccionpresupuestalcabecera)
        return Response(proyeccionpresupuestalcabecera_serializers.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        data = request.data  
        if 'estado' in data.keys():
            data['estado'] = 'Por Aprobar'

        if 'institucioneducativaid' in data.keys():
            institucioneducativaid = data.pop('institucioneducativaid')
            if 'codigo' in institucioneducativaid.keys():
                institucioneducativa = Institucioneducativa.objects.filter(codigo = institucioneducativaid['codigo']).first() 
                if institucioneducativa:
                    institucioneducativaid_serializer = InstitucioneducativaSerializer(institucioneducativa)
                    institucioneducativaid = dict(institucioneducativaid_serializer.data)
                    data.update({"institucioneducativaid": institucioneducativaid['id'] })

                    if 'periodoid' in data.keys():
                        periodoid = data.pop('periodoid')
                        if 'codigo' in periodoid.keys():
                            periodo = Periodo.objects.filter(codigo = periodoid['codigo']).first()
                            if periodo:
                                periodoid_serializers = Periodoserializers(periodo)
                                periodoid = dict(periodoid_serializers.data)
                                data.update({"periodoid" : periodoid['id']})

                                proyeccionpresupuestalcabecera_serializers = ProyeccionpresupuestalcabeceraSerializers(data = request.data)            
                                
                                if proyeccionpresupuestalcabecera_serializers.is_valid():
                                    try:
                                        proyeccionpresupuestalcabecera_serializers.save()
                                        return Response(proyeccionpresupuestalcabecera_serializers.data,status = status.HTTP_201_CREATED)
                                    except IntegrityError:
                                        return Response('la institucion educativa ya tiene una proyeccion presupuestal en el periodo seleccionado',status = status.HTTP_400_BAD_REQUEST)
                                return Response(proyeccionpresupuestalcabecera_serializers.errors, status = status.HTTP_400_BAD_REQUEST)
                            return Response('periodo no existe',status = status.HTTP_400_BAD_REQUEST)    
                        return Response('falta el nodo codigo para el periodo',status = status.HTTP_400_BAD_REQUEST) 
                    return Response('falta el nodo periodoid',status = status.HTTP_400_BAD_REQUEST) 
                return Response('institucion educativa ingresada no existe',status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo codigo para tipo institucion educativa',status = status.HTTP_400_BAD_REQUEST) 
        return Response('falta el nodo institucioneducativaid',status = status.HTTP_400_BAD_REQUEST)
    elif request.method =='DELETE': 
        proyeccionpresupuestalcabecera = buscarproyeccionpresupuestalcabecera(request)
        if proyeccionpresupuestalcabecera:
            if proyeccionpresupuestalcabecera.estado !='Aprobado':
                try:
                    proyeccionpresupuestalcabecera.delete()
                    return Response('Eliminado Correctamente',status = status.HTTP_200_OK)
                except RestrictedError:
                    return Response('proyeccion presupuestal no puede ser eliminar',status = status.HTTP_400_BAD_REQUEST)
            return Response('proyeccion presupuestal no se puede ser eliminar en este Estado',status = status.HTTP_400_BAD_REQUEST)
        return Response('no existe cabecera',status = status.HTTP_400_BAD_REQUEST)
    elif request.method =='PUT': 
        data = request.data 
        proyeccionpresupuestalcabecera = buscarproyeccionpresupuestalcabecera(request)
        if proyeccionpresupuestalcabecera:
            if proyeccionpresupuestalcabecera.estado !='Aprobado':
                proyeccionpresupuestalcabecera_serializers = ProyeccionpresupuestalcabeceraSerializers(proyeccionpresupuestalcabecera)  
                proyeccionpresupuestalcabecera_dict = dict(proyeccionpresupuestalcabecera_serializers.data)           
                if 'periodoid' in data.keys():                   
                    periodoid = proyeccionpresupuestalcabecera_dict['periodoid']
                    request.data['periodoid'] = periodoid['id'] 
                    if 'institucioneducativaid' in data.keys():
                        institucioneducativaid = proyeccionpresupuestalcabecera_dict['institucioneducativaid']
                        request.data['institucioneducativaid'] = institucioneducativaid['id']
                        proyeccionpresupuestalcabecera_PUT = ProyeccionpresupuestalcabeceraSerializers(proyeccionpresupuestalcabecera, data = request.data)
                        if proyeccionpresupuestalcabecera_PUT.is_valid():
                            proyeccionpresupuestalcabecera_PUT.save()
                            return Response(proyeccionpresupuestalcabecera_PUT.data,status = status.HTTP_201_CREATED)    
                        return Response(proyeccionpresupuestalcabecera_PUT.errors, status = status.HTTP_400_BAD_REQUEST)    
                    return Response('falta el nodo institucioneducativaid',status = status.HTTP_400_BAD_REQUEST)    
                return Response('falta el nodo periodoid',status = status.HTTP_400_BAD_REQUEST)
            return Response('proyeccion presupuestal no se puede ser modificar en este Estado',status = status.HTTP_400_BAD_REQUEST)     
        return Response('no existe cabecera',status = status.HTTP_400_BAD_REQUEST)
@api_view(['GET','PUT'])
def proyeccionpresupuestal_Aprobar_api_view(request): 
    if request.method =='GET': 
        proyeccionpresupuestalcabecera = buscarproyeccionpresupuestalcabecera(request)        
        proyeccionpresupuestalcabecera_serializers = ProyeccionpresupuestalcabeceraSerializers(proyeccionpresupuestalcabecera)
        return Response(proyeccionpresupuestalcabecera_serializers.data,status = status.HTTP_200_OK)
    if request.method =='PUT': 
        proyeccionpresupuestalcabecera = buscarproyeccionpresupuestalcabecera(request)
        if proyeccionpresupuestalcabecera:
            proyeccionpresupuestaldetalle = Proyeccionpresupuestaldetalle.objects.filter(proyeccionpresupuestalid = proyeccionpresupuestalcabecera.id).all()
            if proyeccionpresupuestaldetalle:
                if proyeccionpresupuestalcabecera.estado !='Aprobado':
                    proyeccionpresupuestalcabecera.estado ='Aprobado' 
                    proyeccionpresupuestalcabecera.save()
                    proyeccionpresupuestalcabecera_serializers = ProyeccionpresupuestalcabeceraSerializers(proyeccionpresupuestalcabecera)                  
                    return Response(proyeccionpresupuestalcabecera_serializers.data,status = status.HTTP_200_OK)                 
                return Response('proyeccion presupuestal no se puede ser aprobar en este Estado',status = status.HTTP_400_BAD_REQUEST)     
            return Response("No existe registros en el detalle para aprobar documento",status = status.HTTP_400_BAD_REQUEST)
        return Response('no existe cabecera',status = status.HTTP_400_BAD_REQUEST)

def buscarproyeccionpresupuestalcabecera(request):
        parametros = dict(request.query_params)
        codigoperiodo = 0
        codigoinstitucioneducativa = ""
        institucioneducativa_parametros = ""    
        periodo_parametros = ""
        
        if 'codigoperiodo' in parametros.keys():
            codigoperiodo = parametros["codigoperiodo"][0]
            
            periodo_parametros =  Periodo.objects.filter(codigo = codigoperiodo).first()

            if periodo_parametros:
                periodo_parametros_serializers = Periodoserializers(periodo_parametros)
                periodo_parametros = dict(periodo_parametros_serializers.data)
            else:
                periodo_parametros = dict({"id":0})
        else:
            periodo_parametros = dict({"id":0})

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
        
        proyeccionpresupuestalcabecera = Proyeccionpresupuestalcabecera.objects.filter(periodoid=periodo_parametros['id'], institucioneducativaid = institucioneducativa_parametros['id'] ).first() 
        return proyeccionpresupuestalcabecera

def buscarproyeccionpresupuestalcabecera_dict(parametros):
        
        codigoperiodo = 0
        codigoinstitucioneducativa = ""
        institucioneducativa_parametros = ""    
        periodo_parametros = ""
        
        if 'codigoperiodo' in parametros.keys():
            codigoperiodo = parametros["codigoperiodo"]
            
            periodo_parametros =  Periodo.objects.filter(codigo = codigoperiodo).first()

            if periodo_parametros:
                periodo_parametros_serializers = Periodoserializers(periodo_parametros)
                periodo_parametros = dict(periodo_parametros_serializers.data)
            else:
                periodo_parametros = dict({"id":0})
        else:
            periodo_parametros = dict({"id":0})

        if 'codigoinstitucioneducativa' in parametros.keys():
            codigoinstitucioneducativa = str(parametros["codigoinstitucioneducativa"])
            codigoinstitucioneducativa = codigoinstitucioneducativa.upper() 
            
            institucioneducativa_parametros = Institucioneducativa.objects.filter(codigo =codigoinstitucioneducativa).first()
            if institucioneducativa_parametros:            
                institucioneducativa_parametros_serializer = InstitucioneducativaSerializer(institucioneducativa_parametros)
                institucioneducativa_parametros = dict(institucioneducativa_parametros_serializer.data)
            else:
                institucioneducativa_parametros = dict({"id":0})
        else:
            institucioneducativa_parametros = dict({"id":0})
        
        proyeccionpresupuestalcabecera = Proyeccionpresupuestalcabecera.objects.filter(periodoid=periodo_parametros['id'], institucioneducativaid = institucioneducativa_parametros['id'] ).first() 
        return proyeccionpresupuestalcabecera
