API Library Technical Documentation


Table of Contents:

Introduction	1
Authentication & Authorization, Access Control	1
Notification System	4
Internal Notification:	5
SMS:	6
Email:	6
Integrate with frontend react:	7
Payment	7
Integrate Payment Gateway With Frontend:	8



Introduction
The API Library is a collection of modules and functionalities aimed at providing an easy to use and intuitive interface for authentication and authorization, access control, activity logging, document handling, notification system, payment gateway and system setting. The library utilizes various third-party packages such as Django Rest Framework, Django Rest Password Reset, and SimpleJWT for its functionalities. This documentation aims to guide the users on how to install and integrate the API Library into their existing Django project.

Authentication & Authorization, Access Control

The API Library offers a robust solution for user authentication and authorization. The library leverages the SimpleJWT package to provide JSON Web Token (JWT) authentication for the users. The library also offers password reset functionality through the Django Rest Password Reset package.
To integrate the API Library for authentication and authorization into an existing Django project, follow these steps:
1. Install the required dependencies using the following command: pip install django-phonenumber-field djangorestframework djangorestframework-simplejwt phonenumbers django-rest-passwordreset Pillow.
2. Add the following modules to the INSTALLED_APPS setting: django_rest_passwordreset, phonenumber_field, user.
3. In the settings.py file, add the following lines of code for JWT token authentication:




REST_FRAMEWORK = {
            'COERCE_DECIMAL_TO_STRING': False,
            'DEFAULT_PERMISSION_CLASSES': [
                'rest_framework.permissions.DjangoModelPermissions'
            ],
            'DEFAULT_AUTHENTICATION_CLASSES': [
                    'rest_framework_simplejwt.authentication.JWTAuthentication'
            ],
            
        }

        
SIMPLE_JWT = {
            'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
            'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
            'ROTATE_REFRESH_TOKENS': False,
            'BLACKLIST_AFTER_ROTATION': False,
            'UPDATE_LAST_LOGIN': False,

            'ALGORITHM': 'HS256',
            'SIGNING_KEY': SECRET_KEY,
            'VERIFYING_KEY': None,
            'AUDIENCE': None,
            'ISSUER': None,
            'JWK_URL': None,
            'LEEWAY': 0,

            'AUTH_HEADER_TYPES': ('Bearer',),
            'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
            'USER_ID_FIELD': 'id',
            'USER_ID_CLAIM': 'user_id',
            'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

            'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
            'TOKEN_TYPE_CLAIM': 'token_type',
            'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

            'JTI_CLAIM': 'jti',
            'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
            'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
            'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
        }

 AUTH_USER_MODEL = 'user.User'




4. Include the User Auth URLconf in your project urls.py like this::

    path('', include('user.urls')),

5. Run ``python manage.py migrate`` to create the User Auth models.

6. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a user (you'll need the Admin app enabled).

7. Visit http://127.0.0.1:8000/api/user/ to participate in the user auth.

 All the url for particular action is given below(note: for details follow the api documentation),
    user registration, url: http://127.0.0.1:8000/api/user/users/ , method: post, body: 
    login, url: http://127.0.0.1:8000/api/user/auth/ , method: post, body: username,password
    update profile , http://127.0.0.1:8000/api/user/update_profile/ , method: post
    get user role, http://127.0.0.1:8000/api/user/user_role/ , method: get
    path('change_password/',change_password),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),



Activity Log

The API Library offers a robust solution for Activity Log. The Module offers Auth Log functionality and also user click based and non click based activity log functionality.
To integrate the API Library for Activity Log into an existing Django project, follow these steps:
1. Add this to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = [
        ...
        'activityLog',
    ]
2. Include the Activity Log URLconf in your project urls.py like this::

    path('', include('activityLog.urls')),

3. Run ``python manage.py migrate`` to create the ActivityLog models.


4. Visit http://127.0.0.1:8000/api/activity_log/ to participate in the user auth.

All the url for particular action is given below(note: for details follow the api documentation),
    auth log, url: http://127.0.0.1:8000/api/auth_log/ , method: get 
    activity log, url: http://127.0.0.1:8000/api/activity_log/ , method: get,post 




Notification System


The API Library offers a robust solution for Notification System. The Module offers  Real time Internal notification system functionality  , send sms, send email functionality.
To integrate the API Library for Activity Log into an existing Django project, follow these steps:
1. Install the required dependencies using the following command: pip install twilio, celery, django-celery-beat, django-celery-results, channels['daphne'], channels_redis

1. Add this to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        'daphne',
        ...
        'notification',
        'django_celery_beat',
        'django_celery_results'

    ]
add this in settings.py,

 for celery:

            
CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SELERLIZER = 'json'
CELERY_TIMEZONE = 'Asia/Dhaka'




Internal Notification:
This module offers schedule , non-schedule and broadcasting real time internal notification.
Set channel layer for real time internal notification:
          
 CHANNEL_LAYERS = {
                    "default": {
                        "BACKEND": "channels_redis.core.RedisChannelLayer",
                        "CONFIG": {
                            "hosts": [(os.environ.get('HOSTS'), 6379)],
                        },
                    },
                }




