"""
Django settings for build_interface project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from dotenv import load_dotenv
from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.contrib.auth import get_user_model


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class CookieJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get('token')
        if not token:
            return None
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except Exception:
            raise AuthenticationFailed('Invalid token')

        user = self.get_or_create_user(payload)

        return (user, token)

    def get_or_create_user(self, payload):
        username = payload.get('username', None)
        if username != os.environ.get('ART_DASH_PRIVATE_USER'):
            raise AuthenticationFailed('Invalid token payload')

        User = get_user_model()
        user, _ = User.objects.get_or_create(username=username)
        return user


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COMMON_ENV_FILE = 'conf/common.env'
CONF_FILE = 'conf/prod.env'

if "RUN_ENV" in os.environ:
    if os.environ["RUN_ENV"] == "development":
        CONF_FILE = 'conf/dev.env'
    elif os.environ["RUN_ENV"] == "production":
        CONF_FILE = 'conf/prod.env'
    else:
        print("Invalid run environment.")
        exit(1)
else:
    print("Run environment missing in environment variables.")
    exit(1)

load_dotenv(f"{BASE_DIR}/{COMMON_ENV_FILE}")
load_dotenv(f"{BASE_DIR}/{CONF_FILE}")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    # safe value used for development when DJANGO_SECRET_KEY might not be set
    '9e4@&tw46$l31)zrqe3wi+-slqm(ruvz&se0^%9#6(_w3ui!c0'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'art-dash-server-art-dashboard-server.apps.artc2023.pc3z.p1.openshiftapps.com'
]


# Application definition

INSTALLED_APPS = [
    'api',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'incident_reports',
    'build_health',
    'build',
    'ocp_build_data',
    'autocomplete',
    'django_extensions',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'build_interface.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'build_interface.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     # 'default': {
#     #     'ENGINE': 'django.db.backends.sqlite3',
#     #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     # }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ["MYSQL_DB_NAME"],
        'USER': os.environ["MYSQL_USER"],
        'PASSWORD': os.environ["MYSQL_PASSWORD"],
        'HOST': os.environ["MYSQL_HOST"],
        'PORT': int(os.environ["MYSQL_CONNECTION_PORT"]),
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# TO DO: setup CORS
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',
#     'https://art-dash.engineering.redhat.com',
#     'http://art-dash-hackspace-martin.apps.artc2023.pc3z.p1.openshiftapps.com'
# ]

SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_DOMAIN = ".apps.artc2023.pc3z.p1.openshiftapps.com"

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'build_interface.settings.CookieJWTAuthentication',
        'build_interface.settings.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'page',
]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'http://localhost',
    'https://art-dash.engineering.redhat.com',
    'https://art-dash-art-dashboard-ui.apps.artc2023.pc3z.p1.openshiftapps.com'
]

CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
