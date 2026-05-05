import os 
import imaplib
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from groq import Groq
from dotenv import load_dotenv
import time

load_dotenv()


# Setup
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MY_EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("APP_PASSWORD")

print(f"Email: {MY_EMAIL}, Password length: {len(PASSWORD) if PASSWORD else 'NOT LOADED'}")

def check_emails():
    #connect to inbox
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(MY_EMAIL, PASSWORD)
    mail.select("inbox")

    #search for unread emails
    _, messages = mail.search(None, '(UNSEEN)')
    email_ids = messages[0].split()

    print(f"Found {len(email_ids)} unread emails.")
    return mail, email_ids

def main():
    print("SJR Automates - Running email reader...")
    while True:
        mail ,email_ids = check_emails()
        time.sleep(30)  # Check every 30 seconds


main()