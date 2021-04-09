from django.urls import path

from workflow.views import (
    ApprovalView,
    ApprovedView,
    NewRequirementView,
    RequirementsView,
    RequirementSubmittedView,
    NeedsAuthorisationView,
)

urlpatterns = [
    path("new-requirement/", NewRequirementView.as_view(), name="new_requirement",),
    path("", RequirementsView.as_view(), name="requirements", ),
    path("requirement_submitted/", RequirementSubmittedView.as_view(), name="requirement_submitted", ),
    path("approval/<uuid:requirement_id>/", ApprovalView.as_view(), name="approval", ),
    path("approved/", ApprovedView.as_view(), name="approved", ),
    path("needs-auth/<uuid:requirement_id>/", NeedsAuthorisationView.as_view(), name="needs_auth", ),

]
