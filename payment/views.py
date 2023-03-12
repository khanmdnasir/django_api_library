from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import *
from .serializers import *
from user.views import ExtendedDjangoModelPermissions
from django.http import HttpResponseRedirect
from pydoc import locate
# from .utils.paymentGateway import *




# Create your views here.


class CurrencyViewset(viewsets.ModelViewSet):
    queryset=CurrencyModel.objects.all()
    serializer_class=CurrencySerializer
    permission_classes = [ExtendedDjangoModelPermissions]

        
    def list(self, request):
        instance=CurrencyModel.objects.all()       
        serializer=CurrencySerializer(instance, many=True)
        return Response({'results':serializer.data})
        
    def create(self, request):
        try:            
            data=request.data
            serializer = CurrencySerializer(data=data)
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
            instance = CurrencyModel.objects.get(id=pk)
            serializer = CurrencySerializer(instance=instance, data=data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
        except Exception as e:
            print(str(e))
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})
        
    def destroy(self, request, pk):
        try:
            instance = CurrencyModel.objects.get(id=pk)
            instance.delete()
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})
        
class PaymentGatewayViewSet(viewsets.ModelViewSet):
    queryset=PaymentGatewayModel.objects.all()
    serializer_class=PaymentGatewaySerializer
    permission_classes = [ExtendedDjangoModelPermissions]

        
    def list(self, request):
        instance=PaymentGatewayModel.objects.all()       
        serializer=PaymentGatewaySerializer(instance, many=True)
        return Response({'results':serializer.data})
        
    def create(self, request):
        try:            
            data=request.data
            serializer = PaymentGatewaySerializer(data=data)
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
            instance = PaymentGatewayModel.objects.get(id=pk)
            serializer = PaymentGatewaySerializer(instance=instance, data=data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
        except Exception as e:
            print(str(e))
            return Response({"success": False,"error": list(serializer.errors.values())[0][0] })
        else:
            return Response({"success": True,"data":serializer.data})
        
    def destroy(self, request, pk):
        try:
            instance = PaymentGatewayModel.objects.get(id=pk)
            instance.delete()
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})



    

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(selt,request):
        data = request.data
        print(data['payment_gateway_class'])
        try:
            myClass = locate(str(data['payment_gateway_class']))
            object = myClass(data)
            object.generate_invoice()
            redirect_url = object.generate_redirect_url()
            # result = stripe_payment_integration(data)
            
        except Exception as e:
            print(e)
            return Response({'success': False,'error': str(e)})
        else:
            print(redirect_url)
            return HttpResponseRedirect(redirect_url)
            
            
        
    
class PaymentReceiveView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        data = self.request.query_params
        order = OrderModel.objects.get(id=int(data.order_id))
        
        order.status = data.status
        order.save()
        return HttpResponseRedirect(data.return_url+data.status)
    




