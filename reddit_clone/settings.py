from pathlib import Path
import os

ALLOWED_HOSTS = ["*"]
SECRET_KEY = "ww(n4z2v-r$pya*!w4sjbit6fh&q9s90v(gol(y%-i^x98s(6u"
BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    # My Apps
    "main.apps.MainConfig",
    "accounts.apps.AccountsConfig",
    # DEFAULT apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps
    "mptt",
    "storages",
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "reddit_clone.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "reddit_clone.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# HEROKU DEPLOY
import django_heroku

django_heroku.settings(locals())

# S3 BUCKETS CONFIG
AWS_ACCESS_KEY_ID = "AKIAVUQ7VH3IUA7YA3UR"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "sashasergeev-redditclonedjango"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_HOST = "s3.eu-north-1.amazonaws.com"
AWS_S3_REGION_NAME = "eu-north-1"

# DEBUG SETTINGS
# DEBUG = True
DEBUG = os.environ.get("DEBUG") == "True"

INTERNAL_IPS = [
    "127.0.0.1",
]
