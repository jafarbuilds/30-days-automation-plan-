import smtplib
import time

my_email=input("My email:")
password= input("password:")



file=open(r"C:\Users\Dell 7490\OneDrive\Documents\GitHub\30-days-automation-plan-\week1\recipients.txt","r")

email_list=[line.strip() for line in file.readlines()]


server=smtplib.SMTP("smtp.gmail.com",587)
server.starttls()

server.login(my_email,password)

file.close()

for email in email_list:
 try:
        print(f"preparing to send email to :{email}")

        

        message="Subject: Hello this is my bulk email test!"
        server.sendmail(my_email,email,message)
        print(f"Successfully sent to {email}")


 except Exception as e:
     print(f"Failed to send to {email}because of {e}")

server.quit