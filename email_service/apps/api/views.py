#-------------------------------------------------------------------------------------------------------
# This file contains the logic methods that are usually used by API's to fullfill the requests
#-------------------------------------------------------------------------------------------------------

from django.shortcuts import render
from django.conf import settings
import traceback, sys, json
from api.helpers import create_formatted_mime, send_email_aws, send_email_sendgrid
from tastypie.http import *



#-------------------------------------------------------------------------------------------------------
# This method implements the logic to accept email parameters received in the request, 
# do a preliminary check for required parameters,
# call the helper methods that create a formatted email MIME,
# then send_email_aws to send email via AWS SES.

# If there is an exception, and SES fails, this method tries to send the email
# via Sendgrid
#-------------------------------------------------------------------------------------------------------

def _send_email(request):
    
    # Try to load data from request body
    try:
        data = json.loads(request.body)

    # If the body is empty, try to load data from POST params.
    # This is useful if the content-type of the request is multipart/form-data.
    except ValueError, e:
        data = request.POST
    
    

    # If no data could be decoded from the request, 
    # throw an exception telling it is a bad request. In this case, the API response will return a 400 HttpBadRequest error.
    except:
        traceback.print_exc(file=sys.stdout)
        return False, "Invalid request body", HttpBadRequest

    try:        
        # Try to a get a from_address from the request data. If a from_address is not provided, use the default from address 
        # from settings
        from_address = data.get('from_address')
        if not from_address:
            from_address = settings.DEFAULT_FROM_ADDRESS

        # Try to get to_addresses from the request 
        to_addresses = data.get('to_addresses')

        # Convert the string of to_addresses delimited by single blankspaces to a list
        if to_addresses:
            to_array = to_addresses.split(' ')

        # If there are no to_addresses return an error with response code as HttpForbidden
        # Indicate the server cannot process the request further without valid to_addresses
        else:
            return False, "Empty or invalid to_addresses", HttpForbidden


        # Get a subject for the email from the request
        subject = data.get('subject')


        # Get the body for the email from the request
        body = data.get('body')

    except:
        #print the stacktrace to standard output if there is an error
        traceback.print_exc(file=sys.stdout)



    # Load all files uploaded as part of the request to attachments list variable
    if request.FILES.items():
        attachments = request.FILES.items()

    #If there are no attchments, create an empty list for attachments
    else:
        attachments = []


    #Try to send an email via AWS SES. If it fails, try to send via Sendgrid. If that fails too, raise an exception
    try:
        print "Trying to send email via Amazon SES"
        
        # Create a MIMEMultipart object with the right data encodings and save it to content 
        content = create_formatted_mime(from_email, subject, body, attachments)
        
        #Send an email using AWS with the MIME content generated
        email_sent = send_email_aws(from_email, to_array, content)

        #Check if email_sent is False, and raise an exception.
        if not email_sent:
            raise Exception()
    
    except:
        traceback.print_exc(file=sys.stdout)
        print "Failing over to sendgrid"
        
        #Now try to send email via Mailgun
        try:
            email_sent = send_email_sendgrid(from_address, to_addresses, subject, body, attachments)
        
        #If there is an exception, raise an exception indicating the request has failed
        except:
            print traceback.print_exc(file=sys.stdout)
            raise Exception("Both email services failed")

    # If the email was sent successfully, return a success, else return a failure
    if email_sent:
        return True, "Email sent to recipients", HttpCreated
    else:
        return False, "Internal Error in sending email", HttpForbidden
