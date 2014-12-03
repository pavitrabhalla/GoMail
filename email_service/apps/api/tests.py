#-------------------------------------------------------------------------
# Tests for testing API's
#-------------------------------------------------------------------------

from django.test import TestCase
from tastypie.test import ResourceTestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import Client
import requests
import sys


# -------------------------------------------------------------------------
# Test class for SendEmail API
# -------------------------------------------------------------------------
class SendEmailTest(ResourceTestCase):
    
    # Setup data before running tests
    def setUp(self):
        super(SendEmailTest, self).setUp()
        
        # Email address that is verified to send emails via AWS
        self.aws_verified_from_address = settings.DEFAULT_FROM_EMAIL

        # Random email address to use as 'From' address
        self.default_from_address = 'randomSender@pbmail.service'
        
        # Email To addresses
        self.to_addresses = settings.DEFAULT_TO_EMAILS

        # Email Subject
        self.subject = 'Testing email sending service'

        # Plain text body without any HTML tags
        self.textbody = 'Hi, this is a plaintext message.'
        
        # HTML formatted body
        self.htmlbody = 'Hi, <br> This is a <b> HTML </b> formatted text.'
        
        # Body to send with emails having attachments
        self.attachment_body = 'Hi, <br> This is a <b> HTML </b> formatted text. Please find attached files.'

        # Test files that can be used as atatchments
            # Microsoft Office Word document file
        self.docFile = open(settings.TESTDATA_DIR+'dummy_doc.docx', 'rb')
            # PDF formatted file
        self.pdfFile = open(settings.TESTDATA_DIR+'dummy_pdf.pdf', 'rb')
            # JPEG Image file 
        self.imgFile = open(settings.TESTDATA_DIR+'dummy_img.jpg', 'rb')
        
        # Dictionary with filenames as keys and files as values
        # This can be used to send requests to the API using Requests Python Module
        self.attachments = {'dummy_doc.docx':self.docFile, 
                'dummy_pdf.pdf':self.pdfFile, 
                'dummy_image.jpg':self.imgFile} 

        # Url to send-email endpoint
        self.send_email_api_url = settings.API_BASE_URL+"api/v1/email-service/send-email/"


    # -----------------------------------------------------------------------------------------------------------------
    # Test success with AWS and a plaintext body
    # "From" address is the address that is verified with AWS SES, thus the email should be sent successfully via SES, 
    # unless the service is down
    # The service should return a 200 HttpCreated response on success
    # -----------------------------------------------------------------------------------------------------------------
    def test_plaintext_success_aws(self):
        print "Testing sending plaintext message using AWS"
        post_data = {
                'from_address':self.aws_verified_from_address,
                'to_addresses':self.to_addresses,
                'subject':self.subject,
                'body':self.textbody,
                }
        self.assertHttpCreated(self.api_client.post('/api/v1/email-service/send-email/', format='json', data=post_data))


    # -----------------------------------------------------------------------------------------------------------------
    # Test success with AWS and HTML formatted string as body
    # "From" address is the address that is verified with AWS SES, thus the email should be sent successfully via SES, 
    # unless the service is down.
    # The service should return a 200 HttpCreated response on success
    # -----------------------------------------------------------------------------------------------------------------
    def test_html_success_aws(self):
        print "Testing sending HTML message using AWS"
        post_data = {
                'from_address':self.aws_verified_from_address,
                'to_addresses':self.to_addresses,
                'subject':self.subject,
                'body':self.htmlbody,
                }
        self.assertHttpCreated(self.api_client.post('/api/v1/email-service/send-email/', format='json', data=post_data))


    # -----------------------------------------------------------------------------------------------------------------
    # Test success with AWS and attachments in the mail. Body is HTML formatted.
    # "From" address is the address that is verified with AWS SES, thus the email should be sent successfully via SES, 
    # unless the service is down.
    # The service should return a 200 HttpCreated response on success
    # -----------------------------------------------------------------------------------------------------------------
    def test_attachments_success_aws(self):
        print "Testing sending attachments with HTML message using AWS"
        r = requests.post(self.send_email_api_url,
            data={"from_address": self.aws_verified_from_address,
                    "to_addresses": self.to_addresses,
                    "subject":self.subject,
                    "body":self.attachment_body,
                    "h: Content-Type":"multipart/form-data",
                    },
            files=self.attachments,
            )
        print r.text
        self.assertHttpCreated(r)


    # -----------------------------------------------------------------------------------------------------------------
    # Test failover to sendgrid with a plaintext body
    # 
    # "From" address is an address NOT verified with AWS SES and it is required by AWS to verify your address
    # if you want to use it as the "From" address. 
    # Thus AWS will raise an exception and the service will failover to Sendgrid
    # 
    # Still, our email service will failover to Sendgrid 
    # Sendgrid should be able to send the email successfully through the given "From" alias address
    # The service should return a 200 HttpCreated response on success
    # -----------------------------------------------------------------------------------------------------------------
    def test_plaintext_failover_to_sendgrid(self):
        print "Testing sending plaintext message using Sendgrid after AWS throws exception"
        post_data = {
                'from_address':self.default_from_address,
                'to_addresses':self.to_addresses,
                'subject':self.subject,
                'body':self.textbody,
                }
        self.assertHttpCreated(self.api_client.post('/api/v1/email-service/send-email/', format='json', data=post_data))


    # -----------------------------------------------------------------------------------------------------------------
    # Test failover to sendgrid with an HTML body
    # 
    # "From" address is an address NOT verified with AWS SES and it is required by AWS to verify your address
    # if you want to use it as the "From" address. 
    # Thus AWS will raise an exception and the service will failover to Sendgrid
    # 
    # Still, our email service will failover to Sendgrid 
    # Sendgrid should be able to send the email successfully through the given "From" alias address
    # The service should return a 200 HttpCreated response on success
    # -----------------------------------------------------------------------------------------------------------------
    def test_html_failover_to_sendgrid(self):
        print "Testing sending HTML message using Sendgrid after AWS throws exception"
        post_data = {
                'from_address':self.default_from_address,
                'to_addresses':self.to_addresses,
                'subject':self.subject,
                'body':self.htmlbody,
                }
        self.assertHttpCreated(self.api_client.post('/api/v1/email-service/send-email/', format='json', data=post_data))


    # -----------------------------------------------------------------------------------------------------------------
    # Test failover to sendgrid with an HTML body and attachments
    # 
    # "From" address is an address NOT verified with AWS SES and it is required by AWS to verify your address
    # if you want to use it as the "From" address. 
    # Thus AWS will raise an exception and the service will failover to Sendgrid
    # 
    # Still, our email service will failover to Sendgrid 
    # Sendgrid should be able to send the email successfully through the given "From" alias address
    # The service should return a 200 HttpCreated response on success
    # -----------------------------------------------------------------------------------------------------------------
    def test_attachments_failover_to_sendgrid(self):
        print "Testing sending attachments with message using Sendgrid after AWS throws exception"
        r = requests.post(self.send_email_api_url,
            data={"from_address": self.default_from_address,
                    "to_addresses": self.to_addresses,
                    "subject":self.subject,
                    "body":self.attachment_body,
                    "h: Content-Type":"multipart/form-data",
                    },
            files=self.attachments,
            )
        print r.text
        self.assertHttpCreated(r)


    # -----------------------------------------------------------------------------------------------------------------
    # Test sending empty field in to_addresses
    # The service should return a 403 HttpForbidden response with message as "Empty or invalid to_addresses"
    # -----------------------------------------------------------------------------------------------------------------
    def test_empty_to_addresses(self):
        print "Testing empty to_addresses - 403 Forbidden"
        post_data = {
                'from_address':self.aws_verified_from_address,
                'subject':self.subject,
                'body':self.textbody,
                }
        resp = self.api_client.post('/api/v1/email-service/send-email/', format='json', data=post_data)
        self.assertEqual(self.deserialize(resp)['message'], "Empty or invalid to_addresses")
        self.assertHttpForbidden(resp)


    # -----------------------------------------------------------------------------------------------------------------
    # Test sending empty field in from_address
    # The service should use the default from_address and send the email 
    # Should return 200 HttpCreated response
    # -----------------------------------------------------------------------------------------------------------------
    def test_empty_from_address(self):
        print "Testing empty from address"
        post_data = {
                'to_addresses':self.to_addresses,
                'subject':self.subject,
                'body':self.textbody,
                }
        self.assertHttpCreated(self.api_client.post('/api/v1/email-service/send-email/', format='json', data=post_data))


    # -----------------------------------------------------------------------------------------------------------------
    # Test sending empty field in subject
    # The service should send the email with an empty subject
    # Should return 200 HttpCreated response
    # -----------------------------------------------------------------------------------------------------------------
    def test_empty_subject(self):
        print "Testing empty subject"
        post_data = {'from_address':self.default_from_address,
                'to_addresses':self.to_addresses,
                'body':self.textbody,
                }
        self.assertHttpCreated(self.api_client.post('/api/v1/email-service/send-email/', format='json', data=post_data))


    # -----------------------------------------------------------------------------------------------------------------
    # Test sending empty body
    # The service should send the email with an empty body
    # Should return 200 HttpCreated response
    # -----------------------------------------------------------------------------------------------------------------
    def test_empty_subject(self):
        print "Testing empty subject"
        post_data = {'from_address':self.default_from_address,
                'to_addresses':self.to_addresses,
                'subject':self.subject,
                }
        self.assertHttpCreated(self.api_client.post('/api/v1/email-service/send-email/', format='json', data=post_data))


    # -----------------------------------------------------------------------------------------------------------------
    # Test an incorrect Http method
    # Send a GET instead of POST
    # Should return 405 Method not allowed response
    # -----------------------------------------------------------------------------------------------------------------
    def test_incorrect_http_method(self):
        print "Testing empty subject"
        post_data = {'from_address':self.default_from_address,
                'to_addresses':self.to_addresses,
                'body':self.textbody,
                }
        self.assertHttpMethodNotAllowed(self.api_client.get('/api/v1/email-service/send-email/', format='json', data=post_data))


    # -----------------------------------------------------------------------------------------------------------------
    # Test a malformed url.
    # Changed the endpoint to send-emai
    # Should return 501 Http Not Implemented Error response
    # -----------------------------------------------------------------------------------------------------------------
    def test_malformed_url(self):
        print "Testing malformed url"
        post_data = {'from_address':self.default_from_address,
                'to_addresses':self.to_addresses,
                'body':self.textbody,
                }
        self.assertHttpNotImplemented(self.api_client.post('/api/v1/email-service/send-emai/', format='json', data=post_data))


