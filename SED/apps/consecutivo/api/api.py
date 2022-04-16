from itertools import count
from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from apps.consecutivo.models import Consecutivo
from apps.consecutivo.api.serializers import Consecutivoserializers

from django.db.models.deletion import RestrictedError
from django.db.utils import IntegrityError

def consultarconsecutivo (tipodocumento,institucioneducativaid):

    if Consecutivo.objects.filter(tipodocumento = tipodocumento, institucioneducativaid = institucioneducativaid).count() == 0:
        return 1
    else:
        consecutivo = Consecutivo.objects.filter(tipodocumento = tipodocumento, institucioneducativaid = institucioneducativaid).first()
        if consecutivo:
            consecutivoserializers = Consecutivoserializers(consecutivo)
            consecutivo = dict(consecutivoserializers.data)
            return consecutivo['consecutivo'] + 1
        else:
            return 1

def actualizarconsecutivo(tipodocumento,institucioneducativaid,consecutivo):
    consecutivo = {
            "tipodocumento":tipodocumento,
            "institucioneducativaid":institucioneducativaid,
            "consecutivo":consecutivo
            }  
    objconsecutivo = Consecutivo.objects.filter(tipodocumento = tipodocumento, institucioneducativaid = institucioneducativaid).first()
    if objconsecutivo:
        consecutivo_serializers = Consecutivoserializers(objconsecutivo,consecutivo)
        if consecutivo_serializers.is_valid():            
            try:
                consecutivo_serializers.save()
            except IntegrityError:
                return Response('error duplicado en cosecutivo para tipo de documento seleccionado',status = status.HTTP_400_BAD_REQUEST)
        return  Response('error en cosecutivo para tipo de documento seleccionado',status = status.HTTP_400_BAD_REQUEST)
    else:
        consecutivo_serializers = Consecutivoserializers(data = consecutivo)
        if consecutivo_serializers.is_valid():    
            try:
                consecutivo_serializers.save()
            except IntegrityError:
                return Response('error duplicado en cosecutivo para tipo de documento seleccionado',status = status.HTTP_400_BAD_REQUEST)
        return  Response('error en cosecutivo para tipo de documento seleccionado',status = status.HTTP_400_BAD_REQUEST)
        

        