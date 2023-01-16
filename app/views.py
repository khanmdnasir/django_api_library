from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import DocumentSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import AppSettings,DocumentModel
from .serializers import AppSettingsSerializer
from user.views import ExtendedDjangoModelPermissions
from django.utils.decorators import decorator_from_middleware
from app.middleware.app_settings_middleware import AppSettingsMiddleware
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

    @decorator_from_middleware(AppSettingsMiddleware)
    def post(self,request):
        try:
            links = []
            for f in request.data.getlist('files'):
                try:
                    serializer = DocumentSerializer(data={'file':f})
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    
                except Exception as e:
                    print(e)
                    return Response({"success": False,"error": str(e) })
                else:
                    links.append(serializer.data['file'])
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:
            return Response({"success": True,"data":links})




