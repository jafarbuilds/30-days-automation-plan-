import smtplib

email= input("SENDER EMAIL:")
reciever_email=input("RECIEVER EMAIL:")

subject=input("SUBJECT:")
message=input("MESSAGE:")

text = f"subject: {subject}\n\n{message}"

server=smtplib.SMTP("smtp.gmail.com",587)
server.starttls()

server.login(email,"nuywruncgluajoly")
server.sendmail(email,reciever_email,text)

print("Email has been sent to "+ reciever_email)