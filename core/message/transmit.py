# This file will be used to set-up text messenging capabilities so I know if a
# job succeeds or fails. It mostly uses the same code as what's in Nuclear Octopus.

# This will be the final stage that takes the model.py data and turns it into
# a user friendly message based on the result. It then sends a text message to the
# user through an SMS gateway. This is a simple solution that only applies to one
# user. Long-term, an app that can do push notifications right after a survey is
# completed would be the ideal way to communicate.s

# Load Libraries
from datetime import datetime
from os import getenv #This will be used for sending the text message
import smtplib #This will allow us to use the SMS gateway
from email.mime.multipart import MIMEMultipart #Needed for sending text from an email
from email.mime.text import MIMEText #Needed for sending the text from an email

# Craft a message to the user based on the results and accuracy
def communicado(success):

    #Craft the body message based on the above variables
    if success: #Is the job successful?
        timestamp = datetime.utcnow().replace(microsecond=0)
        results = f"\nSUCCESS: {timestamp} Data loaded.\n"
    else: # Handling for the false values
        timestamp = datetime.utcnow().replace(microsecond=0)
        results = f"\nERROR: {timestamp} Data failed to load.\n"

    #Text recipient variables
    phone = getenv('Phone')
    sms_gateway = getenv('Gateway')
    recipient_address = '+1' + phone + sms_gateway

    # Credentials for the entity sending the text. Currently stored as local variables
    # since this is not a public facing app yet, but will want to change this
    # before it is public.
    sender_email = getenv('messenger')
    sender_pass = getenv('password') # Need to remove this and replace with more secure option
    smtp = 'smtp.gmail.com'
    port = 587
    server = smtplib.SMTP(smtp, port)

    #Start the email server and login
    server.connect(smtp, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender_email, sender_pass)

    # Structure the message using MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_address
    message['Subject'] = 'API Status\n' # Need to figure out how to strip the forward and back slashes
    body = results
    message.attach(MIMEText(body, 'plain'))

    #Convert the message into text, send it, and close the server
    text_message = message.as_string()
    server.sendmail(sender_email, recipient_address, text_message)
    server.quit()


    