SMS:
This module offers scheduled , non-scheduled sms.
 set twilio sid and token in settings.py for send sms:
            
TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')


Email:
This module offers scheduled , non-scheduled email.
Set configuration in settings.py for email send:

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')

2. Include the Activity Log URLconf in your project urls.py like this::
    path('api/', include('notification.urls')),

3. Run ``python manage.py migrate`` to create the Notification,SMS,Email related models.


5. Visit http://127.0.0.1:8000/api/notifications/ to set broadcast and schedule notification.

All the url for particular action is given below(note: for details follow the api documentation),
    set sms config, url: http://127.0.0.1:8000/api/sms_config/ , method: get,post,put,delete 
    set sms schedule, url: http://127.0.0.1:8000/api/sms_schedule/ , method: get,post,put,delete
    set email schedule, url: http://127.0.0.1:8000/api/email_schedule/ , method: get,post,put,delete
    send sms, url: http://127.0.0.1:8000/api/send_sms/ , method: post
    send email, url: http://127.0.0.1:8000/api/send_email/ , method: post
    send notification, url: http://127.0.0.1:8000/api/send_notification/ , method: post

Integrate with frontend react:
    -> npm install websocket
     import w3cwebsocket :
     import { w3cwebsocket as W3CWebSocket } from "websocket";

    -> set client for web socket connection and send and receive:
  const client = new W3CWebSocket('ws://127.0.0.1:8000/ws/notification/' + room + '/');
    
    -> pass client in every components for functionality:
    -> receive and set state:
        

socket.onmessage = (message) => {
            
            setNotifications((prev) => [...prev,  JSON.parse(message.data)]);
            
        }





Payment

This Module offers a robust solution for multi payment methods. This Module offers payment  functionality for multiple currencies.
To integrate the API Library for payment into an existing Django project, follow these steps:


Install the required dependencies using the following command: pip install –upgrade stripe
Add this to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = [
        ...
        ‘payment’,
    ]
Include the Activity Log URLconf in your project urls.py like this::

    	path('', include(payment.urls')),

Setup api key config:
STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY')

Run ``python manage.py migrate`` to create the Payment and Currency models.


Visit http://127.0.0.1:8000/api/payment/ to participate in the user auth.

All the url for particular action is given below(note: for details follow the api documentation),
    Payment crud, url: http://127.0.0.1:8000/api/payment/, method: get,post,patch,delete
    Currency crud, url: http://127.0.0.1:8000/api/currency/, method: get,post,patch,delete
    Test payment, url: http://127.0.0.1:8000/api/test-payment/ , method: post
    Stripe payment, url: http://127.0.0.1:8000/api/stripe-payment/ , method: post
    Stripe Subscription, url: http://127.0.0.1:8000/api/stripe-payment-subscription/ ,    method: post 


Integrate Payment Gateway With Frontend:
	-> install stripe dependency with command: npm install @stripe/react-stripe-js @stripe/stripe-js




	-> Sample Code for integration:
	App.js:
	
import './App.css';
import {Elements} from '@stripe/react-stripe-js';
import {loadStripe} from "@stripe/stripe-js/pure";
import CheckoutForm from "./components/CheckoutForm";
const stripePromise = loadStripe('pk_test_51MNt4eLelMOFYUcqYR4J2pJc1BJB12peSjKajyRZQ7173tjHIvK3bLJOsAeD0oydugU0pFB2h9h9Za2NG2JSSdJ600ZAGmA04b');
const App = () => (
 <Elements stripe={stripePromise}>
   <CheckoutForm />
 </Elements>
);
export default App;


	CheckoutForm.js:

	


import {CardElement, useElements, useStripe} from "@stripe/react-stripe-js";
import React, {useState} from "react";
import ApiService from "../api";


const Checkout = () => {
 const [error, setError] = useState(null);
 const [email, setEmail] = useState('');
 const stripe = useStripe();
 const elements = useElements();
// Handle real-time validation errors from the CardElement.
const handleChange = (event) => {
 if (event.error) {
   setError(event.error.message);
 } else {
   setError(null);
 }
}






// Handle form submission.
const handleSubmit = async (event) => {
 event.preventDefault();
 const card = elements.getElement(CardElement);
// add these lines
 const {paymentMethod, error} = await stripe.createPaymentMethod({
    type: 'card',
    card: card
});


ApiService.saveStripeInfo({
   email, payment_method_id: paymentMethod.id})
 .then(response => {
   console.log(response.data);
 }).catch(error => {
   console.log(error)
 })
}




return (
 <>
 <form onSubmit={handleSubmit} className="stripe-form">
   <div className="form-row">
     <label htmlFor="email">Email Address</label>
     <input className="form-input" id="email" name="name"    type="email" placeholder="jenny.rosen@example.com" required
value={email} onChange={(event) => { setEmail(event.target.value)}} />
   </div>
   <div className="form-row">
     <label for="card-element">Credit or debit card</label>
     <CardElement id="card-element" onChange={handleChange}/>
     <div className="card-errors" role="alert">{error}</div>
   </div>
   <button type="submit" className="submit-btn">
     Submit Payment
   </button>
 </form>
 </>
);
};
export default Checkout;


