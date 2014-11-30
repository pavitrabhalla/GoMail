import sys, traceback, json
from django.conf import settings
from django.conf.urls import url
from tastypie.resources import ModelResource, ALL
from tastypie.http import *
from api.views import create_formatted_email_msg, send_email_aws

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
            traceback.print_exc(file=sys.stdout)
            return self.create_response(request, {"success":False, "message":"Invalid request body"}, HttpBadRequest)

        try:
            from_address = data.get('from_address')
            if not from_address:
                return self.create_response(request, {"success":False, "message":"Empty or invalid from_address"}, HttpForbidden)

            to_addresses = data.get('to_addresses')
            if to_addresses:
                to_array = to_addresses.split(' ')
            else:
                return self.create_response(request, {"success":False, "message":"Empty or invalid to_addresses"}, HttpForbidden)

            subject = data.get('subject')
            body = data.get('body')
        except:
            traceback.print_exc(file=sys.stdout)

        if request.FILES.items():
            attachments = request.FILES.items()
        else:
            attachments = []

        content = create_formatted_email_msg(subject, body, attachments)

        try:
            email_sent = send_email_aws(from_address, to_array, content)
            if email_sent:
                return self.create_response(request, {"success":True, "message":"Email sent to recipients"}, HttpAccepted)
            else:
                return self.create_response(request, {"success":False, "message":"Internal Error in sending email"}, HttpForbidden)
        except:
            traceback.print_exc(file=sys.stdout)
            return self.create_response(request, {"success":False, "message":"Internal Error in sending email"}, HttpForbidden)

