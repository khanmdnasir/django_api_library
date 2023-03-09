import stripe,requests
from payment.models import *
from abc import ABC,abstractmethod
from main import settings

class AbstractPaymentGateway(ABC):

    @abstractmethod
    def generate_invoice(self):
        pass
    
    @abstractmethod
    def generate_redirect_url(self):
        pass

def SetStripeConfig():    
    stripe_config = PaymentGatewayModel.objects.filter(name='stripe').first()    
    if(stripe_config.test_mode):
        stripe.api_key = stripe_config.test_api_key
    else:
        stripe.api_key = stripe_config.api_key
    
class StripePaymentGateway(AbstractPaymentGateway):
    def __init__(self,data):
        self.data = data
        self.return_url = settings.DOMAIN+'/api/payment_receive?return_url='+data['return_url']+'&'

    def generate_invoice(self):
        try:            
            order = OrderModel.objects.create(description=self.data['description'],amount=self.data['amount'],currency=self.data['currency'],customer_name=self.data['name'],customer_email=self.data['email'],customer_phone=self.data['phone'])
            self.order = order
        except Exception as e:
            print(e)
            return False
        else:
            return True
        
    def generate_redirect_url(self):
        try:
            SetStripeConfig()
            product = stripe.Product.create(
            name="order"+str(self.order.id),
            
            )
            print('product',product)
            price = stripe.Price.create(
            product=product.id,
            unit_amount=self.data['amount'],
            currency=self.data['currency'],
            )
            print('price',price)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url= self.return_url+'status=success&order_id='+str(self.order.id),
                cancel_url= self.return_url+'status=cancelled&order_id='+str(self.order.id)
            )
        except Exception as e:
            raise Exception(str(e))
        else:
            return checkout_session.url
        
class StripeSubscriptionPaymentGateway(AbstractPaymentGateway):
    def __init__(self,data):
        self.data = data
        self.return_url = settings.DOMAIN+'/api/payment_receive?return_url='+data['return_url']+'&'

    def generate_invoice(self):
        try:            
            order = OrderModel.objects.create(description=self.data['description'],amount=self.data['amount'],currency=self.data['currency'],customer_name=self.data['name'],customer_email=self.data['email'],customer_phone=self.data['phone'])
            self.order = order
        except Exception as e:
            print(e)
            return False
        else:
            return True
        
    def generate_redirect_url(self):
        try:
            SetStripeConfig()
            product = stripe.Product.create(
            name="order"+str(self.order.id),
            
            )
            print('product',product)
            price = stripe.Price.create(
            product=product.id,
            unit_amount=self.data['amount'],
            currency=self.data['currency'],
            )
            print('price',price)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1,
                    }
                ],
                mode='subscription',
                success_url= self.return_url+'status=success&order_id='+str(self.order.id),
                cancel_url= self.return_url+'status=cancelled&order_id='+str(self.order.id)
            )
        except Exception as e:
            raise Exception(str(e))
        else:
            return checkout_session.url
        
# def stripe_payment_integration(data):
#     try:
#         SetStripeConfig()
#         email = data['email']
#         payment_method_id = data['payment_method_id']
#         extra_msg = '' # add new variable to response message
#         # checking if customer with provided email already exists
#         customer_data = stripe.Customer.list(email=email).data   
        
#         # if the array is empty it means the email has not been used yet  
#         if len(customer_data) == 0:
#             # creating customer
#             customer = stripe.Customer.create(
#             email=email, payment_method=payment_method_id)
#         else:
#             customer = customer_data[0]
#             extra_msg = "Customer already existed."
        
#         stripe.PaymentIntent.create(
#         customer=customer, 
#         payment_method=payment_method_id,  
#         currency=data['currency'], # you can provide any currency you want
#         amount=data['amount'],
#         confirm=True
#         ) 
#     except Exception as e:
#         raise Exception(str(e))
#     else:
#         return { 'customer_id': customer.id,'extra_msg':extra_msg }


