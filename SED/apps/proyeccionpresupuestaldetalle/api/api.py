from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.proyeccionpresupuestaldetalle.models import Proyeccionpresupuestaldetalle
from apps.proyeccionpresupuestaldetalle.api.serializers import ProyeccionpresupuestaldetalleSerializers
from apps.proyeccionpresupuestalcabecera.api.api import buscarproyeccionpresupuestalcabecera_dict
from apps.proyeccionpresupuestalcabecera.api.serializers import ProyeccionpresupuestalcabeceraSerializers
from apps.fuenterecurso.api.api import buscarfuenterecurso_final
from apps.fuenterecurso.api.serializers import Fuenterecursoserializers
from apps.rubropresupuestal.api.api import buscarrubropresupuestal_final
from apps.rubropresupuestal.api.serializers import Rubropresupuestalserializers
from django.db.utils import IntegrityError
from apps.proyeccionpresupuestalcabecera.api.api import buscarproyeccionpresupuestalcabecera
from apps.fuenterecurso.models import Fuenterecurso
from apps.rubropresupuestal.models import Rubropresupuestal
from apps.fuenterecurso.api.api import  buscarfuenterecursoingresopresupuestal


@api_view(['GET','POST','DELETE'])
def proyeccionpresupuestaldetalle_api_view(request):
    if request.method =='POST':
        data = request.data
        if 'proyeccionpresupuestalid' in data.keys():
            proyeccionpresupuestalid = data.pop('proyeccionpresupuestalid')
            if 'codigoperiodo' in proyeccionpresupuestalid.keys() and 'codigoinstitucioneducativa' in proyeccionpresupuestalid.keys():
                proyeccionpresupuestalcabecera = buscarproyeccionpresupuestalcabecera_dict(proyeccionpresupuestalid)
                if proyeccionpresupuestalcabecera:
                    
                    proyeccionpresupuestalcabecera_serializers = ProyeccionpresupuestalcabeceraSerializers(proyeccionpresupuestalcabecera)
                    proyeccionpresupuestalid = dict(proyeccionpresupuestalcabecera_serializers.data)
                    data.update({"proyeccionpresupuestalid" : proyeccionpresupuestalid['id']})

                    if 'fuenterecursoid' in data.keys():
                        fuenterecursoid = data.pop('fuenterecursoid')
                        fuenterecurso = buscarfuenterecurso_final(fuenterecursoid)
                        if fuenterecurso:
                            fuenterecurso_serializers =Fuenterecursoserializers(fuenterecurso)
                            fuenterecursoid = dict(fuenterecurso_serializers.data)
                            data.update({"fuenterecursoid":fuenterecursoid['id']})

                            if 'rubropresupuestalid' in data.keys():
                                rubropresupuestalid = data.pop('rubropresupuestalid')
                                rubropresupuestal = buscarrubropresupuestal_final(rubropresupuestalid)
                                if rubropresupuestal:
                                    rubropresupuestal_serializers = Rubropresupuestalserializers(rubropresupuestal)
                                    rubropresupuestalid = dict(rubropresupuestal_serializers.data)
                                    data.update({"rubropresupuestalid":rubropresupuestalid['id']})
                                    
                                    proyeccionpresupuestaldetalle_Serializers = ProyeccionpresupuestaldetalleSerializers(data = data)
                                    
                                    if proyeccionpresupuestaldetalle_Serializers.is_valid():
                                        try:
                                            proyeccionpresupuestaldetalle_Serializers.save()
                                            return Response(proyeccionpresupuestaldetalle_Serializers.data,status = status.HTTP_201_CREATED)
                                        except IntegrityError:
                                            return Response('para el rubro y presupuesto seleccionado ya tiene registrados valores en el periodo actual',status = status.HTTP_400_BAD_REQUEST)
                                    return Response(proyeccionpresupuestaldetalle_Serializers.errors, status = status.HTTP_400_BAD_REQUEST)
                                return Response('rubro presupuestal no es de detalle',status = status.HTTP_400_BAD_REQUEST)
                            return Response('falta el nodo rubropresupuestalid para buscar rubro presupuestal',status = status.HTTP_400_BAD_REQUEST)
                        return Response('fuente recurso no es de detalle',status = status.HTTP_400_BAD_REQUEST)
                    return Response('falta el nodo fuenterecursoid para buscar la fuente de recurso',status = status.HTTP_400_BAD_REQUEST)
                return Response("proyeccion presupuestal no existe para el periodo seleccionado", status = status.HTTP_400_BAD_REQUEST)    
            return Response('faltan el nodo codigoperiodo/codigoinstitucioneducativa para buscar la cabecera',status = status.HTTP_400_BAD_REQUEST)
        return Response('falta el nodo proyeccionpresupuestalid para buscar la cabecera',status = status.HTTP_400_BAD_REQUEST)
    else:
        proyeccionpresupuestalcabecera = buscarproyeccionpresupuestalcabecera(request)
        if proyeccionpresupuestalcabecera:     
            proyeccionpresupuestalcabecera_serializers = ProyeccionpresupuestalcabeceraSerializers(proyeccionpresupuestalcabecera)  
            proyeccionpresupuestalcabecera_dict = dict(proyeccionpresupuestalcabecera_serializers.data)
            institucioneducativa = proyeccionpresupuestalcabecera_dict['institucioneducativaid']
            proyeccionpresupuestaldetalle = buscarproyeccionpresupuestalcabeceradetalle(request,proyeccionpresupuestalcabecera_serializers.data['id'])
            if proyeccionpresupuestaldetalle:
                proyeccionpresupuestaldetalle_serializers = ProyeccionpresupuestaldetalleSerializers(proyeccionpresupuestaldetalle)
                if request.method =='GET':                
                    return Response(proyeccionpresupuestaldetalle_serializers.data,status = status.HTTP_201_CREATED)
                elif request.method =='DELETE':
                    proyeccionpresupuestaldetalle_dict = dict(proyeccionpresupuestaldetalle_serializers.data)
                    fuenterecurso = proyeccionpresupuestaldetalle_dict['fuenterecursoid']                    
                    if buscarfuenterecursoingresopresupuestal(fuenterecurso['id'],institucioneducativa['id'])==False:
                        proyeccionpresupuestaldetalle.delete()
                        return Response("Eliminado Correctamente",status = status.HTTP_201_CREATED)
                    return Response("Fuente de recurso no puede ser eliminada ya tiene ingreso presupuestal registrado",status = status.HTTP_400_BAD_REQUEST)
            return Response("No existe registro para los datos ingresados",status = status.HTTP_400_BAD_REQUEST)
        return Response("No existe registro para los datos ingresados",status = status.HTTP_400_BAD_REQUEST) 

