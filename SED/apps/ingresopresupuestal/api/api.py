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
from apps.fuenterecurso.api.api import buscarfuenterecurso_final,saldofuenterecursoporingreso,saldofuenterecursoporingreso_mod
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

from apps.recaudopresupuestal.api.serializers import Recaudopresupuestalserializers

from apps.certificadodisponibilidadpresupuestal.models import Certificadodisponibilidadpresupuestal
from apps.certificadodisponibilidadpresupuestal.api.serializers import CertificadodisponibilidadpresupuestalSerializers

from apps.registropresupuestal.models import Registropresupuestal
from apps.registropresupuestal.api.serializers import Registropresupuestalserializers

from apps.obligacionpresupuestal.models import Obligacionpresupuestal
from apps.obligacionpresupuestal.api.serializers import ObligacionpresupuestalSerializers

from apps.pagopresupuestal.models import Pagopresupuestal
from apps.pagopresupuestal.api.serializers import PagopresupuestalSerializers

from apps.solicitudpresupuestalcabecera.models import Solicitudpresupuestalcabecera
from apps.solicitudpresupuestalcabecera.api.serializers import SolicitudpresupuestalcabeceraSerializers

from apps.proyeccionpresupuestalcabecera.models import Proyeccionpresupuestalcabecera
from apps.proyeccionpresupuestalcabecera.api.serializers import ProyeccionpresupuestalcabeceraSerializers

from apps.modificacionproyeccionpresupuestalcabecera.models import Modificacionproyeccionpresupuestalcabecera
from apps.modificacionproyeccionpresupuestalcabecera.api.serializers import ModificacionproyeccionpresupuestalcabeceraSerializers

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

