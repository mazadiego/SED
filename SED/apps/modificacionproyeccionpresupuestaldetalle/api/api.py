from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.modificacionproyeccionpresupuestaldetalle.models import Modificacionproyeccionpresupuestaldetalle
from apps.modificacionproyeccionpresupuestaldetalle.api.serializers import ModificacionproyeccionpresupuestaldetalleSerializers
from apps.modificacionproyeccionpresupuestalcabecera.api.api import buscarmodificacionproyeccionpresupuestalcabecera_dict
from apps.modificacionproyeccionpresupuestalcabecera.api.serializers import ModificacionproyeccionpresupuestalcabeceraSerializers
from apps.fuenterecurso.api.api import buscarfuenterecurso_final
from apps.fuenterecurso.api.serializers import Fuenterecursoserializers
from apps.rubropresupuestal.api.api import buscarrubropresupuestal_final
from apps.rubropresupuestal.api.serializers import Rubropresupuestalserializers
from django.db.utils import IntegrityError
from apps.modificacionproyeccionpresupuestalcabecera.api.api import buscarmodificacionproyeccionpresupuestalcabecera
from apps.fuenterecurso.models import Fuenterecurso
from apps.rubropresupuestal.models import Rubropresupuestal
from apps.fuenterecurso.api.api import  buscarfuenterecursoingresopresupuestal
from apps.rubropresupuestal.api.api import buscarrubro_solicitud


@api_view(['GET','POST','DELETE'])
def modificacionproyeccionpresupuestaldetalle_api_view(request):
    if request.method =='POST':
        data = request.data
        if 'modificacionproyeccionpresupuestalid' in data.keys():
            modificacionproyeccionpresupuestalid = data.pop('modificacionproyeccionpresupuestalid')
            if 'codigoperiodo' in modificacionproyeccionpresupuestalid.keys() and 'codigoinstitucioneducativa' in modificacionproyeccionpresupuestalid.keys():
                modificacionproyeccionpresupuestalcabecera = buscarmodificacionproyeccionpresupuestalcabecera_dict(modificacionproyeccionpresupuestalid)
                if modificacionproyeccionpresupuestalcabecera:
                    
                    modificacionproyeccionpresupuestalcabecera_serializers = ModificacionproyeccionpresupuestalcabeceraSerializers(modificacionproyeccionpresupuestalcabecera)
                    modificacionproyeccionpresupuestalid = dict(modificacionproyeccionpresupuestalcabecera_serializers.data)
                    data.update({"modificacionproyeccionpresupuestalid" : modificacionproyeccionpresupuestalid['id']})
                    
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
                                    
                                    modificacionproyeccionpresupuestaldetalle_Serializers = ModificacionproyeccionpresupuestaldetalleSerializers(data = data)
                                    
                                    if modificacionproyeccionpresupuestaldetalle_Serializers.is_valid():
                                        
                                        try:
                                            modificacionproyeccionpresupuestaldetalle_Serializers.save()
                                            return Response(modificacionproyeccionpresupuestaldetalle_Serializers.data,status = status.HTTP_201_CREATED)
                                        except IntegrityError:
                                            return Response('para el rubro y presupuesto seleccionado ya tiene registrados valores en el periodo actual',status = status.HTTP_400_BAD_REQUEST)
                                    return Response(modificacionproyeccionpresupuestaldetalle_Serializers.errors, status = status.HTTP_400_BAD_REQUEST)
                                return Response('rubro presupuestal no es de detalle',status = status.HTTP_400_BAD_REQUEST)
                            return Response('falta el nodo rubropresupuestalid para buscar rubro presupuestal',status = status.HTTP_400_BAD_REQUEST)
                        return Response('fuente recurso no es de detalle',status = status.HTTP_400_BAD_REQUEST)
                    return Response('falta el nodo fuenterecursoid para buscar la fuente de recurso',status = status.HTTP_400_BAD_REQUEST)
                return Response("modificacion proyeccion presupuestal no existe para el periodo seleccionado", status = status.HTTP_400_BAD_REQUEST)    
            return Response('faltan el nodo codigoperiodo/codigoinstitucioneducativa para buscar la cabecera',status = status.HTTP_400_BAD_REQUEST)
        return Response('falta el nodo modificacionproyeccionpresupuestalid para buscar la cabecera',status = status.HTTP_400_BAD_REQUEST)
    else:
        modificacionproyeccionpresupuestalcabecera = buscarmodificacionproyeccionpresupuestalcabecera(request)
        if modificacionproyeccionpresupuestalcabecera:     
            modificacionproyeccionpresupuestalcabecera_serializers = ModificacionproyeccionpresupuestalcabeceraSerializers(modificacionproyeccionpresupuestalcabecera)  
            modificacionproyeccionpresupuestalcabecera_dict = dict(modificacionproyeccionpresupuestalcabecera_serializers.data)
            institucioneducativa = modificacionproyeccionpresupuestalcabecera_dict['institucioneducativaid']
            modificacionproyeccionpresupuestaldetalle = buscarproyeccionpresupuestalcabeceradetalle(request,modificacionproyeccionpresupuestalcabecera_serializers.data['id'])
            if modificacionproyeccionpresupuestaldetalle:
                modificacionproyeccionpresupuestaldetalle_serializers = ModificacionproyeccionpresupuestaldetalleSerializers(modificacionproyeccionpresupuestaldetalle)
                if request.method =='GET':                
                    return Response(modificacionproyeccionpresupuestaldetalle_serializers.data,status = status.HTTP_201_CREATED)
                elif request.method =='DELETE':
                    modificacionproyeccionpresupuestaldetalle_dict = dict(modificacionproyeccionpresupuestaldetalle_serializers.data)
                    fuenterecurso = modificacionproyeccionpresupuestaldetalle_dict['fuenterecursoid']   
                    rubropresupuestal = modificacionproyeccionpresupuestaldetalle_dict['rubropresupuestalid']     
                    if buscarfuenterecursoingresopresupuestal(fuenterecurso['id'],institucioneducativa['id'])==False:
                        if buscarrubro_solicitud(institucioneducativa['id'],rubropresupuestal['id'])==False:
                            modificacionproyeccionpresupuestaldetalle.delete()
                            return Response("Eliminado Correctamente",status = status.HTTP_201_CREATED)
                        return Response("Rubro no puede ser eliminado esta asigando a una solicitud presupuestal",status = status.HTTP_400_BAD_REQUEST)
                    return Response("Fuente de recurso no puede ser eliminada ya tiene ingreso presupuestal registrado",status = status.HTTP_400_BAD_REQUEST)
            return Response("No existe registro para los datos ingresados",status = status.HTTP_400_BAD_REQUEST)
        return Response("No existe registro para los datos ingresados",status = status.HTTP_400_BAD_REQUEST) 

def buscarproyeccionpresupuestalcabeceradetalle(request,modificacionproyeccionpresupuestalid):
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

    modificacionproyeccionpresupuestaldetalle = Modificacionproyeccionpresupuestaldetalle.objects.filter(modificacionproyeccionpresupuestalid = modificacionproyeccionpresupuestalid,fuenterecursoid = fuenterecurso_parametros['id'],rubropresupuestalid= rubropresupuestal_parametros['id']).first()
    return modificacionproyeccionpresupuestaldetalle