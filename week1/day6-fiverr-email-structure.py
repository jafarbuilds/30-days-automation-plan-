import os
import smtplib
import csv
from getpass import getpass
import time

# Small delay so you can see prints clearly
time.sleep(1)

print("CURRENT FOLDER:", os.getcwd())
print("FILES INSIDE:", os.listdir())

# --- SMTP setup ---
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
my_email = input("Enter your Gmail address: ")
password = getpass("Enter your app password: ")
server.login(my_email, password)

# --- Read template ---
template_path = "template.txt"
if not os.path.exists(template_path):
    print(f"Error: {template_path} not found!")
    exit()
with open(template_path) as f:
    template = f.read()

# --- Read CSV and send emails ---
csv_path = "recipients.csv"
if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found!")
    exit()

with open(csv_path, newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row.get("name")
        email = row.get("email")
        if not name or not email:
            print(f"Skipping invalid row: {row}")
            continue

        # Personalized message with subject
        message = template.format(name=name)

        try:
            server.sendmail(my_email, email, message)
            print(f"Sent to {email}")
        except Exception as e:
            print(f"Failed to send to {email}: {e}")
            continue

        # Log each sent email
        with open("log.txt", "a") as log:
            log.write(f"Sent to {email}\n")

# --- Close server connection ---
server.quit()
print("All emails processed successfully!")