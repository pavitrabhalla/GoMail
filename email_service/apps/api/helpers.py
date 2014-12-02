#This file includes helper methods for the APIs
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
import requests
import traceback, sys, json
import sendgrid

def create_formatted_mime(from_address, subject, body, attachments):
    m = MIMEMultipart() 

    #Email subject
    m['Subject'] = subject

    #Email from address
    m['From'] = from_address

    #Email text/html body
    part = MIMEText(body, 'html') 
    m.attach(part)

    #Attachments
    for filename,attached_file in attachments:
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


def send_email_aws(from_address, to_addresses, content):
    try:
        conn = boto.ses.connect_to_region(settings.AWS_SES_REGION, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    except:
        traceback.print_exc(file=sys.stdout)
    try:
        r = conn.send_raw_email(source=from_address, raw_message=content.as_string(), destinations=to_addresses)
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        return False

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
        print msg
    except:
        traceback.print_exc(file=sys.stdout)
        return False
    return True

def send_email_mailgun(from_address, to_addresses, subject, body, attachments):
    #to_addresses = ",".join(str(addr) for addr in to_addresses)
    print attachments
    try:
        return requests.post(settings.MAILGUN_SEND_URL,
            auth=("api", settings.MAILGUN_API_KEY),
            data={"from": from_address,
                    "to": to_addresses,
                    "subject":subject,
                    "html":body,
                    "h: Content-Type":"multipart/form-data",
                    },
            files=attachments
            )
    except:
        traceback.print_exc(file=sys.stdout)
        return False