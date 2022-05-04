from .viewset_includes import *

class PermissionViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Permission.objects.all()

    def get_object(self, pk=None):
        try:
            return Permission.objects.get(pk = pk)
        except Permission.DoesNotExist:
            raise Http404 
            
    def list(self, request):
        Security.secureAccess(self, 'view_permission', request)        
        paginator = ResponsePaginationHelper()
        results = paginator.paginate_queryset(self.queryset, request)
        serializer = PermissionSerializer(results, many=True)
        UserLogHelper.createLog(request, request.method, request.user.id)
        return paginator.get_paginated_response(serializer.data)

    def create (self, request):
        Security.secureAccess(self, 'add_permission', request)          
        serializer = PermissionSerializer(data =  request.data)
        if serializer.is_valid():
            serializer.save()  
            UserLogHelper.createLog(request, request.method, request.user.id)
            return Response(serializer.data, status = status.HTTP_201_CREATED)    
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_permission', request)          
        permission =  self.get_object(pk)  
        serializer = PermissionSerializer(permission, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)              
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)              

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_permission', request)          
        permission = self.get_object(pk)
        serializer = PermissionSerializer(permission)
        return Response(serializer.data) 

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_permission', request)          
        permission = self.get_object(pk)
        permission.delete()
        UserLogHelper.createLog(request.data, request.method, request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT) 