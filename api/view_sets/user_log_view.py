from .viewset_includes import *

class UserLogsViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = UserLogs.objects.all()

    def get_object(self, pk=None):
        try:
            return UserLogs.objects.get(pk = pk)
        except UserLogs.DoesNotExist:
            raise Http404 
            
    def list(self, request):
        Security.secureAccess(self, 'view_userlogs', request)          
        paginator = ResponsePaginationHelper()
        results = paginator.paginate_queryset(self.queryset, request)
        serializer = UserLogSerializer(results, many=True)
        UserLogHelper.createLog(request, request.method, request.user.id)
        return paginator.get_paginated_response(serializer.data)
