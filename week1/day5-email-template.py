import os
import smtplib
import csv 
import time

time.sleep(2)

print("CURRENT FOLDER:", os.getcwd())
print("FILES INSIDE:", os.listdir())

server=smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
my_email=input("My email:")

from getpass import getpass
password = input("Enter your app password:",)

server.login(my_email,password)


with open("C:/Users/Dell 7490/OneDrive/Documents/GitHub/30-days-automation-plan-/week1/template.txt") as f:
    template = f.read()

with open("30-days-automation-plan-/week1/recipients.csv", newline="") as file:
    reader= csv.DictReader(file)
    for row in reader:
        print(row)
        name= row["name"]
        email= row["email"]
        message= template.format(name=name)
        try:
            server.sendmail(my_email, email, message)
            print(f"Sent to {email}")
        except Exception as e:
           print(f"Failed to send to {email}: {e}")

        with open("log.txt","a") as log:
         log.write(f"Sent to {email}\n")

server.quit()



