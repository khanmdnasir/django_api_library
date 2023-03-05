from rest_framework.views import APIView
from rest_framework import viewsets
from .models import *
from user.models import User
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .tasks import non_schedule_sms_send_task,non_schedule_mail_send_task,non_schedule_notification
from user.views import ExtendedDjangoModelPermissions


class SMSConfigViewSet(viewsets.ModelViewSet):
    queryset = SMSConfigModel.objects.all()
    serializer_class = SMSConfigSerializer
    permission_classes = [ExtendedDjangoModelPermissions]

        
    def list(self, request):
        instance=SMSConfigModel.objects.all()       
        serializer=SMSConfigSerializer(instance, many=True)
        return Response({'results':serializer.data})
        
    def create(self, request):
        try:            
            data=request.data
            serializer = SMSConfigSerializer(data=data)
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
            instance = SMSConfigModel.objects.get(id=pk)
            serializer = SMSConfigSerializer(instance=instance, data=data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
        except Exception as e:
            print(str(e))
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})
        
    def destroy(self, request, pk):
        try:
            instance = SMSConfigModel.objects.get(id=pk)
            instance.delete()
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = NotificationModel.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [ExtendedDjangoModelPermissions]

        
    def list(self, request):
        instance=NotificationModel.objects.all().order_by('-id')      
        serializer=NotificationSerializer(instance, many=True)
        return Response({'results':serializer.data})
        
    def create(self, request):
        try:            
            data=request.data
            serializer = NotificationSerializer(data=data)
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
            instance = NotificationModel.objects.get(id=pk)
            serializer = NotificationSerializer(instance=instance, data=data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
        except Exception as e:
            print(str(e))
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})
        
    def destroy(self, request, pk):
        try:
            instance = NotificationModel.objects.get(id=pk)
            instance.delete()
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})

class SMSScheduleViewSet(viewsets.ModelViewSet):
    queryset = SMSScheduleModel.objects.all()
    serializer_class = SMSScheduleSerializer
    permission_classes = [ExtendedDjangoModelPermissions]

        
    def list(self, request):
        instance=SMSScheduleModel.objects.all().order_by('-id')       
        serializer=SMSScheduleSerializer(instance, many=True)
        return Response({'results':serializer.data})
        
    def create(self, request):
        try:            
            data=request.data
            serializer = SMSScheduleSerializer(data=data)
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
            instance = SMSScheduleModel.objects.get(id=pk)
            serializer = SMSScheduleSerializer(instance=instance, data=data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
        except Exception as e:
            print(str(e))
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})
        
    def destroy(self, request, pk):
        try:
            instance = SMSScheduleModel.objects.get(id=pk)
            instance.delete()
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})

class EmailScheduleViewSet(viewsets.ModelViewSet):
    queryset = SMSScheduleModel.objects.all()
    serializer_class = SMSScheduleSerializer
    permission_classes = [ExtendedDjangoModelPermissions]

        
    def list(self, request):
        instance=SMSScheduleModel.objects.all().order_by('-id')       
        serializer=SMSScheduleSerializer(instance, many=True)
        return Response({'results':serializer.data})
        
    def create(self, request):
        try:            
            data=request.data
            serializer = SMSScheduleSerializer(data=data)
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
            instance = SMSScheduleModel.objects.get(id=pk)
            serializer = SMSScheduleSerializer(instance=instance, data=data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
        except Exception as e:
            print(str(e))
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})
        
    def destroy(self, request, pk):
        try:
            instance = SMSScheduleModel.objects.get(id=pk)
            instance.delete()
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})


        
class UserNotificationApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            instance=NotificationModel.objects.filter(receiver__contains=request.user).order_by('-id',send_to_all=True)    
            serializer=NotificationSerializer(instance, many=True)            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:            
            return Response({"success": True,"data":serializer.data})
        
class SendSMSApi(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            users = User.objects.filter(id__in=request.data['users'])
            non_schedule_sms_send_task(request.data['text'],users)
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            
            return Response({"success": True})
        
class SendSMSAllApi(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            users = User.objects.all()
            non_schedule_sms_send_task(request.data['text'],users)
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            
            return Response({"success": True})

class SendNotificationApi(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            users = User.objects.filter(id__in = request.data['users'])
            non_schedule_notification(request.data['message'],users)
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            
            return Response({"success": True})
        
class SendNotificationAllApi(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            users = User.objects.all()
            non_schedule_notification(request.data['message'],users)
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            
            return Response({"success": True})

class SendEmailApi(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            users = User.objects.filter(id__in = request.data['users'])
            non_schedule_mail_send_task({'mail_subject': request.data['mail_subject'],'text': request.data['text'],'users': users})
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            
            return Response({"success": True})
        
class SendEmailAllApi(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            users = User.objects.all()
            non_schedule_mail_send_task({'mail_subject': request.data['mail_subject'],'text': request.data['text'],'users': users})
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            
            return Response({"success": True})


