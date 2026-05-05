import os
import smtplib
import csv
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

my_email = input("My email: ")
password = input("App password: ")

with open("30-days-automation-plan-/week1/template.txt") as f:
    template = f.read()
    
with open("30-days-automation-plan-/week1/recipients.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row["name"]
        email = row["email"]

        # personalize message
        body = template.format(name=name)

        # create email container
        msg = MIMEMultipart()
        msg["From"] = my_email
        msg["To"] = email
        msg["Subject"] = "Automated Email Test"

        msg.attach(MIMEText(body, "plain"))

        try:
            server.sendmail(my_email, email, msg.as_string())
            print(f"Sent to {email}")

            with open("log.txt","a") as log:
                log.write(f"SUCCESS: {email}\n")

        except Exception as e:
            print(f"Failed to send to {email}: {e}")

            with open("log.txt","a") as log:
                log.write(f"FAILED: {email} - {e}\n")

        # delay so Gmail doesn't flag spam
        time.sleep(3)