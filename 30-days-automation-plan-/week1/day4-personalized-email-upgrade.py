import smtplib
import time
time.sleep(2)

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
      email=email.strip()

      print(f"Preparing to send personalized email to:{name}({email})")
      subject=f"SUbject:Quick message\n\n"
      body=f"""Hi {name},
      Just testing .....

      Best regards,
      Jafar
      """
      message= subject+body

      server.sendmail(my_email,email,message)
      print(f"Successfully sent to {name}")
    
    except Exception as e:
     print(f"Failed to send to {line} beacause of {e}") 


server.quit