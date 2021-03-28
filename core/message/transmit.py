# This file will be used to set-up text messenging capabilities so I know if a
# job succeeds or fails. It mostly uses the same code as what's in Nuclear Octopus.

# This will be the final stage that takes the model.py data and turns it into
# a user friendly message based on the result. It then sends a text message to the
# user through an SMS gateway. This is a simple solution that only applies to one
# user. Long-term, an app that can do push notifications right after a survey is
# completed would be the ideal way to communicate.s

# Load Libraries
from datetime import datetime
import os  #This will be used for sending the text message
import smtplib #This will allow us to use the SMS gateway
from email.mime.multipart import MIMEMultipart #Needed for sending text from an email
from email.mime.text import MIMEText #Needed for sending the text from an email
import rollbar

# Craft a message to the user based on the results and accuracy
def communicado(table_group, success=False):

  #Craft the body message based on the above variables
    if success: #Is the job successful?
        timestamp = datetime.utcnow().replace(microsecond=0)
        results = f"\nSUCCESS: {timestamp} Data loaded into the {table_group} table(s).\n"
        print(results) #want successes printed to the console
    else: # Only want to send a message if the the load failed
        timestamp = datetime.utcnow().replace(microsecond=0)
        results = f"\nERROR: {timestamp} Data failed to load into the {table_group} table(s).\n"
        #Text recipient variables if the job failed
        phone = os.getenv('user_phone')
        sms_gateway = os.getenv('user_gateway')
        recipient_address = '+1' + phone + sms_gateway
        # Credentials for the entity sending the text. Currently stored as local variables
        # since this is not a public facing app yet, but will want to change this
        # before it is public.
        try:
            sender_email = os.getenv('messenger')
            sender_pass = os.getenv('messenger_password') # Need to remove this and replace with more secure option
            smtp = 'smtp.gmail.com'
            port = 587
            server = smtplib.SMTP(smtp, port)
        except Exception: #Not sure of the specific exceptions here
            rollbar.report_exc_info()
        with server as server:
            print("Opening connection to server")
            # Start the email server and login
            try:
                server.connect(smtp, port)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(sender_email, sender_pass)
            except Exception:
                rollbar.report_exc_info()
            # Structure the message using MIME
            else: 
                try:
                    message = MIMEMultipart()
                    message['From'] = sender_email
                    message['To'] = recipient_address
                    message['Subject'] = 'API Status\n' # Need to figure out how to strip the forward and back slashes
                    body = results
                    message.attach(MIMEText(body, 'plain'))
                except Exception:
                    rollbar.report_exc_info()
            # Send the text message
                else:
                    try:
                        text_message = message.as_string()
                        server.sendmail(sender_email, recipient_address, text_message)
                    except Exception:
                        rollbar.report_exc_info()