def buscarproyeccionpresupuestalcabeceradetalle(request,proyeccionpresupuestalid):
    parametros = dict(request.query_params)
    codigofuenterecurso = ""
    codigorubropresupuestal = ""
    fuenterecurso_parametros = ""    
    rubropresupuestal_parametros = ""

    if 'codigofuenterecurso' in parametros.keys():
        codigofuenterecurso = parametros['codigofuenterecurso'][0]

        fuenterecurso_parametros = Fuenterecurso.objects.filter(codigo = codigofuenterecurso).first()

        if fuenterecurso_parametros:
            fuenterecurso_parametros_serializers = Fuenterecursoserializers(fuenterecurso_parametros)
            fuenterecurso_parametros = dict(fuenterecurso_parametros_serializers.data)
        else:
            fuenterecurso_parametros = dict({"id":0})
    else:
        fuenterecurso_parametros = dict({"id":0})

    if 'codigorubropresupuestal' in parametros.keys():
        codigorubropresupuestal = parametros['codigorubropresupuestal'][0]
        rubropresupuestal_parametros = Rubropresupuestal.objects.filter(codigo = codigorubropresupuestal).first()

        if rubropresupuestal_parametros:
            rubropresupuestal_parametros_serializers = Rubropresupuestalserializers(rubropresupuestal_parametros)
            rubropresupuestal_parametros = dict(rubropresupuestal_parametros_serializers.data)
        else:
            rubropresupuestal_parametros = dict({"id":0})
    else:
        rubropresupuestal_parametros = dict({"id":0})

    proyeccionpresupuestaldetalle = Proyeccionpresupuestaldetalle.objects.filter(proyeccionpresupuestalid = proyeccionpresupuestalid,fuenterecursoid = fuenterecurso_parametros['id'],rubropresupuestalid= rubropresupuestal_parametros['id']).first()
    return proyeccionpresupuestaldetalle