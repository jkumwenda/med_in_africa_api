from .viewset_includes import *

class GroupViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = Group.objects.all()

    def get_object(self, pk=None):
        try:
            return Group.objects.get(pk = pk)
        except Group.DoesNotExist:
            raise Http404 
            
    def list(self, request):
        Security.secureAccess(self, 'view_group', request)
        paginator = ResponsePaginationHelper()
        results = paginator.paginate_queryset(self.queryset, request)
        serializer = GroupSerializer(results, many=True)
        UserLogHelper.createLog(request, request.method, request.user.id)
        return paginator.get_paginated_response(serializer.data)

    def create (self, request):
        Security.secureAccess(self, 'add_group', request)        
        serializer = GroupSerializer(data =  request.data)
        if serializer.is_valid():
            serializer.save()  
            UserLogHelper.createLog(request, request.method, request.user.id)
            return Response(serializer.data, status = status.HTTP_201_CREATED)    
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_group', request)        
        group =  self.get_object(pk)  
        serializer = GroupSerializer(group, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)              
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)              

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_group', request)        
        group = self.get_object(pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data) 


    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_group', request)        
        group = self.get_object(pk)
        group.delete()
        UserLogHelper.createLog(request.data, request.method, request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT) 