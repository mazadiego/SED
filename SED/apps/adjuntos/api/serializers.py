from rest_framework import serializers
from apps.adjuntos.models import Adjuntos
from drf_extra_fields.fields import Base64FileField
import filetype
import base64
import os
from SED.settings import BASE_DIR    
from django.core.files import File
    
class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']
   
    def get_file_extension(self, filename, decoded_file):
        kind = filetype.guess(decoded_file)
        return kind.extension

class AdjuntosSerializers(serializers.ModelSerializer):    
    archivobase64 = PDFBase64File()

    def validate_archivobase64(selft,value):
        if value == "" or value == None:
            raise serializers.ValidationError("campo no puede ser vacio")
        return value

    def validate_documnetoid(selft,value):
        if value <= 0 or value == None:
            raise serializers.ValidationError({
                "documnetoid": "ingresar un valor mayor que cero(0)."
            })
        return value

    def validate_tipo(selft,value):
        if value <= 0 or value == None:            
            raise serializers.ValidationError({
                "tipo": "ingresar un valor mayor que cero(0)."
            })
        return value

    class Meta:
        model = Adjuntos
        fields = ['id','tipo','institucioneducativaid','documnetoid','nombrearchivo','archivobase64']

class DescargarAdjuntosSerializers(serializers.ModelSerializer):    
    
    class Meta:
        model = Adjuntos
        fields = ['id','tipo','institucioneducativaid','documnetoid','nombrearchivo','archivobase64']

    def to_representation(self, instance):
        adjuntos = super().to_representation(instance)
        Rutarel = "." + adjuntos['archivobase64']
        Rutasol = os.path.join(BASE_DIR, Rutarel)        
        
        file_string =  os.path.abspath(Rutasol)
        with open(file_string,"rb") as pdf_file:
            encoded_base64 = base64.b64encode(pdf_file.read())
        
        encoded_str = encoded_base64.decode('utf-8')
        adjuntos['archivobase64'] = encoded_str
        
        return adjuntos

        


   