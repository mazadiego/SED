from itertools import count
from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status


from apps.rubropresupuestal.models import Rubropresupuestal
from apps.rubropresupuestal.api.serializers import Rubropresupuestalserializers
from django.db.models.deletion import RestrictedError
from apps.proyeccionpresupuestaldetalle.models import Proyeccionpresupuestaldetalle
from apps.periodo.models import Periodo
from apps.proyeccionpresupuestalcabecera.models import Proyeccionpresupuestalcabecera
from django.db.models import Count,Sum
from apps.solicitudpresupuestalcabecera.models import Solicitudpresupuestalcabecera
from apps.solicitudpresupuestaldetalle.models import Solicitudpresupuestaldetalle
from apps.institucioneducativa.models import Institucioneducativa
from apps.certificadodisponibilidadpresupuestal.models import Certificadodisponibilidadpresupuestal
from apps.ingresopresupuestal.models import Ingresopresupuestal
from apps.recaudopresupuestal.models import Recaudopresupuestal

@api_view(['GET','POST'])
def rubropresupuestal_api_view(request):

    if request.method =='GET':
        rubropresupuestal = Rubropresupuestal.objects.all()
        rubropresupuestal_serializer = Rubropresupuestalserializers (rubropresupuestal, many = True)
        return Response(rubropresupuestal_serializer.data,status = status.HTTP_200_OK)
    
    elif request.method =='POST':
        if 'idpadre' in request.data.keys():
            idpadre = request.data.pop('idpadre')
            if 'codigo' in idpadre.keys():
                rubropadre = Rubropresupuestal.objects.filter(codigo = idpadre['codigo']).first()
                if rubropadre:
                    idpadre_serializers = Rubropresupuestalserializers(rubropadre)
                    idpadre = dict(idpadre_serializers.data)
                    if Proyeccionpresupuestaldetalle.objects.filter(rubropresupuestalid = idpadre['id']).count()==0:
                        request.data.update({'idpadre':idpadre['id']})
                        rubropresupuestal_serializer = Rubropresupuestalserializers(data = request.data)
                        if rubropresupuestal_serializer.is_valid():
                            rubropresupuestal_serializer.save()
                            return Response(rubropresupuestal_serializer.data,status = status.HTTP_201_CREATED)
                        return Response(rubropresupuestal_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                    return Response('rubro presupuestal padre ingresado no puede ser asociado ya tiene movimiento como rubro detalle',status = status.HTTP_400_BAD_REQUEST)
                return Response('rubro presupuestal padre ingresado no existe',status = status.HTTP_400_BAD_REQUEST)
            return Response('falta nodo codigo del rubro presupuestal padre',status = status.HTTP_400_BAD_REQUEST)
        else: 
            if Rubropresupuestal.objects.all().count()==0:          
                rubropresupuestal_serializer = Rubropresupuestalserializers(data = request.data)
                if rubropresupuestal_serializer.is_valid():
                    rubropresupuestal_serializer.save()
                    return Response(rubropresupuestal_serializer.data,status = status.HTTP_201_CREATED)
                return Response(rubropresupuestal_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response('solo puede exitir un rubro presupuetal de cabecera',status = status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','PUT','DELETE'])
def rubropresupuestal_details_api_view(request, codigo = None):
    
    rubropresupuestal = Rubropresupuestal.objects.filter(codigo=codigo).first()
    if rubropresupuestal:
        if request.method == 'GET':            
            rubropresupuestal_serializers = Rubropresupuestalserializers(rubropresupuestal)
            return Response(rubropresupuestal_serializers.data,status = status.HTTP_200_OK)

        elif request.method == 'PUT':            
            if 'codigo' in request.data.keys(): 
                request.data['codigo'] = codigo          
                if 'idpadre' in request.data.keys():
                    idpadre = request.data.pop('idpadre')
                    if 'codigo' in idpadre.keys():
                        if codigo != idpadre['codigo']:
                            rubropadre = Rubropresupuestal.objects.filter(codigo = idpadre['codigo']).first()
                            if rubropadre:
                                idpadre_serializers = Rubropresupuestalserializers(rubropadre)
                                idpadre = dict(idpadre_serializers.data)
                                if Proyeccionpresupuestaldetalle.objects.filter(rubropresupuestalid = idpadre['id']).count()==0:
                                    request.data.update({'idpadre':idpadre['id']})

                                    rubropresupuestal_serializer = Rubropresupuestalserializers(rubropresupuestal,data = request.data)
                                    if rubropresupuestal_serializer.is_valid():
                                        rubropresupuestal_serializer.save()
                                        return Response(rubropresupuestal_serializer.data,status = status.HTTP_201_CREATED)
                                    return Response(rubropresupuestal_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                                return Response('rubro presupuestal padre ingresado no puede ser asociado ya tiene movimiento como rubro detalle',status = status.HTTP_400_BAD_REQUEST)
                            return Response('rubro presupuestal padre ingresado no existe',status = status.HTTP_400_BAD_REQUEST)
                        return Response('rubro presupuestal padre ingresado no puede ser igual al codigo del rubro',status = status.HTTP_400_BAD_REQUEST)
                    return Response('falta nodo codigo del rubro presupuestal padre',status = status.HTTP_400_BAD_REQUEST)
                else:                    
                    rubropresupuestal_serializer = Rubropresupuestalserializers(rubropresupuestal,data = request.data)
                    if rubropresupuestal_serializer.is_valid():
                        rubropresupuestal_serializer.save()
                        return Response(rubropresupuestal_serializer.data,status = status.HTTP_201_CREATED)
                    return Response(rubropresupuestal_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response('falta el nodo codigo',status = status.HTTP_400_BAD_REQUEST) 
        elif request.method == 'DELETE':
            rubropresupuestal_serializers = Rubropresupuestalserializers(rubropresupuestal)
            if Rubropresupuestal.objects.filter(idpadre = rubropresupuestal_serializers.data['id']).count() == 0:
                try:
                    rubropresupuestal.delete()
                    return Response('Rubro presupuestal eliminado Correctamente',status = status.HTTP_200_OK)
                except RestrictedError:
                    return Response('Rubro presupuestal no puede ser eliminado esta asociado a un documento',status = status.HTTP_400_BAD_REQUEST)
            return Response('Rubro presupuestal no puede ser eliminado esta asociado como padre a otro rubro',status = status.HTTP_400_BAD_REQUEST)            
    return Response('Rubro presupuestal No Existe',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def rubropresupuestal_final_api_view(request):

    if request.method =='GET':
        data = Rubropresupuestal.objects.all()        
        rubropresupuestal_serializer = Rubropresupuestalserializers(data, many=True)
        list_rubros = [rubro for rubro in rubropresupuestal_serializer.data if Rubropresupuestal.objects.filter(idpadre = rubro['id']).count() == 0]  
        return Response(list_rubros,status = status.HTTP_200_OK)

@api_view(['GET'])
def rubropresupuestal_proyectados_api_view(request):
    periodoid=0
    parametros = dict(request.query_params)        
    codigoinstitucioneducativa = ""
    institucioneducativaid = 0
    

    if request.method =='GET':
        periodo = Periodo.objects.filter(activo = True).first()

        if periodo:
            periodoid = periodo.id
        
        if 'codigoinstitucioneducativa' in parametros.keys():
            codigoinstitucioneducativa = str(parametros["codigoinstitucioneducativa"][0])
            codigoinstitucioneducativa = codigoinstitucioneducativa.upper() 
            
            institucioneducativa = Institucioneducativa.objects.filter(codigo =codigoinstitucioneducativa).first()
            
            if institucioneducativa:            
                institucioneducativaid = institucioneducativa.id                

        proyeccionpresupuestalcabecera = Proyeccionpresupuestalcabecera.objects.filter(periodoid=periodoid,institucioneducativaid=institucioneducativaid).first()        
        if proyeccionpresupuestalcabecera:            
            proyeccionpresupuestaldetalle = Proyeccionpresupuestaldetalle.objects.filter(proyeccionpresupuestalid=proyeccionpresupuestalcabecera.id).values('rubropresupuestalid').annotate(total=Sum('valor'))
            if proyeccionpresupuestaldetalle:                
                list_rubros = [Rubropresupuestal.objects.filter(id = rubro['rubropresupuestalid']).first() for rubro in proyeccionpresupuestaldetalle]
                if list_rubros:
                    rubropresupuestal_serializer = Rubropresupuestalserializers(list_rubros, many=True)
                    return Response(rubropresupuestal_serializer.data,status = status.HTTP_200_OK)
                return Response('No existen datos de rubros asociados al detalle la proyeccion del periodo actual',status = status.HTTP_400_BAD_REQUEST)
            return Response('No existen datos de detalle para el documento de proyeccion del periodo actual',status = status.HTTP_400_BAD_REQUEST)        
        return Response('No existen datos de proyeccion para la institucion educativa ',status = status.HTTP_400_BAD_REQUEST)


def buscarrubropresupuestal_final(data):
    rubropresupuestal = Rubropresupuestal.objects.filter(codigo = data['codigo']).first()
    if rubropresupuestal:
        if Rubropresupuestal.objects.filter(idpadre = rubropresupuestal.id).count()==0:
            return rubropresupuestal

@api_view(['GET'])
def saldorubroporproyeccion_final_api_view(request):

    parametros = dict(request.query_params)
    if request.method =='GET':
        codigoinstitucioneducativa = ""
        institucioneducativaid = 0
        codigorubropresupuestal = ""
        rubropresupuestalid = 0        
        
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

        if 'codigorubropresupuestal' in parametros.keys():
            codigorubropresupuestal = parametros['codigorubropresupuestal'][0]
            rubropresupuestal = Rubropresupuestal.objects.filter(codigo = codigorubropresupuestal).first()

            if rubropresupuestal:
                rubropresupuestalid = rubropresupuestal.id
            else:
                return Response('rubropresupuestal no existe',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('rubropresupuestal no existe',status = status.HTTP_400_BAD_REQUEST)
        
        
        return Response(saldorubroporproyeccion(institucioneducativaid,rubropresupuestalid),status = status.HTTP_200_OK)

@api_view(['GET'])
def saldorubro_solicitud_api_view(request):

    parametros = dict(request.query_params)
    if request.method =='GET':
        saldo = 0
        totalsolicitudes = 0
        totalcdp=0
        codigoinstitucioneducativa = ""
        institucioneducativaid = 0
        codigorubropresupuestal = ""
        rubropresupuestalid = 0        
        
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

        if 'codigorubropresupuestal' in parametros.keys():
            codigorubropresupuestal = parametros['codigorubropresupuestal'][0]
            rubropresupuestal = Rubropresupuestal.objects.filter(codigo = codigorubropresupuestal).first()

            if rubropresupuestal:
                rubropresupuestalid = rubropresupuestal.id
            else:
                return Response('rubropresupuestal no existe',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('rubropresupuestal no existe',status = status.HTTP_400_BAD_REQUEST)
        
        totalsolicitudes = saldo_rubro_solicitud(institucioneducativaid,rubropresupuestalid)
        totalcdp = saldo_rubro_cdp(institucioneducativaid,rubropresupuestalid)
        saldo = totalsolicitudes - totalcdp
        
        return Response(saldo,status = status.HTTP_200_OK)

@api_view(['GET'])
def saldorubro_recaudo_api_view(request):

    parametros = dict(request.query_params)
    
    if request.method =='GET':
        saldo = 0
        totalrecaudos= 0
        totalcdp=0
        codigoinstitucioneducativa = ""
        institucioneducativaid = 0
        codigorubropresupuestal = ""
        rubropresupuestalid = 0        
        
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

        if 'codigorubropresupuestal' in parametros.keys():
            codigorubropresupuestal = parametros['codigorubropresupuestal'][0]
            
            rubropresupuestal = Rubropresupuestal.objects.filter(codigo = codigorubropresupuestal).first()

            if rubropresupuestal:
                rubropresupuestalid = rubropresupuestal.id
            else:
                return Response('rubropresupuestal no existe',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('rubropresupuestal no existe',status = status.HTTP_400_BAD_REQUEST)
        
        totalrecaudos = saldo_rubro_recaudos(institucioneducativaid,rubropresupuestalid)
        totalcdp = saldo_rubro_cdp(institucioneducativaid,rubropresupuestalid)
        saldo = totalrecaudos - totalcdp
        
        return Response(saldo,status = status.HTTP_200_OK)      

def saldorubroporproyeccion(institucioneducativaid,rubropresupuestalid):
    saldo = 0
    codigoperiodo = 0
    periodoid = 0
    periodo = Periodo.objects.filter(activo = True).first()
    totalproyeccion = 0
    totalsolicitudes = 0
    if periodo:
        periodoid = periodo.id
        codigoperiodo = periodo.codigo
    
    proyeccionpresupuestalcabecera = Proyeccionpresupuestalcabecera.objects.filter(periodoid=periodoid, institucioneducativaid = institucioneducativaid ).first() 
    
    if proyeccionpresupuestalcabecera:           
        proyeccionpresupuestaldetalle = Proyeccionpresupuestaldetalle.objects.filter(rubropresupuestalid = rubropresupuestalid,proyeccionpresupuestalid = proyeccionpresupuestalcabecera.id).values('rubropresupuestalid').annotate(total=Sum('valor')).order_by()
        if proyeccionpresupuestaldetalle:
            totalproyeccion =proyeccionpresupuestaldetalle[0]['total']

    solicitudes = Solicitudpresupuestalcabecera.objects.filter(institucioneducativaid = institucioneducativaid,fecha__year = codigoperiodo).all()
   
    for solicitud in solicitudes:
        solicitudpresupuestaldetalle = Solicitudpresupuestaldetalle.objects.filter(rubropresupuestalid=rubropresupuestalid,solicitudpresupuestalcabeceraid=solicitud.id).values('rubropresupuestalid').annotate(total=Sum('valor')).order_by()
        if solicitudpresupuestaldetalle:
            totalsolicitudes = totalsolicitudes + solicitudpresupuestaldetalle[0]['total']

    
    saldo = totalproyeccion - totalsolicitudes 

    return saldo

def buscarrubro_solicitud(institucioneducativaid,rubropresupuestalid):
    codigoperiodo = 0
    periodo = Periodo.objects.filter(activo = True).first()
    
    if periodo:
        codigoperiodo = periodo.codigo     

    if Solicitudpresupuestaldetalle.objects.select_related('solicitudpresupuestalcabeceraid').filter(solicitudpresupuestalcabeceraid__institucioneducativaid__id=institucioneducativaid,solicitudpresupuestalcabeceraid__fecha__year=codigoperiodo,rubropresupuestalid=rubropresupuestalid).count()>0:
        return True
    else:
        return False

def saldo_rubro_solicitud(institucioneducativaid,rubropresupuestalid):
    codigoperiodo = 0
    periodo = Periodo.objects.filter(activo = True).first()
    saldo = 0

    if periodo:
        codigoperiodo = periodo.codigo     

    solicitudpresupuestaldetalle = Solicitudpresupuestaldetalle.objects.select_related('solicitudpresupuestalcabeceraid').filter(solicitudpresupuestalcabeceraid__institucioneducativaid__id=institucioneducativaid,solicitudpresupuestalcabeceraid__fecha__year=codigoperiodo,rubropresupuestalid=rubropresupuestalid).values('rubropresupuestalid').annotate(total=Sum('valor'))
    
    if solicitudpresupuestaldetalle:
        saldo = solicitudpresupuestaldetalle[0]['total']
    return saldo

def saldo_rubro_cdp(institucioneducativaid,rubropresupuestalid):
    codigoperiodo = 0
    periodo = Periodo.objects.filter(activo = True).first()
    saldo = 0

    if periodo:
        codigoperiodo = periodo.codigo     

    cdp = Certificadodisponibilidadpresupuestal.objects.filter(institucioneducativaid = institucioneducativaid, fecha__year=codigoperiodo,rubropresupuestalid=rubropresupuestalid).values('rubropresupuestalid').annotate(total=Sum('valor'))
    
    if cdp:
        saldo = cdp[0]['total']
    return saldo


def saldo_rubro_recaudos(institucioneducativaid,rubropresupuestalid):
    codigoperiodo = 0
    periodo = Periodo.objects.filter(activo = True).first()
    saldo = 0
    periodoid= 0
    if periodo:
        periodoid = periodo.id
        codigoperiodo = periodo.codigo     

    proyeccionpresupuestalcabecera = Proyeccionpresupuestalcabecera.objects.filter(periodoid=periodoid, institucioneducativaid = institucioneducativaid ).first() 
    
    if proyeccionpresupuestalcabecera:           
        fuenterecursos = Proyeccionpresupuestaldetalle.objects.filter(rubropresupuestalid = rubropresupuestalid,proyeccionpresupuestalid = proyeccionpresupuestalcabecera.id).values('fuenterecursoid','rubropresupuestalid').all()
    if fuenterecursos:
        ingresos = [Ingresopresupuestal.objects.filter(institucioneducativaid = institucioneducativaid, fecha__year = codigoperiodo,fuenterecursoid = fuente['fuenterecursoid']).all() for fuente in fuenterecursos if Ingresopresupuestal.objects.filter(institucioneducativaid = institucioneducativaid, fecha__year = codigoperiodo,fuenterecursoid = fuente['fuenterecursoid']).count()>0]
        for ingresopresupuestal in ingresos:            
            recaudos = Recaudopresupuestal.objects.filter(ingresopresupuestalid = ingresopresupuestal[0].id).values('ingresopresupuestalid').annotate(total=Sum('valor'))
            if recaudos:
                saldo = saldo + recaudos[0]['total']
    return saldo
    
    
    

      

