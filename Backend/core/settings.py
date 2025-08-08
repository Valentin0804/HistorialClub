from pathlib import Path
from decouple import config
import os
import environ
import dj_database_url
import core.db as db

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Inicializa django-environ
env = environ.Env()

# Lee el archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Docker
hosts = os.environ.get("ALLOWED_HOSTS", "127.0.0.1")
ALLOWED_HOSTS = [host.strip() for host in hosts.split(',')]

# Lee CSRF_TRUSTED_ORIGINS desde una variable de entorno, también como una lista.
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in config('CSRF_TRUSTED_ORIGINS', default='').split(',') if origin.strip()]

# DEBUG para Docker
DEBUG = os.environ.get("DEBUG", "True")

if not DEBUG:
    SECRET_KEY = os.environ.get('SECRET_KEY')
else:
    SECRET_KEY = 'sv3bn4w^rir+zz4@jh_cse38bi3sxh#3s-3ro@yybzrmk98=bp'

# DOCKER 
USE_DOCKER = os.environ.get('USE_DOCKER', 'False')


print(f"DEBUG: {DEBUG}")
print(f"USE_DOCKER: {USE_DOCKER}")
# Esta es la nueva lógica, mucho más robusta
if USE_DOCKER == 'True':
    print("DB -> Usando PostgreSQL (Entorno Docker)")
    DATABASES = db.DATABASE_URL
elif DEBUG == "True":
    print("DB -> Usando MySQL (Entorno Local, sin Docker)")
    DATABASES = db.LOCAL_MYSQL
else:
     # Este caso se aplicaría para producción sin Docker
     print("DB -> Usando PostgreSQL (Producción)")
     DATABASES = db.DATABASE_URL



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'historial',        
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'historial/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

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

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuración de Cookies Seguras
# Asegura que las cookies solo se envíen a través de una conexión HTTPS segura.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Configuración para Proxies (Opcional pero muy recomendado)
# Ayuda a Django a identificar correctamente que la conexión es segura (https)
# cuando está detrás del proxy de Railway.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
