import stripe,requests
from payment.models import EBLConfig,StripeConfig

def SetStripeConfig():    
    stripe_config = StripeConfig.objects.get()    
    if(stripe_config.testMode):
        stripe.api_key = stripe_config.test_stripe_api_key
    else:
        stripe.api_key = stripe_config.stripe_api_key
    

def stripe_payment_integration(data):
    try:
        SetStripeConfig()
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
    except Exception as e:
        raise Exception(str(e))
    else:
        return { 'customer_id': customer.id,'extra_msg':extra_msg }

def stripe_subscription_payment_integration(data):
    try:
        SetStripeConfig()
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
            'price': data['amount'] #here paste your price id
            }
            ]
        )
    except Exception as e:
        raise Exception(str(e))
    else:
        return { 'curtomer_id': customer.id,'extra_msg':extra_msg }

def EblPayment(data):
    try:
        ebl_config = EBLConfig.objects.get()
        if ebl_config.testMode:
            ebl_merchant_id = ebl_config.testMerchantId
            ebl_merchant_password = ebl_config.testPassword
            ebl_merchant_url = 'https://test-gateway.mastercard.com/api/nvp'
            redirect_url = 'https://easternbank.test.gateway.mastercard.com/checkout/pay/'
        else:
            ebl_merchant_id = ebl_config.merchantId
            ebl_merchant_password = ebl_config.password
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
                "order.id": data['order_id'],
                "order.amount": data['amount'],
                "order.description": data['description'],
                "order.currency": data['currency'],
                "interaction.cancelUrl": data['cancel_url'],
                "interaction.returnUrl": data['return_url'],
                "interaction.operation": "PURCHASE",
                "interaction.timeout": "1800",
                "interaction.timeoutUrl": data['timeout_url'],
                "interaction.merchant.name": "EBL Secure Invoice",
                "interaction.merchant.logo": "https://caab.pod.aero/shared/images/logo/pod_logo_400.png",               
                "interaction.displayControl.billingAddress": "HIDE",
                "customer.firstName": data['name'],
                "customer.email": data['email'],
                "customer.phone": data['phone']
                                
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
        raise Exception(str(e))
    else:
        return redirect_to