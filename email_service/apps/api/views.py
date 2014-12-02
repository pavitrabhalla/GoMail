#This file includes helper methods for the APIs
from django.shortcuts import render
from django.conf import settings
import traceback, sys, json
from api.helpers import create_formatted_mime, send_email_aws, send_email_sendgrid

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
        print "From:" + from_address
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
        content = create_formatted_mime(from_email, subject, body, attachments)
        email_sent = send_email_aws(from_email, to_array, content)
        if not email_sent:
            raise Exception()
    except:
        traceback.print_exc(file=sys.stdout)
        print "Failing over to sendgrid"
        try:
            email_sent = send_email_sendgrid(from_address, to_addresses, subject, body, attachments)
        except:
            raise Exception("Both email services failed")
    if email_sent:
        return True, "Email sent to recipients", HttpCreated
    else:
        return False, "Internal Error in sending email", HttpForbidden
