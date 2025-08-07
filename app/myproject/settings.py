from pathlib import Path
from decouple import config, Csv  
import boto3
import json
import os

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'myapp' / 'templates' ],
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

LANGUAGE_CODE = 'ja'  
TIME_ZONE = 'Asia/Tokyo'  
USE_I18N = True  
USE_TZ = True  

WSGI_APPLICATION = 'myproject.wsgi.application'


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'myapp' / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

env = os.environ.get("ENV_NAME", "production")

if env == "local":
    #ローカル
    
    SECRET_KEY = config('DJANGO_SECRET_KEY')

    DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)
    ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', cast=Csv())

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('MYSQL_DATABASE'),
            'USER': config('MYSQL_USER'),
            'PASSWORD': config('MYSQL_PASSWORD', default=config('MYSQL_ROOT_PASSWORD')),
            'HOST': config('MYSQL_HOST', default='db'),
            'PORT': config('MYSQL_PORT', default='3306'),
        }
    }

else:
    #本番

    def get_secret(secret_name):
        region = os.environ.get("AWS_REGION", "ap-northeast-1")
        client = boto3.client("secretsmanager", region_name=region)
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response["SecretString"])

    secrets = get_secret("skima-secrets")

    SECRET_KEY = secrets["DJANGO_SECRET_KEY"]
    DEBUG = False
    ALLOWED_HOSTS = secrets["DJANGO_ALLOWED_HOSTS"].split(",")  # カンマ区切り

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': secrets["DB_NAME"],
            'USER': secrets["DB_USER"],
            'PASSWORD': secrets["DB_PASSWORD"],
            'HOST': secrets["DB_HOST"],
            'PORT': '3306',
        }
    }