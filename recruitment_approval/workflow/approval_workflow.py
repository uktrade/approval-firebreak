# TODO - these imports must not be removed
# TODO - even though they appear unused
from recruitment_approval.tasks.create_requirement import (
    CreateRequirement,
    ReviewRequirement,
)
from recruitment_approval.tasks.find_approvers import FindApproverRecipients
from recruitment_approval.tasks.hiring_manager_approval import HiringManagerApproval
from workflow.dataclasses import Step, Workflow


ApprovalWorkflow = Workflow(
    name="approval_workflow",
    steps=[
        Step(
            step_id="create_requirement",
            task_name="create_requirement",
            start=True,
            target="alert_hiring_managers",
        ),
        Step(
            step_id="alert_hiring_managers",
            task_name="find_approver_recipients",
            target="send_approver_email",
            task_info={"group_name": "Hiring Managers"},
        ),
        Step(
            step_id="send_approver_email",
            task_name="send_email",
            target="hiring_manager_approval",
            task_info={
                "subject": "Hiring manager approval required",
                "message": "You can view the requirement at {{ flow.continue_url }}.",
                "from_email": "system@example.com",
            },
        ),
        Step(
            step_id="hiring_manager_approval",
            task_name="hiring_manager_approval",
            target=["hiring_approved", "hiring_rejected"],
        ),
        Step(
            step_id="hiring_approved",
            task_name="find_approver_recipients",
            target="hiring_approved_email",
            task_info={"group_name": "Chiefs"},
        ),
        Step(
            step_id="hiring_approved_email",
            task_name="send_email",
            target=None,
            task_info={
                "subject": "Hiring approved",
                "message": "This requirement has been approved!",
                "from_email": "system@example.com",
            },
        ),
        Step(
            step_id="hiring_rejected",
            task_name="find_approver_recipients",
            target="hiring_rejected_email",
            task_info={"group_name": "Hiring Managers"},
        ),
        Step(
            step_id="hiring_rejected_email",
            task_name="send_email",
            target="review_requirement",
            task_info={
                "subject": "Hiring rejected",
                "message": "Your requirement has been rejected for the following reason:\n{{ rejection_reason }}\n\nPlease amend your requirement at {{ flow.continue_url }}.",
                "from_email": "system@example.com",
            },
        ),
        Step(
            step_id="review_requirement",
            task_name="review_requirement",
            # target="hiring_manager_approval",
            target="find_hiring_managers",
        ),
        Step(
            step_id="find_hiring_managers",
            task_name="find_approver_recipients",
            target="notifiy_requirement_reviewed",
            task_info={"group_name": "Hiring Managers"},
        ),
        Step(
            step_id="notifiy_requirement_reviewed",
            task_name="send_email",
            target="hiring_manager_approval",
            task_info={
                "subject": "Requirement reviewed",
                "message": "This requirement has been amended and is ready for review at {{ flow.continue_url }}.",
                "from_email": "system@example.com",
            },
        ),
    ],
)
