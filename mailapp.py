from email.message import EmailMessage
import ssl
import smtplib
import tkinter as tk

root = tk.Tk()
root.geometry("800x400")

clearButtonsFrame = tk.Frame(root, bg='cyan')
clearButtonsFrame.pack(expand=True, fill='both')

clearButton = tk.Button(clearButtonsFrame, text="Button 1", width=40)
clearButton.place(relx=0.25, rely=0.5, anchor=tk.CENTER)

selectButton = tk.Button(clearButtonsFrame, text="Button 2", width=40)
selectButton.place(relx=0.75, rely=0.5, anchor=tk.CENTER)
selectButton = tk.Button(clearButtonsFrame, text="Button 2", width=40)
selectButton.place(relx=0.75, rely=0.6, anchor=tk.CENTER)

root.mainloop()

email_sender = 'wisamabady7@gmail.com'
email_password ='gtqmsspsjyotaipy'

email_receiver = 'kokajek645@wwgoc.com'

subject="Price just droped!!"
body="""
The price of the product you're tracking just droped!!
"""

em=EmailMessage()
em ['From']=email_sender
em ['To']=email_receiver
em ['subject']=subject
em.set_content(body)

context=ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())