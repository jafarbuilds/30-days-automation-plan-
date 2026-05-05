import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Setup
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

my_email = input("Your Gmail: ")
password = input("App password: ")
recipient = input("Send demo reply to (email): ")
customer_message = input("Enter customer message: ")

# AI generates reply
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": """You are a professional customer support agent for a business automation service called Autoflow. Your name is Danny. Write warm, friendly but professional replies. Never use placeholder text. Keep replies short -- no more than 4 sentences."""},
        {"role": "user", "content": f"A customer sent this message: '{customer_message}'. Reply to them professionally. Sign off as Danny from Autoflow."}
    ]
)

body = response.choices[0].message.content

print("\n--- AI Generated Reply ---")
print(body)
print("--------------------------\n")

# Send email
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(my_email, password)

msg = MIMEMultipart()
msg["From"] = my_email
msg["To"] = recipient
msg["Subject"] = "Re: Your Enquiry"
msg.attach(MIMEText(body, "plain"))

try:
  server.sendmail(my_email, recipient, msg.as_string())
  print(f"Reply sent to {recipient}")
except Exception as e:
     print(f"Failed to send: {e}")

server.quit()