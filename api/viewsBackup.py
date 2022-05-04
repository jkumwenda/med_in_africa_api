from django.contrib.auth import authenticate
from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import *
from api.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.views import APIView
from rest_framework import generics,mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .helper import *
from rest_framework.exceptions import APIException

from .view_sets.user_view import UserViewSet
from .view_sets.group_view import GroupViewSet
         
# UserViewSet  

# class UserViewSet(viewsets.ModelViewSet): 
#     queryset = User.objects.all()
#     serializer_class = UserSerializer  
#     pagination_class = CustomPagination
#     # permission_classes = (IsAuthenticated,)

#     # def get_object(self, pk):
#     #     try:
#     #         return User.objects.get(pk = pk)
#     #     except User.DoesNotExist:
#     #         raise Http404 

#     def create(self, request):
#         serializer = UserSerializer(data =  request.data)
#         if serializer.is_valid():
#             user = User()
#             user.first_name = request.data['first_name']    
#             user.last_name = request.data['last_name']    
#             user.username = request.data['username']    
#             user.password = make_password(request.data['password'])    
#             user.email = request.data['email']
#             user.save()  
#             return Response(serializer.data, status = status.HTTP_201_CREATED)    
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#     def update(self, request, pk):
#         return HttpResponse('Edit and got here')

class ProfileViewSet(viewsets.ModelViewSet): 
    queryset = Profiles.objects.all()
    serializer_class = ProfileSerializer  
    permission_classes = (IsAuthenticated,)
    pagination_class  = ResponsePaginationHelper

   

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer  
    pagination_class = ResponsePaginationHelper

class UserLogsViewSet(viewsets.ModelViewSet):
    queryset = UserLogs.objects.all()
    serializer_class = UserLogSerializer   
    pagination_class = ResponsePaginationHelper        

"""
class UserList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):  
        return self.list(request)  

    def post(self, request):
        return self.create(request)    

class UserDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, pk):  
        return self.retrieve(request, pk) 

class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data =  request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)    
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk = pk)
        except User.DoesNotExist:
            raise Http404 

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user) 
        return Response(serializer.data)   

    def put(self, request, pk):
        user =  self.get_object(pk)  
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)              
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)    

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)                  

@api_view(['GET', 'POST', ])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()    
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET', 'PUT', 'DELETE' ])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk = pk)
    except User.DoesNotExist:   
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()    
            return Response(serializer.data)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'DELETE':
        user.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)                       
        
"""