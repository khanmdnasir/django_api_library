from rest_framework.response import Response
from .serializers import DocumentSerializer
from rest_framework.views import APIView
from .models import AppSettings,DocumentModel
from .serializers import AppSettingsSerializer
from user.views import ExtendedDjangoModelPermissions
from activityLog import signals
# from django.utils.decorators import decorator_from_middleware
# from appSettings.middleware.app_settings_middleware import AppSettingsMiddleware
# from django.conf import settings
# Create your views here.

class AppSettingsApi(APIView):
    serializer_class=AppSettingsSerializer
    permission_classes = [ExtendedDjangoModelPermissions]

    def get(self,request):
        try:
            instance = AppSettings.objects.get()
            serializer = AppSettingsSerializer(instance,many=False)
        except Exception as e:
            print(e)
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})

    def post(self,request):
        try:
            
            serializer = AppSettingsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            print(e)
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})


class DocumentApi(APIView):
    queryset=DocumentModel.objects.all()
    permission_classes = [ExtendedDjangoModelPermissions]

    
    def post(self,request):
        try:
            
            links = []
            for f in request.data.getlist('files'):
                try:
                    serializer = DocumentSerializer(data={'file':f})
                    serializer.is_valid(raise_exception=True)
                    instance = serializer.save()
                    
                except Exception as e:
                    print(e)
                    return Response({"success": False,"error": str(e) })
                else:
                    links.append(serializer.data['file'])
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            signals.activity_log_task.send(sender=request.user.__class__,user=request.user, credentials={'action_type': 'create','action_model': 'document_handling','action_object': instance.id}, request=request)
            return Response({"success": True,"data":links})



