from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.modificacionproyeccionpresupuestalcabecera.models import Modificacionproyeccionpresupuestalcabecera
from apps.modificacionproyeccionpresupuestalcabecera.api.serializers import ModificacionproyeccionpresupuestalcabeceraSerializers
from apps.institucioneducativa.models import Institucioneducativa
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from django.db.models.deletion import RestrictedError
from django.db.utils import IntegrityError
from apps.periodo.models import Periodo
from apps.periodo.api.serializers import Periodoserializers

@api_view(['GET','POST','DELETE','PUT'])
def modificacionproyeccionpresupuestalcabecera_api_view(request):    
    if request.method =='GET':
        
        modificacionproyeccionpresupuestalcabecera = buscarmodificacionproyeccionpresupuestalcabecera(request)        
        modificacionproyeccionpresupuestalcabecera_serializers = ModificacionproyeccionpresupuestalcabeceraSerializers(modificacionproyeccionpresupuestalcabecera)
        return Response(modificacionproyeccionpresupuestalcabecera_serializers.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        
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
        
        if 'periodoid' in request.data.keys():
            periodoid = request.data.pop('periodoid')
            if 'codigo' in periodoid.keys():
                periodo = Periodo.objects.filter(codigo = periodoid['codigo']).first()
                if periodo:
                    request.data.update({"periodoid" : periodo.id})
                else:
                    return Response('periodo no existe',status = status.HTTP_400_BAD_REQUEST)  
            else:  
                return Response('falta el nodo codigo para el periodo',status = status.HTTP_400_BAD_REQUEST) 
        else:
            return Response('falta el nodo periodoid',status = status.HTTP_400_BAD_REQUEST) 

        modificacionproyeccionpresupuestalcabecera_serializers = ModificacionproyeccionpresupuestalcabeceraSerializers(data = request.data)            
                    
        if modificacionproyeccionpresupuestalcabecera_serializers.is_valid():
            
            try:
                modificacionproyeccionpresupuestalcabecera_serializers.save()
                return Response(modificacionproyeccionpresupuestalcabecera_serializers.data,status = status.HTTP_201_CREATED)
            except IntegrityError:
                return Response('la institucion educativa ya tiene una modificacion de proyeccion presupuestal en el periodo seleccionado',status = status.HTTP_400_BAD_REQUEST)
        return Response(modificacionproyeccionpresupuestalcabecera_serializers.errors, status = status.HTTP_400_BAD_REQUEST)            
        
    elif request.method =='DELETE': 
        modificacionproyeccionpresupuestalcabecera = buscarmodificacionproyeccionpresupuestalcabecera(request)
        if modificacionproyeccionpresupuestalcabecera:
            try:
                modificacionproyeccionpresupuestalcabecera.delete()
                return Response('Eliminado Correctamente',status = status.HTTP_200_OK)
            except RestrictedError:
                return Response('proyeccion presupuestal no puede ser eliminar',status = status.HTTP_400_BAD_REQUEST)
        return Response('no existe cabecera',status = status.HTTP_400_BAD_REQUEST)
    elif request.method =='PUT': 
        data = request.data 
        modificacionproyeccionpresupuestalcabecera = buscarmodificacionproyeccionpresupuestalcabecera(request)
        if modificacionproyeccionpresupuestalcabecera:
            modificacionproyeccionpresupuestalcabecera_serializers = ModificacionproyeccionpresupuestalcabeceraSerializers(modificacionproyeccionpresupuestalcabecera)  
            modificacionproyeccionpresupuestalcabecera_dict = dict(modificacionproyeccionpresupuestalcabecera_serializers.data)           
            if 'periodoid' in data.keys():                   
                periodoid = modificacionproyeccionpresupuestalcabecera_dict['periodoid']
                request.data['periodoid'] = periodoid['id'] 
                if 'institucioneducativaid' in data.keys():
                    institucioneducativaid = modificacionproyeccionpresupuestalcabecera_dict['institucioneducativaid']
                    request.data['institucioneducativaid'] = institucioneducativaid['id']
                    modificacionproyeccionpresupuestalcabecera_PUT = ModificacionproyeccionpresupuestalcabeceraSerializers(modificacionproyeccionpresupuestalcabecera, data = request.data)
                    if modificacionproyeccionpresupuestalcabecera_PUT.is_valid():
                        modificacionproyeccionpresupuestalcabecera_PUT.save()
                        return Response(modificacionproyeccionpresupuestalcabecera_PUT.data,status = status.HTTP_201_CREATED)    
                    return Response(modificacionproyeccionpresupuestalcabecera_PUT.errors, status = status.HTTP_400_BAD_REQUEST)    
                return Response('falta el nodo institucioneducativaid',status = status.HTTP_400_BAD_REQUEST)    
            return Response('falta el nodo periodoid',status = status.HTTP_400_BAD_REQUEST)     
        return Response('no existe cabecera',status = status.HTTP_400_BAD_REQUEST)

def buscarmodificacionproyeccionpresupuestalcabecera(request):
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
        
        modificacionproyeccionpresupuestalcabecera = Modificacionproyeccionpresupuestalcabecera.objects.filter(periodoid=periodo_parametros['id'], institucioneducativaid = institucioneducativa_parametros['id'] ).first() 
        return modificacionproyeccionpresupuestalcabecera

def buscarmodificacionproyeccionpresupuestalcabecera_dict(parametros):
        
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
        
        modificacionproyeccionpresupuestalcabecera = Modificacionproyeccionpresupuestalcabecera.objects.filter(periodoid=periodo_parametros['id'], institucioneducativaid = institucioneducativa_parametros['id'] ).first() 
        return modificacionproyeccionpresupuestalcabecera
