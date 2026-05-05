import os
import smtplib
import csv
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Setup
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)


my_email = input("My email: ")
password = input("App password: ")

server.login(my_email, password)

with open("week1/recipients.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row["name"]
        email = row["email"]

        # AI generates the body instead of template
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": """You are a professional customer support agent for a Python automation service called Autoflow. Your name is Jafar. Write warm freindly but professional emails. Never use placeholder text like [Your Name] or [insert anything].Never mention account IDs or usernames. keep the emails short -- no more than 4 sentences."""},
                {"role": "user", "content": f"Write a welcome email for a new customer named {name}. Sign off as Jafar from Autoflow."}
            ]
        )

        body = response.choices[0].message.content

        # Build email
        msg = MIMEMultipart()
        msg["From"] = my_email
        msg["To"] = email
        msg["Subject"] = "Welcome!"
        msg.attach(MIMEText(body, "plain"))

        try:
            server.sendmail(my_email, email, msg.as_string())
            print(f"Sent to {email}")
            with open("log.txt", "a") as log:
                log.write(f"SUCCESS: {email}\n")
        except Exception as e:
            print(f"Failed to send to {email}: {e}")
            with open("log.txt", "a") as log:
                log.write(f"FAILED: {email} - {e}\n")

        time.sleep(3)

server.quit()
print("All done!")