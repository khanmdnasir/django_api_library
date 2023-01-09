from .serializers import *
from .models import *
from rest_framework import viewsets,pagination
from rest_framework.permissions import AllowAny,IsAuthenticated, DjangoModelPermissions
from django.contrib.auth.models import Group, Permission
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound  
from django.db import IntegrityError, transaction
from django.contrib.contenttypes.models import ContentType

from rest_framework.permissions import DjangoModelPermissions
class ExtendedDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET':['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            if 'username' in request.data:
                user_obj = User.objects.filter(username=request.data['username']).first()
                if user_obj:
                    request.data['email']= user_obj.email
                else:
                    return Response({
                        "success":False,
                        "data": "User has not found with this username"
                        })
            serializer = self.serializer_class(
                data=request.data, 
                context={'request': request}
                )           
                
            serializer.is_valid(raise_exception=True)
            return Response({
                "success":True,
                "data": serializer.validated_data
            }
            )
        except Exception as e:     
            print(str(e))       
            return Response({"success":False,"error": e.detail })
        
        
class CustomPagination(pagination.PageNumberPagination): 
    page_query_param = 'page'
    page_size_query_param = 'limit'
    
    def paginate_queryset(self, queryset, request, view=None):
        """Checking NotFound exception"""
        try:
            return super(CustomPagination, self).paginate_queryset(queryset, request, view=view)
        except NotFound:  # intercept NotFound exception
            return list()
    
    def get_paginated_response(self, data):
        try:           
            next = self.page.next_page_number()
        except Exception as e:
            next = None
        try:           
            previous = self.page.previous_page_number()
        except Exception as e:
            previous = None
        return Response({            
            'next': next,
            'previous': previous,
            'current_page': self.page.number,
            'total_object': self.page.paginator.count,
            'total_page': self.page.paginator.num_pages,
            'results': data
        })
    
paginator = CustomPagination()   
    
class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    pagination_class = CustomPagination
    permission_classes = [ExtendedDjangoModelPermissions]

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()

        
    def list(self, request):
        users=User.objects.all().exclude(id=request.user.id).order_by('-id')
        if self.request.query_params.get('limit') == '0':
            serializer=UserSerializer(users, many=True)
            return Response({'results':serializer.data})
        else:
            page = self.paginate_queryset(users)
            serializer=UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
    
    
    def create(self, request):
        try:
            
            data=request.data
            
            if 'username' in data:
                if data['username'] == '':
                    data['username'] = data['email'].split('@')[0]
            else:
                data['username'] = data['email'].split('@')[0]

            serializer = UserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            if "groups" in data:
                for i in data['groups']:
                    user.groups.add(i)
                    user.save()
            
        except Exception as e:
            print(e)
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})
    
    def partial_update(self, request, pk=None):
        try:
            data=request.data
            instance = User.objects.get(id=pk)
            serializer = UserSerializer(instance=instance, data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            

            if "groups" in data:
                user.groups.clear()
                for i in data['groups']:
                    user.groups.add(i)
                    user.save()

        except Exception as e:
            print(str(e))
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})
        
    def destroy(self, request, pk):
        try:
            instance = User.objects.filter(id=pk, is_active=True).first()
            if instance:
                instance.is_active = False
                instance.save()
            else:
                return Response({"success": False, "error": "User Does Not Exist!"})
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})

    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])  
def update_profile(request):
    try:        
        serializer = ProfileSerializer(request.user, data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except Exception as e:
        print(e)
        return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
    else:
        return Response({"success": True,"data":serializer.data})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])  
def change_password(request):
    try:   
        user = request.user
        checkPassword = check_password(request.data['old_password'], user.password)
        if checkPassword:        
            user.password = make_password(request.data['new_password'])
            user.save() 
        else:
            return Response({"success": False,'error':'wrong old password'})
    except Exception as e:
        return Response({"success": False,'error': 'Something Wrong!'})
    else:
        return Response({"success": True})
        

    
    
class PermissionViewSet(viewsets.ModelViewSet):
    queryset=Permission.objects.filter().exclude(codename__in=["add_logentry","change_logentry","delete_logentry","view_logentry","add_permission","change_permission","delete_permission","view_permission","add_customgroup","change_customgroup","delete_customgroup","view_customgroup","add_contenttype","change_contenttype","delete_contenttype","view_contenttype","add_session","change_session","delete_session","view_session"])
    serializer_class=PermissionSerializer

    def create(self, request):
        try:
            data = request.data  
            ct = ContentType.objects.get(app_label='user', model='user')   
            serializer = PermissionSerializer(data={'codename':data['codename'],'name':data['name'],'content_type':ct.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            return Response({"success": False,"error": str(e)})
        else:
            return Response({"success": True,"data":serializer.data})
    
    def partial_update(self, request, pk=None):
        try:
            data = request.data   
            instance= Permission.objects.get(codename=data['codename'])
            serializer = PermissionSerializer(instance=instance,data={'codename':data['codename'],'name':data['name']},partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            return Response({"success": False,"error": 'Something Wrong!' })
        else:
            return Response({"success": True,"data":serializer.data})
    
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset=Group.objects.all()
    serializer_class=UserGroupSerializer
    pagination_class = CustomPagination
    permission_classes = [ExtendedDjangoModelPermissions]
    
    def list(self, request):
        groups=Group.objects.all().order_by('-id')
        
        if self.request.query_params.get('limit'):
            page = self.paginate_queryset(groups)
            serializer=UserGroupSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer=UserGroupSerializer(groups, many=True)
            return Response({'results':serializer.data})
    
    def create(self, request):
        try:
            data = request.data     
            serializer = UserGroupSerializer(data={'name':data['name']})
            serializer.is_valid(raise_exception=True)
            try:
                with transaction.atomic():
                    group = serializer.save()
                    group.permissions.clear()
                    for x in data['permissions']:
                        permission = Permission.objects.get(codename=x)
                        group.permissions.add(permission)
                        group.save()
            except IntegrityError:
                transaction.set_rollback(True)
        except Exception as e:
            return Response({"success": False,"error": str(e)})
        else:
            return Response({"success": True,"data":serializer.data})
    
    def partial_update(self, request, pk=None):
        try:
            data = request.data
            group = Group.objects.get(id=pk)
            group.permissions.clear()
            for x in data['permissions']:
                permission = Permission.objects.get(codename=x)
                group.permissions.add(permission)
                group.save()
            
        except Exception as e:
            return Response({"success": False,"error": 'Something Wrong!' })
        else:
            return Response({"success": True})
    

class UserRoleApi(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        permissions = []
        group = request.user.groups.first()
        serializer = UserGroupSerializer(group)
        for i in serializer.data['permissions']:
            permissions.append(i['codename'])
                   
        return Response({'permissions':permissions})
