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
        return self.create_response(request, {"status":"Reached here"}, HttpAccepted)
