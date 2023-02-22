from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
import stripe
from rest_framework.permissions import AllowAny
from main.settings import STRIPE_API_KEY
from .models import *
from .serializers import *
from user.views import ExtendedDjangoModelPermissions


stripe.api_key = STRIPE_API_KEY

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

class test_payment(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='usd', 
        payment_method_types=['card'],
        receipt_email='test@example.com')
        return Response(status=status.HTTP_200_OK, data=test_payment_intent)



class StripePaymentView(APIView):
    permission_classes = [AllowAny]

    def post(selt,request):
        data = request.data
        email = data['email']
        payment_method_id = data['payment_method_id']
        extra_msg = '' # add new variable to response message
        # checking if customer with provided email already exists
        customer_data = stripe.Customer.list(email=email).data   
        
        # if the array is empty it means the email has not been used yet  
        if len(customer_data) == 0:
            # creating customer
            customer = stripe.Customer.create(
            email=email, payment_method=payment_method_id)
        else:
            customer = customer_data[0]
            extra_msg = "Customer already existed."
        
        stripe.PaymentIntent.create(
        customer=customer, 
        payment_method=payment_method_id,  
        currency=data['currency'], # you can provide any currency you want
        amount=data['amount'],
        confirm=True
        ) 
        return Response(status=status.HTTP_200_OK, 
            data={'message': 'Success', 'data': {
            'customer_id': customer.id, 'extra_msg': extra_msg}
        }) 

class StripePaymentSubscriptionView(APIView):
    permission_classes = [AllowAny]

    def post(selt,request):
        data = request.data
        email = data['email']
        payment_method_id = data['payment_method_id']
        extra_msg = '' # add new variable to response message
        # checking if customer with provided email already exists
        customer_data = stripe.Customer.list(email=email).data   
        
        # if the array is empty it means the email has not been used yet  
        if len(customer_data) == 0:
            # creating customer
            customer = stripe.Customer.create(
            email=email,
            payment_method=payment_method_id,
            invoice_settings={
                'default_payment_method': payment_method_id
            }
            )
        else:
            customer = customer_data[0]
            extra_msg = "Customer already existed."
        
        stripe.Subscription.create(
            customer=customer,
            items=[
            {
            'price': data['price_id'] #here paste your price id
            }
            ]
        )
        return Response(status=status.HTTP_200_OK, 
            data={'message': 'Success', 'data': {
            'customer_id': customer.id, 'extra_msg': extra_msg}
        }) 


