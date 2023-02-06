from rest_framework.views import APIView
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response



class SMSConfigViewSet(viewsets.ModelViewSet):
    queryset = SMSConfigModel.objects.all()
    serializer_class = SMSConfigSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = NotificationModel.objects.all()
    serializer_class = NotificationSerializer

class SMSScheduleViewSet(viewsets.ModelViewSet):
    queryset = SMSScheduleModel.objects.all()
    serializer_class = SMSScheduleSerializer

class EmailScheduleViewSet(viewsets.ModelViewSet):
    queryset = SMSScheduleModel.objects.all()
    serializer_class = SMSScheduleSerializer



class SendSMSApi(APIView):
        
    def post(self,request):
        try:
            
            pass
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            
            return Response({"success": True})

class SendEmailApi(APIView):
        
    def post(self,request):
        try:
            
            pass
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            
            return Response({"success": True})


