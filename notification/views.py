from rest_framework.views import APIView
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .tasks import non_schedule_sms_send_task,non_schedule_mail_send_task,non_schedule_notification


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
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            
            non_schedule_sms_send_task(request.data['text'])
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            
            return Response({"success": True})

class SendNotificationApi(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            
            non_schedule_notification(request.data['message'])
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            
            return Response({"success": True})

class SendEmailApi(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            
            non_schedule_mail_send_task({'mail_subject': request.data['mail_subject'],'text': request.data['text']})
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            
            return Response({"success": True})


