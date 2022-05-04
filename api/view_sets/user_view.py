from api import helper
from django.http.response import JsonResponse
from .viewset_includes import *
from django.contrib.auth.hashers import make_password

class UserViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_object(self, pk=None):
        try:
            return User.objects.get(pk = pk)
        except User.DoesNotExist:
            raise Http404 
            
    def list(self, request):
        Security.secureAccess(self, 'view_user', request)
        paginator = ResponsePaginationHelper()
        results = paginator.paginate_queryset(self.queryset, request)
        serializer = UserSerializer(results, many=True)
        UserLogHelper.createLog(request, request.method, request.user.id)
        return paginator.get_paginated_response(serializer.data)

    def create (self, request):
        Security.secureAccess(self, 'add_user', request)        
        serializer = UserSerializer(data =  request.data)
        if serializer.is_valid():
            user = User()
            user.first_name = request.data['first_name']    
            user.last_name = request.data['last_name']    
            user.username = request.data['username']    
            user.password = helper.GeneratePassword.random_password() 
            user.email = request.data['email']
            user.save()
            helper.AddUserGroups.userGroups(request.data['groups'], user)
            helper.SendEmail.NewUser(request.data, user.password) 
            UserLogHelper.createLog(request, request.method, request.user.id)
            return Response(serializer.data, status = status.HTTP_201_CREATED)    
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_user', request)        
        user =  self.get_object(pk)  
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)              
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)              

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_user', request)        
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data) 

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_user', request)        
        user = self.get_object(pk)
        user.delete()
        UserLogHelper.createLog(request.data, request.method, request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT) 

class UserRegistrationViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def create (self, request):
        Security.secureAccess(self, 'add_user', request) 
        request.data.update({"groups":[2]}) 
        serializer = UserSerializer(data =  request.data)
        
        if serializer.is_valid():
            user = User()
            user.first_name = request.data['first_name']    
            user.last_name = request.data['last_name']    
            user.username = request.data['username']    
            user.password = make_password(request.data['password'])    
            user.email = request.data['email']
            user.save() 
            helper.AddUserGroups.userGroups(request.data['groups'], user)
            helper.SendEmail.UserRegistration(user)
            UserLogHelper.createLog(request.data, request.method, request.user.id)
            return Response(serializer.data, status = status.HTTP_201_CREATED)    
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)   


class PasswordResetViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_object(self, pk=None):
        try:
            return User.objects.get(pk = pk)
        except User.DoesNotExist:
            raise Http404       

    def list(self, request):
        Security.secureAccess(self, 'view_user', request)
        paginator = ResponsePaginationHelper()
        results = paginator.paginate_queryset(self.queryset, request)
        serializer = UserPasswordSerializer(results, many=True)
        UserLogHelper.createLog(request, request.method, request.user.id)
        return paginator.get_paginated_response(serializer.data)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_user', request)        
        user =  self.get_object(pk) 
        serializer = UserPasswordSerializer(user, data = request.data)
        if serializer.is_valid():
            user.password = make_password(request.data['password'])
            user.save()
            helper.SendEmail.PasswordRest(user)
            return Response(serializer.data)             
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)                    