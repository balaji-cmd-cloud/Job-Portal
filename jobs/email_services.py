from django.core.mail import send_mail
from django.conf import settings

def send_application_confirmation(application):
    """
    Sends a confirmation email to the candidate when they apply for a job.
    """
    candidate = application.user
    job = application.job
    candidate_name = f"{candidate.first_name} {candidate.last_name}".strip() or candidate.email

    subject = f"Application Received: {job.title} at {job.company_name}"
    message = (
        f"Dear {candidate_name},\n\n"
        f"Thank you for applying for the position of '{job.title}' at '{job.company_name}' through Apna!\n\n"
        f"We have successfully received your application. The recruiting team has been notified and will review your profile.\n"
        f"You can track your application status at any time on your dashboard.\n\n"
        f"Best regards,\n"
        f"The Apna Team"
    )
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[candidate.email],
        fail_silently=True
    )


def send_status_update_alert(application):
    """
    Sends an email alert to the candidate when the employer updates their application status.
    """
    candidate = application.user
    job = application.job
    candidate_name = f"{candidate.first_name} {candidate.last_name}".strip() or candidate.email

    subject = f"Application Status Update: {job.title} at {job.company_name}"
    message = (
        f"Dear {candidate_name},\n\n"
        f"Your application status for the position of '{job.title}' at '{job.company_name}' has been updated to:\n"
        f"👉 **{application.status}**\n\n"
        f"Log in to your Apna Candidate Dashboard to review details or coordinate next steps.\n\n"
        f"Best regards,\n"
        f"The Apna Team"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[candidate.email],
        fail_silently=True
    )
