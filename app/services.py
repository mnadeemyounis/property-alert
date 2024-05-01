from twilio.rest import Client as TwilioClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Configuration for Twilio SMS service
TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"

# Configuration for SendGrid email service
SENDGRID_API_KEY = "your_sendgrid_api_key"
SENDER_EMAIL = "your_sender_email"


def send_email(to_email: str, message: str):
    # Uncomment this code for actual implementation
    """
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject="Property Alert",
        html_content=message
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    """
    print(f"Email sent successfully to: {to_email}!")


def send_sms(to_phone: str, message: str):
    # Uncomment this code for actual implementation
    """
    try:
        client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone
        )
        print("SMS sent successfully!")
    except Exception as e:
        print(f"Failed to send SMS: {e}")
    """
    print(f"SMS sent successfully to: {to_phone}!")
