from authbroker_client import urls as authbroker_client_urls

from django.conf.urls import include
from django.contrib import admin
from django.urls import path

import workflow.views as workflow_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include(authbroker_client_urls)),
    path("", workflow_views.HomeView.as_view(), name="home"),
    path("flow/", workflow_views.FlowListView.as_view(), name="flow-list"),
    path("flow/new", workflow_views.FlowCreateView.as_view(), name="flow-create"),
    path("flow/<int:pk>/", workflow_views.FlowView.as_view(), name="flow"),
    path(
        "flow/<int:pk>/continue",
        workflow_views.FlowContinueView.as_view(),
        name="flow-continue",
    ),
    path(
        "flow/<int:pk>/diagram",
        workflow_views.FlowDiagramView.as_view(),
        name="flow-diagram",
    ),
]
