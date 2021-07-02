from workflow.dataclasses import Step, Workflow


ApprovalWorkflow = Workflow(
    name="approval_workflow",
    steps=[
        Step(
            step_id="approver_email_form",
            task_name="email_form",
            start=True,
            target="send_approver_email",
            task_info={"subject": "Approval"},
        ),
        Step(
            step_id="send_approver_email",
            task_name="send_email",
            target="approver_email_form2",
            task_info={
                "subject": "Test subject 3",
                "message": "Test message 3",
                "from_email": "admin3@example.com",
                "recipient_list": ["approver3@example.com"],
            },
        ),
    ],
)
