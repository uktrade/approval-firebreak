from authbroker_client import urls as authbroker_client_urls

from django.conf.urls import include
from django.contrib import admin
from django.urls import path

import app_with_workflow.views as workflow_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include(authbroker_client_urls)),
    path("flow/", workflow_views.FlowListView.as_view(), name="flow-list"),
    path("flow/<int:pk>/", workflow_views.FlowView.as_view(), name="flow"),
]
