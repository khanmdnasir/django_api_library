from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from user.views import ExtendedDjangoModelPermissions
from rest_framework.views import APIView
from . import signals
from user.views import CustomPagination

# Create your views here.
class ActionTypeViewSet(viewsets.ModelViewSet):
    queryset=ActionType.objects.all()
    serializer_class=ActionTypeSerializer
    permission_classes = [ExtendedDjangoModelPermissions]

        
    def list(self, request):
        instance=ActionType.objects.all()       
        serializer=ActionTypeSerializer(instance, many=True)
        return Response({'results':serializer.data})
        
    def create(self, request):
        try:            
            data=request.data
            serializer = ActionTypeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            print(e)
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})
    
    def partial_update(self, request, pk=None):
        try:
            data=request.data
            instance = ActionType.objects.get(id=pk)
            serializer = ActionTypeSerializer(instance=instance, data=data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
        except Exception as e:
            print(str(e))
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})
        
    def destroy(self, request, pk):
        try:
            instance = ActionType.objects.get(id=pk)
            instance.delete()
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})



class AuthenticationLogApi(APIView):
    queryset=AuthenticationLog.objects.all()
    serializer_class=AuthenticationLogSerializer
    permission_classes = [ExtendedDjangoModelPermissions]
    pagination_class = CustomPagination

    def get(self,request):        
        data = request.data
        activity_log = AuthenticationLog.objects.all()
        if 'user' in data:
            activity_log.filter(user=data['user'])
    
        if 'page' not in self.request.query_params:
            serializer=AuthenticationLogSerializer(activity_log, many=True)
            return Response({'results':serializer.data})
        else:
            page = self.paginate_queryset(activity_log)
            serializer=AuthenticationLogSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class ActivityLogApi(APIView):
    queryset=ActivityLog.objects.all()
    serializer_class=ActivityLogSerializer
    permission_classes = [ExtendedDjangoModelPermissions]
    pagination_class = CustomPagination

    def get(self,request):        
        data = request.data
        activity_log = ActivityLog.objects.all()
        if 'user' in data:
            activity_log.filter(user=data['user'])
        if 'action_model' in data:
            activity_log.filter(action_model=data['action_model'])
        if 'action_object' in data:
            activity_log.filter(action_object=data['action_object'])

        if 'page' not in self.request.query_params:
            serializer=ActivityLogSerializer(activity_log, many=True)
            return Response({'results':serializer.data})
        else:
            page = self.paginate_queryset(activity_log)
            serializer=ActivityLogSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def post(self,request):
        try:
            data= request.data
            signals.activity_log_task.send(sender=request.user.__class__,user=request.user, credentials=data, request=request)
        except Exception as e:
            print(e)
            return Response({"success": False,"error": 'Failed' })
        else:
            return Response({"success": True})