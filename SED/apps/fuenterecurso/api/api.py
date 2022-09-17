from itertools import count
from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from apps.fuenterecurso.models import Fuenterecurso
from apps.fuenterecurso.api.serializers import Fuenterecursoserializers
from django.db.models.deletion import RestrictedError
from apps.proyeccionpresupuestaldetalle.models import Proyeccionpresupuestaldetalle
from apps.proyeccionpresupuestaldetalle.api.serializers import ProyeccionpresupuestaldetalleSerializers
from apps.periodo.models import Periodo
from apps.periodo.api.serializers import Periodoserializers
from apps.proyeccionpresupuestalcabecera.models import Proyeccionpresupuestalcabecera
from apps.proyeccionpresupuestalcabecera.api.serializers import ProyeccionpresupuestalcabeceraSerializers
from apps.ingresopresupuestal.models import Ingresopresupuestal
from apps.institucioneducativa.models import Institucioneducativa
from apps.institucioneducativa.api.serializers import InstitucioneducativaSerializer
from django.db.models import Count,Sum
from apps.modificacionproyeccionpresupuestalcabecera.models import Modificacionproyeccionpresupuestalcabecera
from apps.modificacionproyeccionpresupuestaldetalle.models import Modificacionproyeccionpresupuestaldetalle
from apps.recaudopresupuestal.models import Recaudopresupuestal
from apps.solicitudpresupuestalcabecera.models import Solicitudpresupuestalcabecera
from apps.solicitudpresupuestaldetalle.models import Solicitudpresupuestaldetalle


