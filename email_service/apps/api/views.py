#This file includes helper methods for the APIs
from django.shortcuts import render
import email
import mimetypes
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
from django.utils.html import strip_tags
from django.template import loader
from django.conf import settings

def create_formatted_email_msg(subject, body, attachments):
    m = MIMEMultipart() 

    #Email subject
    m['Subject'] = subject

    #Email text/html body
    part = MIMEText(body, 'html') 
    m.attach(part)

    #Attachments
    for k,v in attachments:
        attached_file = v
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
            msg = MIMEAudio(attched_file.read(), _subtype=subtype)

        elif maintype == 'application':
            msg = MIMEApplication(attached_file.read(), _subtype=subtype)

        else: 
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(attached_file.read())
            # Encode the payload using Base64
            encoders.encode_base64(msg)
        # Set the filename parameter
        msg.add_header('Content-Disposition', 'attachment', filename=k)
        m.attach(msg)
    return m

def send_email_aws(from_address, to_addresses, content):
    try:
        conn = boto.ses.connect_to_region(settings.AWS_SES_REGION, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    except:
        traceback.print_exc(file=sys.stdout)

    r = conn.send_raw_email(source=from_address, raw_message=content.as_string(), destinations=to_addresses)
    return True

