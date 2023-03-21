from rest_framework.views import APIView
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from user.views import ExtendedDjangoModelPermissions

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [ExtendedDjangoModelPermissions]

        
    def list(self, request):
        instance=Menu.objects.all()     
        serializer=MenuSerializer(instance, many=True)
        return Response({'results':serializer.data})
        
    def create(self, request):
        try:            
            data=request.data
            serializer = MenuSerializer(data=data)
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
            instance = Menu.objects.get(id=pk)
            serializer = MenuSerializer(instance=instance, data=data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
        except Exception as e:
            print(str(e))
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})
        
    def destroy(self, request, pk):
        try:
            instance = Menu.objects.get(id=pk)
            instance.delete()
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})
        
class SubMenuViewSet(viewsets.ModelViewSet):
    queryset = SubMenu.objects.all()
    serializer_class = SubMenuSerializer
    permission_classes = [ExtendedDjangoModelPermissions]

        
    def list(self, request):
        instance=SubMenu.objects.all()     
        serializer=SubMenuSerializer(instance, many=True)
        return Response({'results':serializer.data})
        
    def create(self, request):
        try:            
            data=request.data
            serializer = SubMenuSerializer(data=data)
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
            instance = SubMenu.objects.get(id=pk)
            serializer = SubMenuSerializer(instance=instance, data=data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
        except Exception as e:
            print(str(e))
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})
        
    def destroy(self, request, pk):
        try:
            instance = SubMenu.objects.get(id=pk)
            instance.delete()
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})
        
class SubMenuApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            menu = Menu.objects.get(id=request.data['menu_id'])
            instance=SubMenu.objects.filter(menu=menu)   
            serializer=SubMenuSerializer(instance, many=True)            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": str(e) })
        else:            
            return Response({"success": True,"data":serializer.data})