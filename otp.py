import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class OTPVerification:
    def __init__(self, otp_length=6, expiry_time=300):
        self.otp_length = otp_length
        self.expiry_time = expiry_time
        self.otp = None
        self.otp_expiry = None

    def generate_otp(self):
        otp = ''.join([str(random.randint(0, 9)) for _ in range(self.otp_length)])
        self.otp = otp
        self.otp_expiry = time.time() + self.expiry_time
        return otp

    def validate_otp(self, user_otp):
        if time.time() > self.otp_expiry:
            return False, "OTP expired"
        return self.otp == user_otp, "OTP is valid" if self.otp == user_otp else "Invalid OTP"

def send_otp_email(receiver_email, otp):
    sender_email = "your_email@gmail.com"
    sender_password = "your_email_password"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Your OTP Code"

    body = f"Your OTP code is {otp}. It is valid for the next 5 minutes."
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("OTP sent successfully")
    except Exception as e:
        print(f"Failed to send OTP: {e}")

otp_verification = OTPVerification()
otp = otp_verification.generate_otp()
print(f"Generated OTP: {otp}")

receiver_email = "receiver_email@example.com"
send_otp_email(receiver_email, otp)

user_otp = input("Enter the OTP you received: ")
is_valid, message = otp_verification.validate_otp(user_otp)
print(message)
