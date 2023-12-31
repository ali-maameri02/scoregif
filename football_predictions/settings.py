"""
Django settings for football_predictions project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import whitenoise
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xk1xph-nmesq=&^y9l6c1uj=&s$3hlo%0krgvw)=a!*7^v38ab'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.scoregifs.com','localhost','score-gif.onrender.com','footballpredictions.local']

TWITTER_API_KEY = 'lD8MIDfbsO216w7Jh04Rzt9x9'
TWITTER_API_SECRET = 'Vje3Y4mmmMJltgc7YGGIYDGvUgzUswv91CL4kCGxXuHR2XRoOS'
ACCESS_TOKEN = '1697935934929485824-w7uBXn8EfOp43BH6xQodGuA4jByRQn'
ACCESS_TOKEN_SECRET = 'CL0MKtCDt7bGl8nsoYbYzEw4dzJ6prqgTDp3CWX9NzCEc'
TWITTER_CALLBACK_URL = 'https://score-gif.onrender.com/twitter/callback'


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
        'django.contrib.sites', # must
    'allauth', # must
    'allauth.account', # must
    'allauth.socialaccount', # must
    'allauth.socialaccount.providers.google', # google provider
    'allauth.socialaccount.providers.facebook', # new (facbook provider)
    'allauth.socialaccount.providers.twitter',
    'predictions',
    'social_django',
    'sslserver',
    'django_social_share',
]
SITE_ID = 1  
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
       "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    ' allauth.account.middleware.AccountMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  # <-- Here
]
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
ROOT_URLCONF = 'football_predictions.urls'

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
                # 'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                  'social_django.context_processors.backends',  # <-- Here
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'football_predictions.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
JAZZMIN_SETTINGS = {
    "site_title": "Score_gif",
      "site_brand": "Score_gif",
     "site_header": "Score_gif",
         "site_logo": "images/logo.png",
              "welcome_sign": "Welcome to the Admin panel!",
                  "site_logo_classes": "img-circle",
                      'icons': {
        
        'predictions.Tournament':'fa fa-trophy',
        'predictions.Match':'fa-solid fa-drum',
        'predictions.Prediction':'fas fa-dice-six',
        'predictions.Team':'far fa-futbol',
        'auth.User':'fa fa-user',
        'auth.Group':'fa fa-users',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
     ('en', ('English')),
#     ('ar', ('Arabic')),
 ]

TIME_ZONE = 'UTC'

# USE_I18N = True
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
USE_TZ = True
# USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'football_predictions/static')
]
# STORAGES = {
#     # ...
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# JAZZMIN_SETTINGS = {
#     "language_chooser": True,
# }
AUTHENTICATION_BACKENDS = [
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
        # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# SSL/TLS settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# LOGIN_URL = 'home'
LOGOUT_URL = 'logout'
# LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
THIRD_PARTY_APPS = [
        'social_django',

]

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'APP': {
            'client_id': '1215879345774527',
            'secret': '87da695826fb27b9f8b14f8b17a1f831',
        }
    }
}
# SOCIALACCOUNT_PROVIDERS = {
#     'twitter': {
#         'APP': {
#             'client_id': 'WjZmU1hpZW9nRXBWWEEzRTlJRF86MTpjaQ',
#             'secret': 'CEnqWk2O707ZSTav16QS4l1sOIIFm2_ibxrltR6G1y0idafoHn',
#         }
#     }
# }

# SOCIAL_AUTH_FACEBOOK_KEY = '251823957759951'  # App ID
# SOCIAL_AUTH_FACEBOOK_SECRET = '8b87c47b4947e47dcc03cebe1087eb46'  # App Secret
# SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'facebook/callback/'  # L'URL de redirection après l'authentification
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_IGNORE_SSL_VERIFICATION = True
SOCIAL_AUTH_CREATE_USERS = True
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email, age_range'
}

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True


SECURE_SSL_KEY = 'football_predictions/localhost.key'
SECURE_SSL_CERT = 'football_predictions/localhost.crt'
SOCIALACCOUNT_QUERY_EMAIL = True
LOGIN_URL = 'home'  # Replace with your login URL
LOGIN_REDIRECT_URL = 'home'   # Replace with your desired redirect URL


SOCIAL_AUTH_FACEBOOK_API_VERSION = '17.0'

# SOCIALACCOUNT_FORMS = {
#     'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
#     'signup': 'allauth.socialaccount.forms.SignupForm',
# }