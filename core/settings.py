"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "=%u8t#$)rqtu^%b%)%s$xo=u!pwv)44_d(%^wc)51wa!)oogd*"

SIGNING_KEY = "4@owu(!2yd65ez8en0&32j-h#=@ak3@@1w$z=ju$#8n)1uy&^8"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third
    "corsheaders",
    "rest_framework",
    "rest_framework_roles",
    "drf_yasg",
    "django_filters",
    "django_extensions",
    # author
    "plus_planner",
]

AUTH_USER_MODEL = "plus_planner.User"

DEFAULT_AUTHENTICATION_CLASSES = [
    "rest_framework_simplejwt.authentication.JWTAuthentication",
]

DEFAULT_FILTER_BACKENDS = [
    "django_filters.rest_framework.DjangoFilterBackend",
]

DEFAULT_PAGINATION_CLASS = "django_filters.rest_framework.DjangoFilterBackend"

REST_FRAMEWORK = {
    # Return 'error' key instead of non_field_errors_key
    "NON_FIELD_ERRORS_KEY": "error",
    "DEFAULT_AUTHENTICATION_CLASSES": DEFAULT_AUTHENTICATION_CLASSES,
    "DEFAULT_FILTER_BACKENDS": DEFAULT_FILTER_BACKENDS,
    "DEFAULT_PAGINATION_CLASS": DEFAULT_PAGINATION_CLASS,
    "PAGE_SIZE": 12,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "200/day", "user": "2000/day"},
}

REST_FRAMEWORK_ROLES = {
    "ROLES": "plus_planner.utils.roles.ROLES",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "SIGNING_KEY": SIGNING_KEY,
    "UPDATE_LAST_LOGIN": True,
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "DEFAULT_GENERATOR_CLASS": "rest_framework.schemas.generators.BaseSchemaGenerator",
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"},
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "PlusPlanner",
        "USER": "postgres",
        "PASSWORD": "Pedro97",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# Password validation
MIN_LENGTH_PASSWORD = 8
SPECIAL_CHAR = ["!", "@", "#", "_", ".", "+", "-", "*"]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Bahia"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# LOCALE_PATHS = [
#     os.path.join(BASE_DIR, "locale"),
# ]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
