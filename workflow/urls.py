from django.urls import path

from workflow.views import (
    ApprovalView,
    ApprovedView,
    NewRequirementView,
    RequirementsView,
    RequirementSubmittedView,
)

urlpatterns = [
    path("new-requirement/", NewRequirementView.as_view(), name="new_requirement",),
    path("requirements/", RequirementsView.as_view(), name="requirements", ),
    path("requirement_submitted/", RequirementSubmittedView.as_view(), name="requirement_submitted", ),
    path("approval/<uuid:requirement_id>/", ApprovalView.as_view(), name="approval", ),
    path("requirements/", ApprovedView.as_view(), name="approved", ),

]
