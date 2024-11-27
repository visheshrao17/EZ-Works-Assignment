from flask_mail import Message
from app import mail

def send_verification_email(email, verification_link):
    msg = Message("Verify Your Email", recipients=[email])
    msg.body = f"Click the link to verify your email: {verification_link}"
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
