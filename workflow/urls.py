from django.urls import path

from workflow.views import (
    NewRequirementView,
)

urlpatterns = [
    path("new-requirement/", NewRequirementView.as_view(), name="new_requirement",),
]
