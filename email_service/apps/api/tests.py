from django.test import TestCase
from tastypie.test import ResourceTestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import Client
import requests
# Create your tests here.

class SendEmailTest(ResourceTestCase):
    def setUp(self):
        super(SendEmailTest, self).setUp()
        self.aws_verified_from_address = 'pavitrabhalla@gmail.com'
        self.default_from_address = 'randomSender@pbmail.service'
        self.to_addresses = 'pavitrabhalla@gmail.com pavitra@oceanleap.com'
        self.to_addresses_list = self.to_addresses
        self.subject = 'Testing email sending service'
        self.textbody = 'Hi, this is a plaintext message.'
        self.htmlbody = 'Hi, <br> This is a <b> HTML </b> formatted text.'
        self.docFile = open(settings.TESTDATA_DIR+'dummy_doc.docx', 'rb')
        self.pdfFile = open(settings.TESTDATA_DIR+'dummy_pdf.pdf', 'rb')
        self.imgFile = open(settings.TESTDATA_DIR+'dummy_img.jpg', 'rb')
        self.attachments = {'dummy_doc.docx':self.docFile, 
                'dummy_pdf.pdf':self.pdfFile, 
                'dummy_image.jpg':self.imgFile} 
        self.send_email_api_url = "http://ec2-54-67-40-84.us-west-1.compute.amazonaws.com:8080/api/v1/email-service/send-email/"

    def test_send_email_plaintext_success_aws(self):
        post_data = {
                'from_address':self.aws_verified_from_address,
                'to_addresses':self.to_addresses,
                'subject':self.subject,
                'body':self.textbody,
                }
        #self.assertHttpCreated(self.api_client.post('/api/v1/email-service/send-email/', format='json', data=post_data))

    def test_send_email_html_success_aws(self):
        post_data = {
                'from_address':self.aws_verified_from_address,
                'to_addresses':self.to_addresses,
                'subject':self.subject,
                'body':self.htmlbody,
                }
        #self.assertHttpCreated(self.api_client.post('/api/v1/email-service/send-email/', format='json', data=post_data))

    def test_send_email_attachments_success_aws(self):
        r = requests.post(self.send_email_api_url,
            data={"from_address": self.aws_verified_from_address,
                    "to_addresses": self.to_addresses,
                    "subject":self.subject,
                    "body":self.htmlbody,
                    "h: Content-Type":"multipart/form-data",
                    },
            files=self.attachments,
            )
        print r.text
        self.assertHttpCreated(r)
