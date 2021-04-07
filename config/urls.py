from authbroker_client import urls as authbroker_client_urls

from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from workflow import urls as workflow_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include(authbroker_client_urls)),
    path("workflow/", include(workflow_urls)),
]
