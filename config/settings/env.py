# from django_log_formatter_ecs import ECSFormatter

from .base import *  # noqa

SESSION_COOKIE_AGE = 60 * 60

SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 15768000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# INSTALLED_APPS += [  # noqa F405
#     "elasticapm.contrib.django",
# ]

ELASTIC_APM = {
    "SERVICE_NAME": "Digital Workspace",
    "SECRET_TOKEN": env("ELASTIC_APM_SECRET_TOKEN"),  # noqa F405
    "SERVER_URL": env("ELASTIC_APM_SERVER_URL"),  # noqa F405
    "ENVIRONMENT": env("APP_ENV"),  # noqa F405
    "SERVER_TIMEOUT": env("ELASTIC_APM_SERVER_TIMEOUT", default="20s"),  # noqa F405
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "ecs_formatter": {
            # "()": ECSFormatter,
        },
        "simple": {
            "format": "{asctime} {levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "ecs": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,  # noqa F405
            "formatter": "ecs_formatter",
        },
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,  # noqa F405
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": [
            "ecs",
            "stdout",
        ],
        "level": os.getenv("ROOT_LOG_LEVEL", "INFO"),  # noqa F405
    },
    "loggers": {
        "django": {
            "handlers": [
                "ecs",
                "stdout",
            ],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),  # noqa F405
            "propagate": False,
        },
        "django.server": {
            "handlers": [
                "ecs",
                "stdout",
            ],
            "level": os.getenv("DJANGO_SERVER_LOG_LEVEL", "ERROR"),  # noqa F405
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": [
                "ecs",
                "stdout",
            ],
            "level": os.getenv("DJANGO_DB_LOG_LEVEL", "ERROR"),  # noqa F405
            "propagate": False,
        },
    },
}
