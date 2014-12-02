# ----------------------------------------------------------------------------------------------------------
# This file contains Tastypie resources, 
# which are generally intermediaries between the end user & objects, usually Django models, or views.
# 
# Here, we define our REST APIs to different services. Each service is represented by a Resource class, and contains
# endpoints to sub-services within that service. 

# Author: Pavitra Bhalla
# ----------------------------------------------------------------------------------------------------------

#--------------------------------------------
# Import all necessary modules
#--------------------------------------------
from django.conf import settings
from django.conf.urls import url
from tastypie.resources import ModelResource, ALL
from api.views import _send_email 
from tastypie.http import *


#------------------------------------------------------------
#This Resource provides REST based APIs for an Email Service
#------------------------------------------------------------
class EmailResource(ModelResource):
    
    # Here we define the name of the API as it will be appended to the URL
    class Meta:
        resource_name = 'email-service'

    # Adding custom endpoints to this API
    def prepend_urls(self):
        return [url(r"^(?P<resource_name>%s)/send-email/$" % self._meta.resource_name, self.wrap_view('send_email'), name="send_email"),
                ]

    # This method accepts an HTTP POST request with parameters to send an email, 
    # and returns an HTTP response with status code 200, if the email was sent.
    def send_email(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        try:
            #Try sending an email
            success, message, http_status_code = _send_email(request)
        except:
            #Handle any unhandled exceptions in code and return a user-friendly message
            success, message, http_status_code = False, "Internal server error. Please try again later", HttpForbidden
        return self.create_response(request, {"success":success, "message":message}, http_status_code)