class EblPaymentGateway(AbstractPaymentGateway):
    
    def __init__(self,data):
        self.data = data
        self.return_url = settings.DOMAIN+'/api/payment_receive?return_url='+data['return_url']+'&'

    def generate_invoice(self):
        try:            
            order = OrderModel.objects.create(description=self.data['description'],amount=self.data['amount'],currency=self.data['currency'],customer_name=self.data['name'],customer_email=self.data['email'],customer_phone=self.data['phone'])
            self.order = order
        except Exception as e:
            print(e)
            return False
        else:
            return True
            
        
    
    def generate_redirect_url(self):
        
        try:
            ebl_config = PaymentGatewayModel.objects.filter(name='ebl').first()
            
            if ebl_config.test_mode:
                ebl_merchant_id = ebl_config.test_api_key
                ebl_merchant_password = ebl_config.test_access_key
                ebl_merchant_url = 'https://test-gateway.mastercard.com/api/nvp'
                redirect_url = 'https://easternbank.test.gateway.mastercard.com/checkout/pay/'
            else:
                ebl_merchant_id = ebl_config.api_key
                ebl_merchant_password = ebl_config.access_key
                ebl_merchant_url = 'https://ap-gateway.mastercard.com/api/nvp'
                redirect_url = 'https://easternbank.ap.gateway.mastercard.com/checkout/pay/'

            headers = {
                "Content-Length": "20",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
            }
            body_data = {
                    "merchant": ebl_merchant_id,
                    "apiPassword": ebl_merchant_password,
                    "apiUsername": 'merchant.'+ebl_merchant_id,
                    "apiOperation": "INITIATE_CHECKOUT",
                    "order.id": self.order.id,
                    "order.amount": self.order.amount,
                    "order.description": self.order.description,
                    "order.currency": self.order.currency,
                    "interaction.cancelUrl": self.return_url+'status=cancelled&order_id='+str(self.order.id),
                    "interaction.returnUrl": self.return_url+'status=success&order_id='+str(self.order.id),
                    "interaction.operation": "PURCHASE",
                    "interaction.timeout": "1800",
                    "interaction.timeoutUrl": self.return_url+'status=failed&order_id='+str(self.order.id),
                    "interaction.merchant.name": "EBL Secure Invoice",
                    "interaction.merchant.logo": "https://caab.pod.aero/shared/images/logo/pod_logo_400.png",               
                    "interaction.displayControl.billingAddress": "HIDE",
                    "customer.firstName": self.order.customer_name,
                    "customer.email": self.order.customer_email,
                    "customer.phone": self.order.customer_phone
                                    
                }
            response = requests.post(ebl_merchant_url+'/version/66',headers=headers,data=body_data)
            print('response',response.text)
            result = list(response.text.split("&"))
            session_id = ''
            for i in result:
                item = i.split('=')
                if item[0] == 'session.id':
                    session_id = str(item[1])
                    break
            
            
            redirect_to = redirect_url+session_id
        except Exception as e:
            print(str(e))
            raise Exception(str(e))
        else:
            return redirect_to

# def stripe_subscription_payment_integration(data):
#     try:
#         SetStripeConfig()
#         email = data['email']
#         payment_method_id = data['payment_method_id']
#         extra_msg = '' # add new variable to response message
#         # checking if customer with provided email already exists
#         customer_data = stripe.Customer.list(email=email).data   
        
#         # if the array is empty it means the email has not been used yet  
#         if len(customer_data) == 0:
#             # creating customer
#             customer = stripe.Customer.create(
#             email=email,
#             payment_method=payment_method_id,
#             invoice_settings={
#                 'default_payment_method': payment_method_id
#             }
#             )
#         else:
#             customer = customer_data[0]
#             extra_msg = "Customer already existed."
        
#         stripe.Subscription.create(
#             customer=customer,
#             items=[
#             {
#             'price': data['amount'] #here paste your price id
#             }
#             ]
#         )
#     except Exception as e:
#         raise Exception(str(e))
#     else:
#         return { 'curtomer_id': customer.id,'extra_msg':extra_msg }


# def EblPayment(data):
#     try:
#         ebl_config = EBLConfig.objects.get()
#         if ebl_config.testMode:
#             ebl_merchant_id = ebl_config.testMerchantId
#             ebl_merchant_password = ebl_config.testPassword
#             ebl_merchant_url = 'https://test-gateway.mastercard.com/api/nvp'
#             redirect_url = 'https://easternbank.test.gateway.mastercard.com/checkout/pay/'
#         else:
#             ebl_merchant_id = ebl_config.merchantId
#             ebl_merchant_password = ebl_config.password
#             ebl_merchant_url = 'https://ap-gateway.mastercard.com/api/nvp'
#             redirect_url = 'https://easternbank.ap.gateway.mastercard.com/checkout/pay/'

#         headers = {
#             "Content-Length": "20",
#             "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
#         }
#         body_data = {
#                 "merchant": ebl_merchant_id,
#                 "apiPassword": ebl_merchant_password,
#                 "apiUsername": 'merchant.'+ebl_merchant_id,
#                 "apiOperation": "INITIATE_CHECKOUT",
#                 "order.id": data['order_id'],
#                 "order.amount": data['amount'],
#                 "order.description": data['description'],
#                 "order.currency": data['currency'],
#                 "interaction.cancelUrl": data['cancel_url'],
#                 "interaction.returnUrl": data['return_url'],
#                 "interaction.operation": "PURCHASE",
#                 "interaction.timeout": "1800",
#                 "interaction.timeoutUrl": data['timeout_url'],
#                 "interaction.merchant.name": "EBL Secure Invoice",
#                 "interaction.merchant.logo": "https://caab.pod.aero/shared/images/logo/pod_logo_400.png",               
#                 "interaction.displayControl.billingAddress": "HIDE",
#                 "customer.firstName": data['name'],
#                 "customer.email": data['email'],
#                 "customer.phone": data['phone']
                                
#             }
#         response = requests.post(ebl_merchant_url+'/version/66',headers=headers,data=body_data)
#         print('response',response.text)
#         result = list(response.text.split("&"))
#         session_id = ''
#         for i in result:
#             item = i.split('=')
#             if item[0] == 'session.id':
#                 session_id = str(item[1])
#                 break
        
        
#         redirect_to = redirect_url+session_id
#     except Exception as e:
#         raise Exception(str(e))
#     else:
#         return redirect_to