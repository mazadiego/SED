from rest_framework import serializers
from apps.user.models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','username', 'name', 'last_name','is_active','is_staff','password','rol']


    def validate_rol(self, value):
        if value == None or value == "" or value not in ['Admin','Institucion','Auditor']:
            raise serializers.ValidationError("Debe ingresar un Rol Valido ('Admin','Institucion','Auditor')")
        return value 

    def create(self,validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self,instance,validated_data):
        update_user = super().update(instance,validated_data)
        update_user.set_password(validated_data['password'])
        update_user.save()
        return update_user

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username', 'name', 'last_name','is_active','is_staff','rol']
