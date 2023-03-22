from rest_framework.views import APIView
from rest_framework import viewsets
from user.views import ExtendedDjangoModelPermissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .tasks import db_backup_task
from .models import DbBackupModel
from .serializers import DBBackupSerializer
# Create your views here.

class DbBackupViewSet(viewsets.ModelViewSet):
    queryset = DbBackupModel.objects.all()
    serializer_class = DBBackupSerializer
    permission_classes = [ExtendedDjangoModelPermissions]

        
    def list(self, request):
        instance=DbBackupModel.objects.get()      
        serializer=DBBackupSerializer(instance, many=False)
        return Response({'results':serializer.data})
        
    def create(self, request):
        try:            
            data=request.data
            serializer = DBBackupSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            return Response({"success": True,"data":serializer.data})
    
    def partial_update(self, request, pk=None):
        try:
            data=request.data
            instance = DbBackupModel.objects.get()
            serializer = DBBackupSerializer(instance=instance, data=data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
        except Exception as e:
            print(str(e))
            return Response({"success": False,"error": str(e) })
        else:
            return Response({"success": True,"data":serializer.data})
        
    def destroy(self, request, pk):
        try:
            instance = DbBackupModel.objects.get()
            instance.delete()
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})

class DbBackupApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            db_backup_task(True)
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            
            return Response({"success": True})