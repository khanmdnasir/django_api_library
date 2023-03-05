from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import *
from .serializers import *
from user.views import ExtendedDjangoModelPermissions
from django.http import HttpResponseRedirect

from .utils.paymentGateway import *




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
        if 'payment_gateway' in data:
            if(data['payment_gateway'] == 'stripe'):
                try:
                    result = stripe_payment_integration(data)
                    print(result)
                except Exception as e:
                    return Response({'success': False,'error': str(e)})
                else:
                    return Response({'success': True, 'data': {
                    'customer_id': result['customer_id'], 'extra_msg': result['extra_msg']}
                    }) 
            elif(data['payment_gateway'] == 'ebl'):
                try:
                    redirect_url = EblPayment(data)
                    print(redirect_url)
                except Exception as e:
                    return Response({'success':False,'error': str(e)})
                else:
                    return HttpResponseRedirect(redirect_url) 
            else:
                return Response({'success': False,'error': 'No payment gateway available'})
        else:
            return Response({'success': False,'error': 'Payment gateway parameter required'})
            
        

class PaymentSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(selt,request):
        data = request.data
        
        result = stripe_subscription_payment_integration(data)
        return Response(status=status.HTTP_200_OK, 
            data={'message': 'Success', 'data': {
            'customer_id': result['customer_id'], 'extra_msg': result['extra_msg']}
        }) 
    

class StripeConfigView(APIView):
    permission_classes = [IsAuthenticated]

    def get(selt,request):
        try:
            stripe_config = StripeConfig.objects.get().values('stripe_access_key','test_stripe_access_key','testMode')
        except Exception as e:
            print(str(e))
            return Response({'success':False,'error': str(e)})
        else:        
            return Response({'success': True, 'data': stripe_config}) 


