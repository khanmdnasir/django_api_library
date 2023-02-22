==============================================
Authentication & Authorization, Access Control
==============================================

User Auth is a Django app to conduct web-based User Auth. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------
0. Dependency you have to install: pip install django-phonenumber-field djangorestframework djangorestframework-simplejwt phonenumbers django-rest-passwordreset Pillow
1. Add this to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_rest_passwordreset',
        'phonenumber_field',
        'user',

    ]

    add this in settings.py file for jwt token authentication:

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



2. Include the User Auth URLconf in your project urls.py like this::

    path('', include('user.urls')),

3. Run ``python manage.py migrate`` to create the User Auth models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a user (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/api/user/ to participate in the user auth.

6. all the url for particular action is given below(note: for details follow the api documentation),
    user registration, url: http://127.0.0.1:8000/api/user/users/ , method: post, body: 
    login, url: http://127.0.0.1:8000/api/user/auth/ , method: post, body: username,password
    update profile , http://127.0.0.1:8000/api/user/update_profile/ , method: post
    get user role, http://127.0.0.1:8000/api/user/user_role/ , method: get
    path('change_password/',change_password),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),



============
Activity Log
============


Quick start
-----------

1. Add this to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'activityLog',

    ]

2. Include the Activity Log URLconf in your project urls.py like this::

    path('', include('activityLog.urls')),

3. Run ``python manage.py migrate`` to create the ActivityLog models.


5. Visit http://127.0.0.1:8000/api/activity_log/ to participate in the user auth.

6. all the url for particular action is given below(note: for details follow the api documentation),
    auth log, url: http://127.0.0.1:8000/api/auth_log/ , method: get 
    activity log, url: http://127.0.0.1:8000/api/activity_log/ , method: get,post 


===================
Notification System
===================


Quick start
-----------
0. Dependency you have to install: pip install twilio, celery, django-celery-beat, django-celery-results, channels['daphne'], channels_redis

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

        for channels:

            CHANNEL_LAYERS = {
                    "default": {
                        "BACKEND": "channels_redis.core.RedisChannelLayer",
                        "CONFIG": {
                            "hosts": [(os.environ.get('HOSTS'), 6379)],
                        },
                    },
                }

        set twilio sid and token for send sms:
            TWILIO_SID = os.environ.get('TWILIO_SID')
            TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')

2. Include the Activity Log URLconf in your project urls.py like this::

    path('api/', include('notification.urls')),


3. Run ``python manage.py migrate`` to create the Notification,SMS,Email related models.


5. Visit http://127.0.0.1:8000/api/notifications/ to set broadcast and schedule notification.

6. all the url for particular action is given below(note: for details follow the api documentation),
    set sms config, url: http://127.0.0.1:8000/api/sms_config/ , method: get,post,put,delete 
    set sms schedule, url: http://127.0.0.1:8000/api/sms_schedule/ , method: get,post,put,delete
    set email schedule, url: http://127.0.0.1:8000/api/email_schedule/ , method: get,post,put,delete
    send sms, url: http://127.0.0.1:8000/api/send_sms/ , method: post
    send email, url: http://127.0.0.1:8000/api/send_email/ , method: post
    send notification, url: http://127.0.0.1:8000/api/send_notification/ , method: post

7. integrate with frontend react:
    -> npm install websocket
    -> import w3cwebsocket :
        import { w3cwebsocket as W3CWebSocket } from "websocket";

    -> set client for web socket connection and send and receive:
        const client = new W3CWebSocket('ws://127.0.0.1:8000/ws/notification/' + room + '/');
    
    -> pass client in every components for functionality:
    -> receive and set state:
        socket.onmessage = (message) => {
            
            setNotifications((prev) => [...prev, JSON.parse(message.data)]);
            
        }