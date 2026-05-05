import os
import smtplib
import csv
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ── Configuration ──────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
CSV_PATH = "week1/recipients.csv"
LOG_PATH = "week3/autoflow_log.txt"

# ── AI Setup ───────────────────────────────
client = Groq(api_key=GROQ_API_KEY)

def generate_email(name):
    """Use AI to generate a personalized welcome email."""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """You are a customer support agent for a Python automation 
service called AutoFlow. Your name is Jafar. Write warm, friendly but professional emails.
Never use placeholder text like [Your Name] or [Insert anything].
Never mention account IDs or usernames. Keep emails short — max 4 sentences."""
            },
            {
                "role": "user",
                "content": f"Write a welcome email for a new customer named {name}. Sign off as Jafar from AutoFlow."
            }
        ]
    )
    return response.choices[0].message.content

# ── Email Setup ────────────
def send_email(server, sender, receiver, subject, body):
    """Send a single email."""
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    server.sendmail(sender, receiver, msg.as_string())

# ── Logging ────────────────────────────────
def log(message):
    """Write a log entry."""
    with open(LOG_PATH, "a") as f:
        f.write(message + "\n")

# ── Main Program ───────────────────────────
def main():
    my_email = input("Your email: ")
    password = input("App password: ")

    print("\n🚀 AutoFlow starting...\n")

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(my_email, password)

        with open(CSV_PATH, newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["name"]
                email = row["email"]

                try:
                    body = generate_email(name)
                    send_email(server, my_email, email, "Welcome to AutoFlow!", body)
                    print(f"✅ Sent to {email}")
                    log(f"SUCCESS: {email}")

                except Exception as e:
                    print(f"❌ Failed to send to {email}: {e}")
                    log(f"FAILED: {email} - {e}")
                time.sleep(3)

print("\n✅ All done! Check autoflow_log.txt for details.")

if __name__ == "__main__":
    main()