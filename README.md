email_service
=============

A REST based email service

This service accepts the necessary information (From, to, subject, body, attachment) and sends emails. The service provides an abstraction between two different email service providers, AWS SES and Sendgrid. It tries to send email via AWS SES first and if it fails, the service switches over to Sendgrid to fulfill the request.


