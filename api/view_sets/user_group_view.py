from .viewset_includes import *

class UserGroupViewSet(viewsets.ViewSet):
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
        serializer = UserGroupSerializer(results, many=True)
        UserLogHelper.createLog(request, request.method, request.user.id)
        return paginator.get_paginated_response(serializer.data)

    def create (self, request):
        Security.secureAccess(self, 'add_user', request) 
        serializer = UserGroupSerializer(data =  request.data)
        for group in request.data['groups']:
            group = Group.objects.get(pk=group)
            group.user_set.add(request.data['id']) 
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)             
            
    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_user', request)        
        user =  self.get_object(pk)  
        serializer = UserGroupSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)              
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)              


    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_user', request)        
        user = self.get_object(pk)
        serializer = UserGroupSerializer(user)
        return Response(serializer.data) 


    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_user', request)        
        user = self.get_object(pk)
        user.delete()
        UserLogHelper.createLog(request.data, request.method, request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)         