from django.contrib.auth.models import *
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'username', 'email', 'groups']   

class ProfileSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=False)
    class Meta:
        model = Profiles
        fields = '__all__'                

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'   

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'  

class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogs
        fields = '__all__'  

class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['groups'] 
        depth = 2  

class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']                                         