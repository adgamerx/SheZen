import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = "smtp.elasticemail.com"
smtp_port = 2525
smtp_username = "bhavyabhagwani00@gmail.com"
smtp_password = "88BA2D773ACCBA0266E993D27582CFBF4B90"
from_email = "bhavyabhagwani00@gmail.com"
def send_mail(to_email, message, subject):
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully")
        return True
    except Exception as e:
        print("Email sending failed:", str(e))
        return False

    finally:
        server.quit()

def verification_mail(verification_code, name, email):
    message = """
    Hello {name},

    Thank you for signing up. To complete your registration, please click the link below to verify your email address:

    http://localhost:5000/verify?code={verification_code}

    If you did not request this verification, please ignore this email.

    Regards,
    Team SheZen
    """
    subject = "Please Verify Your Email Address"
    return send_mail(to_email=email, message=message, subject=subject)
