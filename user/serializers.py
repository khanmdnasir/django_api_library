from .models import *
from django.contrib.auth.models import Permission,Group
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions,serializers

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        data = super().validate(attrs)

        data['id'] = self.user.id 
        data['username'] = self.user.username 
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['email'] = self.user.email
        data['phone'] = str(self.user.phone)
        try:
            data['profile_image'] =  str(self.user.profile_image.url)
        except Exception as e:
            data['profile_image'] = 'null'
        
        if self.user:
            if self.user.is_active:
                return data
            raise exceptions.AuthenticationFailed('Account is not activated')
        raise exceptions.AuthenticationFailed()

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
        
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        
class UserGroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True,read_only=True)
    class Meta:
        model = Group
        fields = '__all__'
        
        
class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(Group.objects.all(),many=True,read_only=True)
    class Meta:
        model = User
        read_only_fields = ["is_superuser"]
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)
    
       
    
    
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','phone','profile_image')

        
        
    
        

        
