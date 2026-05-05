import smtplib
import csv
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass

# LOGIN
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

my_email = input("My email: ")
password = input("App password: ")

for attempt in range(3):
    try:
        server.login(my_email, password)
        print("Login successful")
        break
    except Exception as e:
        print(f"Login failed (attempt {attempt+1}): {e}")
        time.sleep(2)

# LOAD TEMPLATE
with open("30-days-automation-plan-/week1/template.txt") as f:
    template = f.read()

# READ CSV
with open("30-days-automation-plan-/week1/recipients.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row["name"]
        email = row["email"]

        # CREATE EMAIL
        msg = MIMEMultipart()
        msg["From"] = my_email
        msg["To"] = email
        msg["Subject"] = "Special Message for You 👀"

        # HTML CONTENT
        html_content = f"""
        <html>
            <body>
                <h2>Hello {name},</h2>
                <p>This is a <b>professional automated email</b>.</p>
                <p>Built with Python 😎</p>
            </body>
        </html>
        """

        msg.attach(MIMEText(html_content, "html"))

        try:
            server.sendmail(my_email, email, msg.as_string())
            print(f"✅ Sent to {email}")

            with open("log.txt", "a") as log:
                log.write(f"Sent to {email}\n")

        except Exception as e:
            print(f"❌ Failed: {email} | {e}")

        # DELAY (IMPORTANT)
        time.sleep(3)

server.quit()