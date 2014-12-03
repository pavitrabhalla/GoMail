GoMail
=============

<h3>A reliable REST API based email service backend to send emails</h3>

<h4>Why do you want this</h4>
Email is the most common way businesses interact with their customers to keep them engaged, interested and informed. Today, businesses are highly relied upon email service providers for doing the job right, but still there are events of failure that can lead to a huge loss in customer retention, money and efforts.

<h4>What does this do</h4>
GoMail provides an abstraction between two different service providers, making sure that if one fails, the service can failover to the other. This decreases the chances of failure in sending emails significantly. 

<h4>Take a test drive</h4>

<h5>Fill in the variables below -</h5>
youremailaddress - Replace with an email address for which you can check inbox
pathtofile - To test sending an attachment, provide the full path to a local file

<pre><code>curl -X POST /
      -H "Content-Type: multipart/form-data" /
      -F "from_address=testEmail@testem.ail" /
      -F "to_addresses=<b>&lt;youremailaddress&gt;</b>" /
      -F "subject=Testing my email service" /
      -F "body=Hi, this is a sample email from my email service" /
      -F "my_attachment=@&lt;pathtofile&gt;" /
    "http://ec2-54-67-40-84.us-west-1.compute.amazonaws.com:8080/api/v1/email-service/send-email/"
      </code></pre>

<h5>API</h5>
<b>&#47;api&#47;v1&#47;email&#45;service&#47;send&#45;mail&#47;</b>
<h6>Request Parameters:</h6>
1. <u>Content&#45;Type</u>: Use "application/json", if sending a JSON body without attachments. To send attachments, use "multipart/form-data"
2. <u>from&#95;address</u>(String): A single email adrress as string. This will be the "from" address displayed in the email. If this is not passed, a default address will be used to send the email. 
3. <u>to&#95;addresses</u>(String): Multiple recipient email addresses delimited by a space. This is a required field.
4. <u>subject</u>(String): Subject for the email. Defaults to empty.
5. <u>body</u>(String): Accepts plain/text or HTML formatted string. This will be the body of the email.
6. Attachments: For sending attachments, use the name of the file as the key and the path to the file as its value. You can send multiple attachments along with the email. Maximum size allowed for all attachments together is 7MB.

<h6>Response</h6>
<pre>Returns an HTTP response with appropriate HTTP response codes - 
Success codes: 200 HTTP CREATED
Failure codes: 400 BAD REQUEST (The request is malformed, or the server could not decode the body of the request)
               403 FORBIDDEN (The server understands the request, but cannot do any further processing)
               500 INTERNAL SERVER ERROR (An unexpected error occured internally)
               501 NOT IMPLEMENTED (Malformed url)
               405 METHOD NOT ALLOWED (Invalid HTTP method)</pre>
<h7>Response body (JSON):</h7>
<pre>      {"success": &lt;True/False for success and failure respectively&gt;
      "message": &lt;Response message from server&gt;}</pre>

<h4>How does it work</h4>
GoMail uses Amazon Web Services-Simple Email Service (AWS SES) and SendGrid as the two email service providers. These services are highly reliable, provide extensive developer support and are easy to integrate with Python. GoMail chooses AWS SES as the default service to send email, but if it fails or SES goes down, it switches to Sendgrid to fulfill the request.

<h4>Under the hood</h4>
The service is built using Python and Django. This is mainly because I have been working with this stack at my current job for about a year now. Tastypie is used as the webservice API framework with django. It provides a convenient, yet powerful and highly customizable, abstraction for creating REST-style interfaces. 

<h4>What more can be done</h4>
<h5>Functional</h5>
1. Handling CC and BCC recipients
2. Adding authentication, authorization for API usage
3. API to add a default signature for a "to" address
4. API to get mail delivery status
5. Adding recipient group for a "from" address to send mass emails frequently
6. Upload a csv for list of recipients

<h5>Internal, Design and Architecture</h5>
1. Add verbose logging
2. Preliminary checks on uploaded files for size and malware content.
3. Add users model, that implements authentication, control and access rights
4. Storing events in database, along with the status of delivery
5. Adding detailed error codes and publishing it to the API documentation

<h4>Build your project</h4>
1. Download the source code from github, and go into the root directory of the project
2. On unix systems, run - <code>pip install -r requirements/requirements.txt</code>. This will install all the required packages for the project.
3. Setup your accounts on Mailgun and AWS
4. Modify the following variables in settings.py with your credentials -
<pre><code>&#32;&#32;&#32;&#32;&#35;Default Email Settings
DEFAULT&#95;FROM&#95;EMAIL = &#39;&lt;default&#95;from&#95;email&gt;&#39;
DEFAULT&#95;TO&#95;EMAILS = &#39;&lt;default to email addresses delimited by a single blankspace&gt;&#39;
&#32;&#32;&#32;&#32;&#35;Sendgrid Credentials
SG&#95;USERNAME = &#39;&lt;sendgrid&#95;username&gt;&#39;
SG&#95;PASSWORD = &#39;&lt;sendgrid&#95;password&gt;&#39;
&#32;&#32;&#32;&#32;&#35;AWS Credentials
AWS&#95;ACCESS&#95;KEY&#95;ID = &#39;&lt;AWS&#95;ACCESS&#95;KEY&#95;ID&gt;&#39;
AWS&#95;SECRET&#95;ACCESS&#95;KEY = &#39;&lt;AWS&#95;SECRET&#95;KEY&gt;&#39;
AWS&#95;SES&#95;REGION = &#39;&lt;AWS&#95;SES&#95;REGION&gt;&#39;
&#32;&#32;&#32;&#32;&#35;API Base URL
API&#95;BASE&#95;URL = &lt;Base url to where your application is hosted&gt;</code></pre>

<h4>Run the test suite</h4>
Once you have setup your accounts, and changed the settings, run the test suite and check your inbox at the default "to" addresses. This is how you can run the tests -<pre>
<code> ./manage.py test api </code></pre>
<h4>Me</h4>
You can find my Resume here - <a>http://bit.ly/1ET4En3</a>












