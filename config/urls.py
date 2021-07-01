from authbroker_client import urls as authbroker_client_urls

from django.conf.urls import include
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include(authbroker_client_urls)),
]
