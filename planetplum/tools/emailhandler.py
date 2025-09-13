from django.core.mail import send_mail
from django.conf import settings

sender = settings.EMAIL_HOST_USER
adminEmail = settings.ADMIN_EMAIL

def admin_alert(alert, message=None):
    match alert:
        case "dm":
            subject = "PP new message!"
            message = f"feedback: {message}\n\n"
        case "approval request":
            subject = "PP admin approval request"
            message = "new Omaha Underground admin approval request dude"

    receiver = [adminEmail,]
    try:
        send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False,
        )
    except:
        pass
        #CHANGE TO ADMIN PANEL THINGY