@api_view(['GET','POST'])
def fuenterecurso_api_view(request):

    if request.method =='GET':
        fuenterecurso = Fuenterecurso.objects.all()
        fuenterecurso_serializer = Fuenterecursoserializers (fuenterecurso, many = True)
        return Response(fuenterecurso_serializer.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        if 'idpadre' in request.data.keys():
            idpadre = request.data.pop('idpadre')
            if 'codigo' in idpadre.keys():
                fuentepadre = Fuenterecurso.objects.filter(codigo = idpadre['codigo']).first()
                if fuentepadre:
                    idpadre_serializers = Fuenterecursoserializers(fuentepadre)
                    idpadre = dict(idpadre_serializers.data)
                    if Proyeccionpresupuestaldetalle.objects.filter(fuenterecursoid = idpadre['id']).count()==0:
                        request.data.update({'idpadre':idpadre['id']})

                        fuenterecurso_serializer = Fuenterecursoserializers(data = request.data)
                        if fuenterecurso_serializer.is_valid():
                            fuenterecurso_serializer.save()
                            return Response(fuenterecurso_serializer.data,status = status.HTTP_201_CREATED)
                        return Response(fuenterecurso_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                    return Response('fuente recurso padre ingresado no puede ser asociado ya tiene movimiento como fuente detalle',status = status.HTTP_400_BAD_REQUEST)
                return Response('fuente recurso padre ingresado no existe',status = status.HTTP_400_BAD_REQUEST)
            return Response('falta nodo codigo de la fuente recurso padre',status = status.HTTP_400_BAD_REQUEST)
        else: 
            if Fuenterecurso.objects.all().count()==0:          
                fuenterecurso_serializer = Fuenterecursoserializers(data = request.data)
                if fuenterecurso_serializer.is_valid():
                    fuenterecurso_serializer.save()
                    return Response(fuenterecurso_serializer.data,status = status.HTTP_201_CREATED)
                return Response(fuenterecurso_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response('solo puede exitir una fuente de recuerso de cabecera',status = status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','PUT','DELETE'])
def fuenterecurso_details_api_view(request, codigo = None):
    
    fuenterecurso = Fuenterecurso.objects.filter(codigo=codigo).first()
    if fuenterecurso:
        if request.method == 'GET':            
            fuenterecurso_serializers = Fuenterecursoserializers(fuenterecurso)
            return Response(fuenterecurso_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT':            
            if 'codigo' in request.data.keys(): 
                request.data['codigo'] = codigo          
                if 'idpadre' in request.data.keys():
                    idpadre = request.data.pop('idpadre')
                    if 'codigo' in idpadre.keys():
                        if codigo != idpadre['codigo']:
                            fuentepadre = Fuenterecurso.objects.filter(codigo = idpadre['codigo']).first()
                            if fuentepadre:
                                idpadre_serializers = Fuenterecursoserializers(fuentepadre)
                                idpadre = dict(idpadre_serializers.data)
                                if Proyeccionpresupuestaldetalle.objects.filter(fuenterecursoid = idpadre['id']).count()==0:
                                    request.data.update({'idpadre':idpadre['id']})
                                    fuenterecurso_serializer = Fuenterecursoserializers(fuenterecurso,data = request.data)
                                    if fuenterecurso_serializer.is_valid():
                                        fuenterecurso_serializer.save()
                                        return Response(fuenterecurso_serializer.data,status = status.HTTP_201_CREATED)
                                    return Response(fuenterecurso_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                                return Response('fuente recurso padre ingresado no puede ser asociado ya tiene movimiento como fuente detalle',status = status.HTTP_400_BAD_REQUEST)
                            return Response('fuente recurso padre ingresado no existe',status = status.HTTP_400_BAD_REQUEST)
                        return Response('fuente de recuerso padre ingresado no puede ser igual al codigo de la fuente de recurso a modificar',status = status.HTTP_400_BAD_REQUEST)
                    return Response('falta nodo codigo de la fuente recurso padre',status = status.HTTP_400_BAD_REQUEST)
                else:                    
                    fuenterecurso_serializer = Fuenterecursoserializers(fuenterecurso,data = request.data)
                    if fuenterecurso_serializer.is_valid():
                        fuenterecurso_serializer.save()
                        return Response(fuenterecurso_serializer.data,status = status.HTTP_201_CREATED)
                    return Response(fuenterecurso_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo codigo',status = status.HTTP_400_BAD_REQUEST) 
        elif request.method == 'DELETE':
            fuenterecurso_serializers = Fuenterecursoserializers(fuenterecurso)
            if Fuenterecurso.objects.filter(idpadre = fuenterecurso_serializers.data['id']).count() == 0:
                try:
                    fuenterecurso.delete()
                    return Response('fuente recurso eliminado Correctamente',status = status.HTTP_200_OK)
                except RestrictedError:
                    return Response('fuente recurso no puede ser eliminado esta asociado a un documento',status = status.HTTP_400_BAD_REQUEST)            
            return Response('fuente recurso no puede ser eliminado esta asociado como padre a otra fuente de recurso',status = status.HTTP_400_BAD_REQUEST)
    return Response('fuente recurso no existe',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def fuenterecurso_final_api_view(request):

    if request.method =='GET':
        data = Fuenterecurso.objects.all()        
        fuenterecurso_serializer = Fuenterecursoserializers(data, many=True)
        list_fuentes = [fuente for fuente in fuenterecurso_serializer.data if Fuenterecurso.objects.filter(idpadre = fuente['id']).count() == 0]  
        return Response(list_fuentes,status = status.HTTP_200_OK)

def buscarfuenterecurso_final(data):

    fuenterecurso = Fuenterecurso.objects.filter(codigo = data['codigo']).first()
    if fuenterecurso:
        if Fuenterecurso.objects.filter(idpadre = fuenterecurso.id).count()==0:
            return fuenterecurso

def buscarfuenterecursoproyeccion(fuenterecursoid, institucioneducativaid):
    
    periodo = Periodo.objects.filter(activo = True).first()
    fuenteproyectada = False    

    if periodo:
        
        proyeccionpresupuestalcabecera = Proyeccionpresupuestalcabecera.objects.filter(periodoid=periodo.id, institucioneducativaid = institucioneducativaid, estado = 'Aprobado' ).first() 
        
        if proyeccionpresupuestalcabecera:           
            if Proyeccionpresupuestaldetalle.objects.filter(fuenterecursoid = fuenterecursoid, proyeccionpresupuestalid = proyeccionpresupuestalcabecera.id).count()>0:
                fuenteproyectada =  True         

        #se agregan las modificaciones
        modificacionproyeccionpresupuestalcabecera = Modificacionproyeccionpresupuestalcabecera.objects.filter(periodoid = periodo.id, institucioneducativaid = institucioneducativaid , estado ='Procesado').first()
        if modificacionproyeccionpresupuestalcabecera:                
            if Modificacionproyeccionpresupuestaldetalle.objects.filter(fuenterecursoid = fuenterecursoid , modificacionproyeccionpresupuestalid = modificacionproyeccionpresupuestalcabecera.id).count()>0:
                fuenteproyectada =  True 
             
    

    return fuenteproyectada  

def buscarfuenterecursoingresopresupuestal(fuenterecursoid, institucioneducativaid):
    codigoperiodo = 0
    periodo = Periodo.objects.filter(activo = True).first()
    if periodo:
        periodo_serializers = Periodoserializers(periodo)
        periodo = dict(periodo_serializers.data)
        codigoperiodo = periodo['codigo']        
         
    ingresopresupuestal = Ingresopresupuestal.objects.filter(fuenterecursoid = fuenterecursoid, institucioneducativaid = institucioneducativaid, fecha__year = codigoperiodo, estado = 'Procesado').first()
    
    if ingresopresupuestal:
        return True         
    else:
        return False    
    

@api_view(['GET'])
def fuenterecurso_proyeccion_api_view(request, codigoinstitucioneducativa = None):
    
    if request.method =='GET':
        codigoperiodo = 0
        periodo = Periodo.objects.filter(activo = True).first()
        if periodo:
            codigoperiodo = periodo.id

        institucioneducativa_parametros = Institucioneducativa.objects.filter(codigo = codigoinstitucioneducativa).first()

        if institucioneducativa_parametros:            
            proyeccionpresupuestalcabecera = Proyeccionpresupuestalcabecera.objects.filter(periodoid=codigoperiodo, institucioneducativaid = institucioneducativa_parametros.id, estado ='Aprobado').first() 

            if proyeccionpresupuestalcabecera:   
                proyeccionpresupuestaldetalle = Proyeccionpresupuestaldetalle.objects.filter(proyeccionpresupuestalid = proyeccionpresupuestalcabecera.id).values('fuenterecursoid').annotate(total=Count('fuenterecursoid')).order_by()
                list_fuentes = [Fuenterecursoserializers(Fuenterecurso.objects.filter(id = fuente['fuenterecursoid']).first()).data for fuente in proyeccionpresupuestaldetalle] 
                return Response(list_fuentes,status = status.HTTP_200_OK)
            return Response('no existen datos',status = status.HTTP_400_BAD_REQUEST)
        return Response('Insitutcion educativa no existe',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def saldofuenterecursoporingreso_api_view(request):
    parametros = dict(request.query_params)
    if request.method =='GET':
        codigofuenterecurso=""
        fuenterecurso_parametros =""
        codigoinstitucioneducativa = ""
        institucioneducativa_parametros = ""
        
        saldo = 0
        codigoperiodo = 0
        periodoid = 0
        periodo = Periodo.objects.filter(activo = True).first()
        totalproyeccion = 0
        totalingreso = 0
        totalmodificaciones=0

        if periodo:
            periodoid = periodo.id
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
        
        if 'codigofuenterecurso' in parametros.keys():
            codigofuenterecurso = str(parametros["codigofuenterecurso"][0])
            codigofuenterecurso = codigofuenterecurso.upper()

            fuenterecurso_parametros = Fuenterecurso.objects.filter(codigo = codigofuenterecurso).first()
            if fuenterecurso_parametros : 
                fuenterecurso_parametros_serializers = Fuenterecursoserializers(fuenterecurso_parametros)
                fuenterecurso_parametros = dict(fuenterecurso_parametros_serializers.data)
            else:
                fuenterecurso_parametros = dict({"id":0})
        else:
            fuenterecurso_parametros = dict({"id":0})

        proyeccionpresupuestalcabecera = Proyeccionpresupuestalcabecera.objects.filter(periodoid=periodoid, institucioneducativaid = institucioneducativa_parametros['id'],estado ='Aprobado' ).first() 
        
        if proyeccionpresupuestalcabecera:           
            proyeccionpresupuestaldetalle = Proyeccionpresupuestaldetalle.objects.filter(fuenterecursoid = fuenterecurso_parametros['id'],proyeccionpresupuestalid = proyeccionpresupuestalcabecera.id).values('fuenterecursoid').annotate(total=Sum('valor')).order_by()
            if proyeccionpresupuestaldetalle:
                totalproyeccion =proyeccionpresupuestaldetalle[0]['total']
                
        ingresopresupuestal = Ingresopresupuestal.objects.filter(fuenterecursoid = fuenterecurso_parametros['id'], institucioneducativaid = institucioneducativa_parametros['id'], fecha__year = codigoperiodo, estado ='Procesado').values('fuenterecursoid').annotate(total=Sum('valor'))
        if ingresopresupuestal:
            totalingreso = ingresopresupuestal[0]['total']
        else:
            totalingreso = 0

        #se agregan las modificaciones
        modificacionproyeccionpresupuestalcabecera = Modificacionproyeccionpresupuestalcabecera.objects.filter(periodoid=periodoid, institucioneducativaid = institucioneducativa_parametros['id'] ,estado ='Procesado').first()
        if modificacionproyeccionpresupuestalcabecera:                
            modificacionproyeccionpresupuestaldetalle = Modificacionproyeccionpresupuestaldetalle.objects.filter(fuenterecursoid = fuenterecurso_parametros['id'],modificacionproyeccionpresupuestalid = modificacionproyeccionpresupuestalcabecera.id).values('fuenterecursoid').annotate(total=Sum('valor')).order_by()
            if modificacionproyeccionpresupuestaldetalle:
                totalmodificaciones = modificacionproyeccionpresupuestaldetalle[0]['total']
        
        saldo = (totalproyeccion + totalmodificaciones) - totalingreso 
        return Response(saldo,status = status.HTTP_200_OK)
          

def saldofuenterecursoporingreso(fuenterecursoid, institucioneducativaid,valoractual):
    saldo = 0
    codigoperiodo = 0
    periodoid = 0
    periodo = Periodo.objects.filter(activo = True).first()
    totalproyeccion=0
    totalingreso=0
    totalmodificaciones=0
    if periodo:
        periodoid = periodo.id
        codigoperiodo = periodo.codigo
    
    proyeccionpresupuestalcabecera = Proyeccionpresupuestalcabecera.objects.filter(periodoid=periodoid, institucioneducativaid = institucioneducativaid ,estado ='Aprobado').first() 

    if proyeccionpresupuestalcabecera:           
        proyeccionpresupuestaldetalle = Proyeccionpresupuestaldetalle.objects.filter(fuenterecursoid = fuenterecursoid,proyeccionpresupuestalid = proyeccionpresupuestalcabecera.id).values('fuenterecursoid').annotate(total=Sum('valor')).order_by()
        if proyeccionpresupuestaldetalle:
            totalproyeccion =proyeccionpresupuestaldetalle[0]['total']

    ingresopresupuestal = Ingresopresupuestal.objects.filter(fuenterecursoid = fuenterecursoid, institucioneducativaid = institucioneducativaid, fecha__year = codigoperiodo, estado ='Procesado').values('fuenterecursoid').annotate(total=Sum('valor'))
    if ingresopresupuestal:
        totalingreso = ingresopresupuestal[0]['total']
    else:
        totalingreso = 0

    #se agregan las modificaciones
    modificacionproyeccionpresupuestalcabecera = Modificacionproyeccionpresupuestalcabecera.objects.filter(periodoid=periodoid, institucioneducativaid = institucioneducativaid ,estado ='Procesado').first()
    if modificacionproyeccionpresupuestalcabecera:                
        modificacionproyeccionpresupuestaldetalle = Modificacionproyeccionpresupuestaldetalle.objects.filter(fuenterecursoid = fuenterecursoid,modificacionproyeccionpresupuestalid = modificacionproyeccionpresupuestalcabecera.id).values('fuenterecursoid').annotate(total=Sum('valor')).order_by()
        if modificacionproyeccionpresupuestaldetalle:
            totalmodificaciones = modificacionproyeccionpresupuestaldetalle[0]['total']

    
    saldo = (totalproyeccion + totalmodificaciones) - (totalingreso + valoractual)
    
    if saldo >= 0:
        return True
    else:
        return False

def saldofuenterecursoporingreso_elim(fuenterecursoid, institucioneducativaid):
    saldo = 0
    codigoperiodo = 0
    periodoid = 0
    periodo = Periodo.objects.filter(activo = True).first()
    totalproyeccion=0
    totalingreso=0
    totalmodificaciones=0
    if periodo:
        periodoid = periodo.id
        codigoperiodo = periodo.codigo
    
    proyeccionpresupuestalcabecera = Proyeccionpresupuestalcabecera.objects.filter(periodoid=periodoid, institucioneducativaid = institucioneducativaid ,estado ='Aprobado').first() 
    
    if proyeccionpresupuestalcabecera:           
        proyeccionpresupuestaldetalle = Proyeccionpresupuestaldetalle.objects.filter(fuenterecursoid = fuenterecursoid,proyeccionpresupuestalid = proyeccionpresupuestalcabecera.id).values('fuenterecursoid').annotate(total=Sum('valor')).order_by()
        if proyeccionpresupuestaldetalle:
            totalproyeccion =proyeccionpresupuestaldetalle[0]['total']

    ingresopresupuestal = Ingresopresupuestal.objects.filter(fuenterecursoid = fuenterecursoid, institucioneducativaid = institucioneducativaid, fecha__year = codigoperiodo, estado ='Procesado').values('fuenterecursoid').annotate(total=Sum('valor'))
    if ingresopresupuestal:
        totalingreso = ingresopresupuestal[0]['total']
    else:
        totalingreso = 0

    #se agregan las modificaciones
    modificacionproyeccionpresupuestalcabecera = Modificacionproyeccionpresupuestalcabecera.objects.filter(periodoid=periodoid, institucioneducativaid = institucioneducativaid ,estado ='Procesado').first()
    if modificacionproyeccionpresupuestalcabecera:                
        modificacionproyeccionpresupuestaldetalle = Modificacionproyeccionpresupuestaldetalle.objects.filter(fuenterecursoid = fuenterecursoid,modificacionproyeccionpresupuestalid = modificacionproyeccionpresupuestalcabecera.id).values('fuenterecursoid').annotate(total=Sum('valor')).order_by()
        if modificacionproyeccionpresupuestaldetalle:
            totalmodificaciones = modificacionproyeccionpresupuestaldetalle[0]['total']

    
    saldo = (totalproyeccion + totalmodificaciones) - (totalingreso)
    
    return saldo
    

def saldofuenterecursoporingreso_mod(ingresopresupuestal,valoractual):
    saldo = 0
    codigoperiodo = 0
    periodoid = 0
    periodo = Periodo.objects.filter(activo = True).first()
    totalproyeccion=0
    totalingreso=0
    totalmodificaciones=0
    if periodo:
        periodoid = periodo.id
        codigoperiodo = periodo.codigo
    
    proyeccionpresupuestalcabecera = Proyeccionpresupuestalcabecera.objects.filter(periodoid=periodoid, institucioneducativaid = ingresopresupuestal.institucioneducativaid.id ,estado ='Aprobado').first() 

    if proyeccionpresupuestalcabecera:           
        proyeccionpresupuestaldetalle = Proyeccionpresupuestaldetalle.objects.filter(fuenterecursoid = ingresopresupuestal.fuenterecursoid.id,proyeccionpresupuestalid = proyeccionpresupuestalcabecera.id).values('fuenterecursoid').annotate(total=Sum('valor')).order_by()
        if proyeccionpresupuestaldetalle:
            totalproyeccion =proyeccionpresupuestaldetalle[0]['total']
            
    ingresopresupuestal_query = Ingresopresupuestal.objects.filter(fuenterecursoid = ingresopresupuestal.fuenterecursoid.id, institucioneducativaid = ingresopresupuestal.institucioneducativaid.id, fecha__year = codigoperiodo, estado ='Procesado').exclude(id = ingresopresupuestal.id).values('fuenterecursoid').annotate(total=Sum('valor'))
    if ingresopresupuestal_query:
        totalingreso = ingresopresupuestal_query[0]['total']
    else:
        totalingreso = 0
            
    #se agregan las modificaciones
    modificacionproyeccionpresupuestalcabecera = Modificacionproyeccionpresupuestalcabecera.objects.filter(periodoid=periodoid, institucioneducativaid = ingresopresupuestal.institucioneducativaid.id ,estado ='Procesado').first()
    if modificacionproyeccionpresupuestalcabecera:                
        modificacionproyeccionpresupuestaldetalle = Modificacionproyeccionpresupuestaldetalle.objects.filter(fuenterecursoid = ingresopresupuestal.fuenterecursoid.id,modificacionproyeccionpresupuestalid = modificacionproyeccionpresupuestalcabecera.id).values('fuenterecursoid').annotate(total=Sum('valor')).order_by()
        if modificacionproyeccionpresupuestaldetalle:
            totalmodificaciones = modificacionproyeccionpresupuestaldetalle[0]['total']

    saldo = (totalproyeccion + totalmodificaciones) - (totalingreso + valoractual)
            
    if saldo >= 0:
        return True
    else:
        return False

def saldo_fuente_recaudos(institucioneducativaid,fuenterecursoid):
    codigoperiodo = 0
    periodo = Periodo.objects.filter(activo = True).first()
    saldo = 0
    periodoid= 0
    totalsolicitudes = 0
    totalrecaudos = 0
    if periodo:
        periodoid = periodo.id
        codigoperiodo = periodo.codigo     

    ingresos = Ingresopresupuestal.objects.filter(institucioneducativaid = institucioneducativaid, fecha__year = codigoperiodo,fuenterecursoid = fuenterecursoid, estado ='Procesado').all() 
    for ingresopresupuestal in ingresos:            
        recaudos = Recaudopresupuestal.objects.filter(ingresopresupuestalid = ingresopresupuestal.id, estado ='Procesado').values('ingresopresupuestalid').annotate(total=Sum('valor'))
        if recaudos:
            totalrecaudos = totalrecaudos + recaudos[0]['total']

    solicitudes = Solicitudpresupuestalcabecera.objects.filter(institucioneducativaid = institucioneducativaid,fecha__year = codigoperiodo, estado = 'Procesado').all()
   
    for solicitud in solicitudes:
        solicitudpresupuestaldetalle = Solicitudpresupuestaldetalle.objects.filter(fuenterecursoid=fuenterecursoid,solicitudpresupuestalcabeceraid=solicitud.id).values('fuenterecursoid').annotate(total=Sum('valor')).order_by()
        if solicitudpresupuestaldetalle:
            totalsolicitudes = totalsolicitudes + solicitudpresupuestaldetalle[0]['total']

    saldo = totalrecaudos - totalsolicitudes

    return saldo

@api_view(['GET'])
def saldofuenterecursoporrecaudos_api_view(request):
    parametros = dict(request.query_params)
    if request.method =='GET':
        codigofuenterecurso=""        
        codigoinstitucioneducativa = ""        
        institucioneducativaid = 0
        fuenterecursoid = 0

        saldo = 0
        
        
        if 'codigoinstitucioneducativa' in parametros.keys():
            codigoinstitucioneducativa = str(parametros["codigoinstitucioneducativa"][0])
            codigoinstitucioneducativa = codigoinstitucioneducativa.upper() 
            
            institucioneducativa = Institucioneducativa.objects.filter(codigo =codigoinstitucioneducativa).first()
            if institucioneducativa:  
                institucioneducativaid = institucioneducativa.id
            else:
                return Response('institucion educativa no existe',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('institucion educativa no existe',status = status.HTTP_400_BAD_REQUEST)        
        
        if 'codigofuenterecurso' in parametros.keys():
            codigofuenterecurso = str(parametros["codigofuenterecurso"][0])
            codigofuenterecurso = codigofuenterecurso.upper()

            fuenterecurso = Fuenterecurso.objects.filter(codigo = codigofuenterecurso).first()
            if fuenterecurso: 
                fuenterecursoid = fuenterecurso.id
            else:
                return Response('Fuente recurso no existe',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Fuente recurso no existe',status = status.HTTP_400_BAD_REQUEST)

        

        saldo = saldo_fuente_recaudos(institucioneducativaid,fuenterecursoid)

        return Response(saldo,status = status.HTTP_200_OK)

