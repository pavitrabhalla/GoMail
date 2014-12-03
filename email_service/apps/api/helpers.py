#This file includes helper methods for the project
import email
import mimetypes
from tastypie.http import *
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import boto 
import boto.exception 
from boto.ses.connection import SESConnection 
from django.conf import settings
import traceback, sys, json
import sendgrid


# ----------------------------------------------------------------------------------------------------------
# This method can be used to send an email using AWS SES and Boto. Uses the send_raw_email() method to send 
# the email. 
# It takes a from_address, a list of to addresses and MIME formatted content as parameters
# Returns True if the email is sent successfully
# ----------------------------------------------------------------------------------------------------------
def send_email_aws(from_address, to_addresses, content):
    
    # Make a connection to AWS SES region and store the SESConnection object in conn
    try:
        conn = boto.ses.connect_to_region(settings.AWS_SES_REGION, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    except:
        traceback.print_exc(file=sys.stdout)
    
    # Try to send the email with MIME multipart content using send_raw_email()
    try:
        r = conn.send_raw_email(source=from_address, raw_message=content.as_string(), destinations=to_addresses)
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        return False



# ----------------------------------------------------------------------------------------------------------
# This method can be used to send an email using Sendgrid. 
# Returns True if the email is sent successfully
# ----------------------------------------------------------------------------------------------------------
def send_email_sendgrid(from_address, to_addresses, subject, body, attachments):
    try:
        # CREATE THE SENDGRID MAIL OBJECT
        #========================================================#
        sg = sendgrid.SendGridClient(settings.SG_USERNAME, settings.SG_PASSWORD)
        message = sendgrid.Mail()

        # ENTER THE EMAIL INFORMATION
        #========================================================#
        message.set_from(from_address)
        message.set_subject(subject)
        message.set_html(body)
        message.add_to(to_addresses)
        for filename,attachment in attachments:
            print attachment.name, attachment.size
            message.add_attachment(attachment.name, attachment.temporary_file_path())

        # SEND THE MESSAGE
        #========================================================#
        status, msg = sg.send(message)
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        return False



# ----------------------------------------------------------------------------------------------------------
# This method can be used to create a MIMEMultipart email object with html data and file attachments.
#
# ----------------------------------------------------------------------------------------------------------
def create_formatted_mime(from_address, subject, body, attachments):
    m = MIMEMultipart() 
    m['Subject'] = subject
    m['From'] = from_address

    #Email text/html body
    part = MIMEText(body, 'html') 
    m.attach(part)

    #Attachments
    for filename,attached_file in attachments:
        #Guess the type of file from its extension
        ctype, encoding = mimetypes.guess_type(attached_file.name)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)

        if maintype == 'text':
            # Note: we should handle calculating the charset
            msg = MIMEText(attached_file.read(), _subtype=subtype)
        elif maintype == 'image': 
            msg = MIMEImage(attached_file.read(), _subtype=subtype)
        elif maintype == 'audio': 
            msg = MIMEAudio(attached_file.read(), _subtype=subtype)
        elif maintype == 'application':
            msg = MIMEApplication(attached_file.read(), _subtype=subtype)
        else: 
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(attached_file.read())
            # Encode the payload using Base64
            encoders.encode_base64(msg)
            # Set the filename parameter
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        m.attach(msg)
    return m
