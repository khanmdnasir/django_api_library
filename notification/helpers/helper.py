from main import settings
from twilio.rest import Client
from django.core.mail import EmailMultiAlternatives

client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)

def send_sms(data):
    to_number=""+str(data.to_number)    
    try:                
        client.messages.create(
            to=to_number, 
            from_=data.from_number,
            body=data.body)
        return True
    except Exception as e:
        print(str(e))
        return False

