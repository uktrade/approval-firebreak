from django.urls import path

from workflow.views import (
    ApprovalView,
    ApprovedView,
    NeedsAuthorisationView,
    NewRequirementView,
    ProcessOwnerView,
    RequirementsView,
    RequirementSubmittedView,
    RequestChangesView,
    RequestSubmittedView,
    UsersView,
)

urlpatterns = [
    path("", RequirementsView.as_view(), name="requirements", ),
    path("new-requirement/", NewRequirementView.as_view(), name="new_requirement",),
    path("requirement-submitted/", RequirementSubmittedView.as_view(), name="requirement_submitted", ),
    path("approval/<uuid:requirement_id>/", ApprovalView.as_view(), name="approval", ),
    path("request-changes/<uuid:requirement_id>/", RequestChangesView.as_view(), name="request_changes", ),
    path("request-submitted/", RequestSubmittedView.as_view(), name="change_request_submitted", ),
    path("approved/", ApprovedView.as_view(), name="approved", ),
    path("needs-auth/<uuid:requirement_id>/", NeedsAuthorisationView.as_view(), name="needs_auth", ),
    path("process-owner/", ProcessOwnerView.as_view(), name="process_owner", ),
    path("users/", UsersView.as_view(), name="workflow_users", ),
]
