from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta
from constance import config


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = os.environ.get('SECRET_KEY')


DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_rest_passwordreset',
    'phonenumber_field',
    'constance',
    'user',
    'appSettings',
    'activityLog',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT')
    }
}

#Email Setttings

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')


# Password validation


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

CONSTANCE_ADDITIONAL_FIELDS = {
    'storage_select': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': (("local", "local"), ("aws", "aws"), ("gcp", "gcp"))
    }],
}

CONSTANCE_CONFIG = {
    'SELECT_STORAGE': ('local', 'select storage', 'storage_select'),
}

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media'


# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# GS_ACCESS_KEY_ID = os.environ.get('GS_ACCESS_KEY_ID')
# GS_SECRET_ACCESS_KEY = os.environ.get('GS_SECRET_ACCESS_KEY')
# GS_STORAGE_BUCKET_NAME = os.environ.get('GS_STORAGE_BUCKET_NAME')
# DEFAULT_FILE_STORAGE = 'storages.backends.gs.GSBotoStorage'


# Default primary key field type


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



#rest framework settings

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

CONSTANCE_REDIS_CONNECTION = 'redis://localhost:6379/0'

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = [
#     'https://localhost:3000',
# ]
CSRF_TRUSTED_ORIGINS = ['http://localhost:5011']
FILE_UPLOAD_PERMISSIONS=0O640
AUTH_USER_MODEL = 'user.User'
