#This file includes helper methods for the APIs
from django.shortcuts import render
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
from django.utils.html import strip_tags
from django.template import loader
from django.conf import settings
import requests
import traceback, sys, json

def create_formatted_email_msg(from_address, subject, body, attachments):
    m = MIMEMultipart() 

    #Email subject
    m['Subject'] = subject

    #Email from address
    m['From'] = from_address

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
            msg = MIMEAudio(attached_file.read(), _subtype=subtype)

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
    try:
        r = conn.send_raw_email(source=from_address, raw_message=content.as_string(), destinations=to_addresses)
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        return False

def send_email_mailgun(from_address, to_addresses, subject, body, attachments):
    #to_addresses = ",".join(str(addr) for addr in to_addresses)
    print to_addresses
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

def _send_email(request):
    try:
        data = json.loads(request.body)
    except ValueError, e:
        data = request.POST
    except:
        traceback.print_exc(file=sys.stdout)
        return False, "Invalid request body", HttpBadRequest

    try:
        from_address = data.get('from_address')
        to_addresses = data.get('to_addresses')
        if to_addresses:
            to_array = to_addresses.split(' ')
        else:
            return False, "Empty or invalid to_addresses", HttpForbidden

        subject = data.get('subject')
        body = data.get('body')
    except:
        traceback.print_exc(file=sys.stdout)

    if request.FILES.items():
        attachments = request.FILES.items()
    else:
        attachments = []

    try:
        print "Trying to send email via Amazon SES"
        if not from_address:
            from_email = settings.AWS_DEFAULT_FROM_EMAIL
        else:
            from_email = from_address
        content = create_formatted_email_msg(from_email, subject, body, attachments)
        email_sent = send_email_aws(from_email, to_array, content)
        if not email_sent:
            raise Exception()
    except:
        traceback.print_exc(file=sys.stdout)
        print "Failing over to Mailgun service"
        if not from_address:
            from_email = settings.MAILGUN_DEFAULT_FROM_EMAIL
        else:
            from_email = from_address
        try:
            #content = create_formatted_email_msg(from_email, subject, body, attachments)
            formatted_attachments = [('attachment', attached_file) for filename,attached_file in attachments]
            print formatted_attachments
            email_sent = send_email_mailgun(from_email, to_array, subject, body, formatted_attachments)
        except:
            traceback.print_exc(file=sys.stdout)
            raise Exception("Both email services failed")
    if email_sent:
        return True, "Email sent to recipients", HttpCreated
    else:
        return False, "Internal Error in sending email", HttpForbidden

