#-------------------------------------------------------------------------
# Tests for testing API's
#-------------------------------------------------------------------------

from django.test import TestCase
from tastypie.test import ResourceTestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import Client
import requests


# -------------------------------------------------------------------------
# Test class for SendEmail API
# -------------------------------------------------------------------------
class SendEmailTest(ResourceTestCase):
    
    # Setup data before running tests
    def setUp(self):
        super(SendEmailTest, self).setUp()

        # Email address that is verified to send emails via AWS
        self.aws_verified_from_address = settings.DEFAULT_FROM_ADDRESS

        # Random email address to use as 'From' address
        self.default_from_address = 'randomSender@pbmail.service'
        
        # Email To addresses
        self.to_addresses = 'pavitrabhalla@gmail.com pavitra@oceanleap.com'

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
    def test_html_failover_to_sendgrid(self):
        post_data = {
                'from_address':self.default_from_address,
                'to_addresses':self.to_addresses,
                'subject':self.subject,
                'body':self.htmlbody,
                'h: Content-Type':'multipart/form-data',
                    },
            files=self.attachments,
            )
        self.assertHttpCreated(self.api_client.post('/api/v1/email-service/send-email/', format='json', data=post_data))










