from django.core.mail import send_mail
from django.conf import settings

sender = settings.EMAIL_HOST_USER
adminEmail = settings.ADMIN_EMAIL

def admin_alert(alert, message):
    match alert:
        case "dm":
            subject = "PP new message!"
            message = f"feedback: {message}\n\n"

    receiver = [adminEmail,]
    send_mail(
        subject,
        message,
        sender,
        receiver,
        fail_silently=False,
    )