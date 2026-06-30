import os
import imaplib
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from groq import Groq
import time


client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MY_EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("APP_PASSWORD")

def generate_reply(customer_message):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a professional customer support agent. Reply warmly and professionally. Max 4 sentences."},
            {"role": "user", "content": f"A customer sent this: '{customer_message[:500]}'. Reply to them."}
        ]
    )
    return response.choices[0].message.content

def send_reply(to_email, subject, body):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(MY_EMAIL, PASSWORD)
    msg = MIMEMultipart()
    msg["From"] = MY_EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Re: " + subject
    msg.attach(MIMEText(body, "plain"))
    server.sendmail(MY_EMAIL, to_email, msg.as_string())
    server.quit()

def check_and_reply():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(MY_EMAIL, PASSWORD)
    mail.select("inbox")
    _, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()
    print(f"Found {len(email_ids)} unread emails")

    for eid in email_ids:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        sender = msg["From"]
        subject = msg["Subject"] or "No Subject"

        print(f"Processing: {sender}")

        if any(word in sender.lower() for word in ["no-reply", "noreply", "mailer", "notification", "donotreply"]):
            print(f"Skipping: {sender}")
            continue

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        print(f"Body length: {len(body)}")

        try:
            reply = generate_reply(body)
            send_reply(sender, subject, reply)
            print(f"Reply sent to {sender}!")
        except Exception as e:
            print(f"Error: {e}")

    mail.logout()

def main():
    print("SJR Automates - Running...")
    while True:
        check_and_reply()
        time.sleep(30)

main()