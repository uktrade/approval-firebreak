from authbroker_client import urls as authbroker_client_urls

from django.conf.urls import include
from django.contrib import admin
from django.urls import path

import app_with_workflow.views as workflow_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include(authbroker_client_urls)),
    path("flow/", workflow_views.FlowListView.as_view(), name="flow-list"),
    path("flow/new", workflow_views.FlowCreateView.as_view(), name="flow-create"),
    path("flow/<int:pk>/", workflow_views.FlowView.as_view(), name="flow"),
    path(
        "flow/<int:pk>/start", workflow_views.FlowStartView.as_view(), name="flow-start"
    ),
    path(
        "flow/<int:pk>/proceed",
        workflow_views.FlowProceedView.as_view(),
        name="flow-proceed",
    ),
]
