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

for line in email_list:
    try:

      name,email=line.split(",")

      print(f"Preparing to send personalized email to:{name}({email})")
      subject=f"Subject:Hello {name}, quick test\n\n"
      body=f"\n\n This is my day 3 automation test. It workred "
      message= subject+body

      server.sendmail(my_email,email,message)
      print(f"Successfully sent to {name}")
    
    except Exception as e:
     print(f"Failed to send to {line} beacause of {e}") 


server.quit