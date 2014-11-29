import sys, traceback, json
from django.conf import settings
from django.conf.urls import url
from tastypie.resources import ModelResource, ALL
from tastypie.http import *

class EmailResource(ModelResource):
    class Meta:
        resource_name = 'email-service'
        allowed_methods = []

    def prepend_urls(self):
        return [url(r"^(?P<resource_name>%s)/send-email/$" % self._meta.resource_name, self.wrap_view('send_email'), name="send_email"),
                ]

    def send_email(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
	
	try:
	    data = json.loads(request.body)
	except ValueError, e:
	    data = request.POST
	except:
	    traceback.print_exc(FILE = sys.stdout)
	    return self.create_response(request, {"success":False, "message":"Error: Invalid request body."}, HttpBadRequest)
			
	from_address = data.get('from_address')
	to_addresses = data.get('to_addresses')
	subject = data.get('subject')
	body = data.get('body')
	
	print "From Address: {}".format(from_address)
	print "To Addresses: {}".format(to_addresses)
	print "subject: {}".format(subject)
	print "body: {}".format(body)
	
	for k,v in request.FILES.items():
	    print k

	import email
	import boto 
	import boto.exception 
	from boto.ses.connection import SESConnection 
	from django.utils.html import strip_tags
	from django.template import loader
	
	m = email.mime.multipart.MIMEMultipart() 
	m['Subject'] = subject
	
	if from_address:  
	    m['From'] = from_address
	else:
	    m['From'] = settings.DEFAULT_FROM_EMAIL
	
	to_array = to_addresses.split(' ')

	#Message body 
	part = email.mime.text.MIMEText(body) 
	m.attach(part) 

	#Attachment 
	#part = email.mime.text.MIMEText('contents of test file here') 
	#part.add_header('Content-Disposition', 'attachment; filename=test.txt') 
	#m.attach(part) 

	try:
	    conn = boto.ses.connect_to_region(settings.AWS_SES_REGION, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
	except:
	    traceback.print_exc(file=sys.stdout)

	r = conn.send_raw_email(source=m['From'], raw_message=m.as_string(), 
	destinations=to_array)

        return self.create_response(request, {"status":"Reached here"}, HttpAccepted)










 