@api_view(['GET','DELETE','PUT'])
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
        elif request.method == 'PUT':
            if Recaudopresupuestal.objects.filter(ingresopresupuestalid = ingresopresupuestal.id, estado ='Procesado').count()==0:
                if ingresopresupuestal.estado =='Procesado':

                    if 'institucioneducativaid' in request.data.keys():
                        request.data['institucioneducativaid'] = ingresopresupuestal.institucioneducativaid.id
                    else:
                        return Response("falta el nodo institucioneducativaid",status = status.HTTP_400_BAD_REQUEST) 

                    if 'consecutivo' in request.data.keys():
                        request.data['consecutivo'] = ingresopresupuestal.consecutivo
                    else:
                        return Response("falta el nodo consecutivo",status = status.HTTP_400_BAD_REQUEST)

                    if 'fecha' in request.data.keys():
                        request.data['fecha'] = ingresopresupuestal.fecha
                    else:
                        return Response("falta el nodo fecha",status = status.HTTP_400_BAD_REQUEST)
                    
                    if 'estado' in request.data.keys():
                        request.data['estado'] = ingresopresupuestal.estado 

                    if 'terceroid' in request.data.keys():
                        terceroid = request.data.pop('terceroid')
                        if 'codigo' in terceroid.keys(): 
                            tercero = Tercero.objects.filter(codigo = terceroid['codigo']).first()
                            if tercero:
                                request.data.update({"terceroid" : tercero.id})
                            else:
                                return Response('tercero no existe',status = status.HTTP_400_BAD_REQUEST) 
                        else:
                            return Response('falta el nodo codigo para el tercero',status = status.HTTP_400_BAD_REQUEST) 
                    else:
                        return Response('falta el nodo terceroid',status = status.HTTP_400_BAD_REQUEST) 

                    if 'fuenterecursoid' in request.data.keys():
                        fuenterecursoid = request.data.pop('fuenterecursoid')
                        fuenterecurso = buscarfuenterecurso_final(fuenterecursoid)
                        if fuenterecurso:                            
                            if buscarfuenterecursoproyeccion(fuenterecurso.id,ingresopresupuestal.institucioneducativaid.id)==True:                                
                                if ingresopresupuestal.valor != request.data['valor'] or ingresopresupuestal.fuenterecursoid.id != fuenterecurso.id:                                    
                                    if saldofuenterecursoporingreso_mod(ingresopresupuestal , request.data['valor'])==True:
                                        request.data.update({"fuenterecursoid" : fuenterecurso.id})
                                    else:
                                        return Response('fuente recurso supera el valor de la proyeccion presupuestal asignada para el periodo',status = status.HTTP_400_BAD_REQUEST)
                                else:
                                    request.data.update({"fuenterecursoid" : fuenterecurso.id})
                            else:
                                return Response('fuente recurso no tiene proyeccion presupuestal asignada o el periodo esta cerrado',status = status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response('fuente recurso no es de detalle',status = status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response('falta el nodo fuenterecursoid para buscar la fuente de recurso',status = status.HTTP_400_BAD_REQUEST)
                    ingresopresupuestal_serializers = Ingresopresupuestalserializers(ingresopresupuestal,data = request.data)
                    
                    if ingresopresupuestal_serializers.is_valid():
                        ingresopresupuestal_serializers.save()
                        return Response(ingresopresupuestal_serializers.data,status = status.HTTP_200_OK)
                    return Response(ingresopresupuestal_serializers.errors, status = status.HTTP_400_BAD_REQUEST)
                return Response('Ingreso presupuestal no se puede actualizar en este Estado',status = status.HTTP_400_BAD_REQUEST) 
            return Response('Ingreso presupuestal no puede ser Actualizar esta asociado a un documento de recaudo',status = status.HTTP_400_BAD_REQUEST)          
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

def saldoingresoporrecaudo_mod(recaudopresupuestal,consecutivo):
    totalingreso = 0
    saldo = 0
    totalrecaudo = 0
    ingresopresupuestal = Ingresopresupuestal.objects.filter(institucioneducativaid = recaudopresupuestal.institucioneducativaid.id, consecutivo = consecutivo).first()
 
    if ingresopresupuestal:
        totalingreso = ingresopresupuestal.valor
        recaudopresupuestal_query = Recaudopresupuestal.objects.filter(ingresopresupuestalid = ingresopresupuestal.id, estado ='Procesado').exclude(id = recaudopresupuestal.id).values('ingresopresupuestalid').annotate(total=Sum('valor'))
        if recaudopresupuestal_query :
            totalrecaudo = recaudopresupuestal_query[0]['total']

    saldo = totalingreso  - totalrecaudo

    return saldo

@api_view(['GET'])
def consultaintegral_dcoumentos_api_view(request):
    if request.method =='GET':
        
        tipodocumento = 0
        institucioneducativaid =0
        estado = 'Procesado'

        if 'tipodocumento' in request.data.keys():
            tipodocumento = request.data.pop('tipodocumento')

        if 'fechainicial' in request.data.keys():
            fechainicial = request.data.pop('fechainicial')

        if 'fechafinal' in request.data.keys():
            fechafinal = request.data.pop('fechafinal')

        if 'estado' in request.data.keys():
            estado = request.data.pop('estado')
        

        if 'institucioneducativaid' in request.data.keys():
            institucioneducativa_id = request.data.pop('institucioneducativaid')
            if 'codigo' in institucioneducativa_id.keys():
                institucioneducativa = Institucioneducativa.objects.filter(codigo = institucioneducativa_id['codigo']).first() 
                if institucioneducativa:
                    institucioneducativaid = institucioneducativa.id
                else:
                    return Response("institucion educativa ingresada no existe",status = status.HTTP_400_BAD_REQUEST)                     
            else:
                return Response("falta el nodo codigo para institucion educativa",status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response("falta el nodo institucioneducativaid",status = status.HTTP_400_BAD_REQUEST)

        #1-Ingreso Presupuestal
        if tipodocumento == 1:
            ingresopresupuestal = Ingresopresupuestal.objects.filter(institucioneducativaid = institucioneducativaid
            , fecha__gte=fechainicial
            , fecha__lte=fechafinal
            , estado=estado).all()
            
            ingresopresupuestal_serializers = Ingresopresupuestalserializers(ingresopresupuestal, many = True)
            return Response(ingresopresupuestal_serializers.data,status = status.HTTP_200_OK)
        #2-Recaudo Presupuestal
        elif tipodocumento == 2:
            recaudopresupuestal = Recaudopresupuestal.objects.filter(institucioneducativaid = institucioneducativaid
            , fecha__gte=fechainicial
            , fecha__lte=fechafinal
            , estado=estado).all()

            recaudopresupuestal_serializers = Recaudopresupuestalserializers(recaudopresupuestal, many = True)
            return Response(recaudopresupuestal_serializers.data,status = status.HTTP_200_OK)
        #3-Solicitud Presupuestal
        elif tipodocumento == 3:
            
            solicitudpresupuestalcabecera = Solicitudpresupuestalcabecera.objects.filter(institucioneducativaid = institucioneducativaid
            , fecha__gte=fechainicial
            , fecha__lte=fechafinal
            , estado=estado).all()

            solicitudpresupuestalcabeceraSerializers = SolicitudpresupuestalcabeceraSerializers(solicitudpresupuestalcabecera, many = True)
            return Response(solicitudpresupuestalcabeceraSerializers.data,status = status.HTTP_200_OK)

        #4-CDP
        elif tipodocumento == 4:
            certificadodisponibilidadpresupuestal = Certificadodisponibilidadpresupuestal.objects.filter(institucioneducativaid = institucioneducativaid
            , fecha__gte=fechainicial
            , fecha__lte=fechafinal
            , estado=estado).all()
         
            certificadodisponibilidadpresupuestalSerializers = CertificadodisponibilidadpresupuestalSerializers(certificadodisponibilidadpresupuestal, many = True)
            return Response(certificadodisponibilidadpresupuestalSerializers.data,status = status.HTTP_200_OK)

        #5-RP
        elif tipodocumento == 5:
            registropresupuestal = Registropresupuestal.objects.filter(institucioneducativaid = institucioneducativaid
            , fecha__gte=fechainicial
            , fecha__lte=fechafinal
            , estado=estado).all()
         
            registropresupuestalserializers = Registropresupuestalserializers(registropresupuestal, many = True)
            return Response(registropresupuestalserializers.data,status = status.HTTP_200_OK)

        #6-OP 
        elif tipodocumento == 6:
            obligacionpresupuestal = Obligacionpresupuestal.objects.filter(institucioneducativaid = institucioneducativaid
            , fecha__gte=fechainicial
            , fecha__lte=fechafinal
            , estado=estado).all()
         
            obligacionpresupuestalSerializers = ObligacionpresupuestalSerializers(obligacionpresupuestal, many = True)
            return Response(obligacionpresupuestalSerializers.data,status = status.HTTP_200_OK)
        #7-PP 
        elif tipodocumento == 7:
            pagopresupuestal = Pagopresupuestal.objects.filter(institucioneducativaid = institucioneducativaid
            , fecha__gte=fechainicial
            , fecha__lte=fechafinal
            , estado=estado).all()
         
            pagopresupuestalSerializers = PagopresupuestalSerializers(pagopresupuestal, many = True)
            return Response(pagopresupuestalSerializers.data,status = status.HTTP_200_OK)

        #8-proyeccion presupuestal
        elif tipodocumento == 8:
            return Response("En Construccion",status = status.HTTP_400_BAD_REQUEST)
            #proyeccionpresupuestalcabecera = Proyeccionpresupuestalcabecera.objects.filter(institucioneducativaid = institucioneducativaid
            #, fecha__gte=fechainicial
            #, fecha__lte=fechafinal
            #, estado=estado).all()
         #
            #proyeccionpresupuestalcabeceraSerializers = ProyeccionpresupuestalcabeceraSerializers(proyeccionpresupuestalcabecera, many = True)
            #return Response(proyeccionpresupuestalcabeceraSerializers.data,status = status.HTTP_200_OK)

        #9-Modificacion Presupuestal 
        elif tipodocumento == 9:
            #modificacionproyeccionpresupuestalcabecera = Modificacionproyeccionpresupuestalcabecera.objects.filter(institucioneducativaid = institucioneducativaid
            #, fecha__gte=fechainicial
            #, fecha__lte=fechafinal
            #, estado=estado).all()
         #
            #modificacionproyeccionpresupuestalcabeceraSerializers = ModificacionproyeccionpresupuestalcabeceraSerializers(modificacionproyeccionpresupuestalcabecera, many = True)
            #return Response(modificacionproyeccionpresupuestalcabeceraSerializers.data,status = status.HTTP_200_OK)
            
            return Response("En Construccion",status = status.HTTP_400_BAD_REQUEST)

        else:
            return Response("Seleccione un tipo de documento correcto",status = status.HTTP_400_BAD_REQUEST)







