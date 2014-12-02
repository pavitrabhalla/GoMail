GoMail
=============

<h3>A reliable REST API based email service backend to send emails</h3>

<h4>Why do you want this</h4>
Email is the most common way businesses interact with their customers to keep them engaged, interested and informed. Today, businesses are highly relied upon email service providers for doing the job right, but still there are events of failure that can lead to a huge loss in customer retention, money and efforts.

<h4>What does this do</h4>
GoMail provides an abstraction between two different service providers, making sure that if one fails, the service can failover to the other. This decreases the chances of failure in sending emails significantly. 

<h4>Take a test drive</h4>

Fill in the variables below - <br>
youremailaddress - Replace with an email address for which you can check inbox <br>
pathtofile - To test sending an attachment, provide the full path to a local file

<pre><code>curl -X POST /
      -H "Content-Type: multipart/form-data" /
      -F "from_address=testEmail@testem.ail" /
      -F "to_addresses=<b>&lt;youremailaddress&gt;</b>" /
      -F "subject=Testing my email service" /
      -F "body=Hi, this is a sample email from my email service" /
      -F "attachment=@&lt;pathtofile&gt;" /
    "http://ec2-54-67-40-84.us-west-1.compute.amazonaws.com:8080/api/v1/email-service/send-email/"
      </code></pre>

<h4>How does it work</h4>
GoMail uses Amazon Web Services-Simple Email Service (AWS SES) and SendGrid as the two email service providers. These services are highly reliable, provide extensive developer support and are easy to integrate with Python. GoMail chooses AWS SES as the default service to send email, but if it fails or SES goes down, it switches to Sendgrid to fulfill the request.

<h4>Under the hood</h4>
The service is built using Python and Django. This is mainly because I have been working with this stack at my current job for about a year now. Tastypie is used as the webservice API framework with django. It provides a convenient, yet powerful and highly customizable, abstraction for creating REST-style interfaces. 

<h4>What more can be done</h4>
<h5>Functional</h5>
1. Handling CC and BCC recipients
2. Adding authentication, authorization for API usage
2. API to add a default signature for a "to" address
3. API to get mail delivery status
4. Adding recipient group for a "from" address to send mass emails frequently
5. Upload a csv for list of recipients

<h5>Architectural</h5>
1. Add verbose logging
2. Add users model, that implements authentication, control and access rights
2. Storing events in database, along with the status of delivery
3. Adding detailed error codes and publishing it to the API documentation

<h4>Build your project</h4>
1. Download the source code from github, and go into the root directory of the project
2. On unix systems, run - <code>pip install -r requirements/requirements.txt</code>. This will install all the required packages for the project.
3. Setup your accounts on Mailgun and AWS
4. Modify the following variables in settings.py with your credentials -
<pre><code>&#32;&#32;&#32;&#32;&#35;Default Email Settings
DEFAULT&#95;FROM&#95;EMAIL = &#39;&lt;default&#95;from&#95;email&gt;&#39;
&#32;&#32;&#32;&#32;&#35;Sendgrid Credentials
SG&#95;USERNAME = &#39;&lt;sendgrid&#95;username&gt;&#39;
SG&#95;PASSWORD = &#39;&lt;sendgrid&#95;password&gt;&#39;
&#32;&#32;&#32;&#32;&#35;AWS Credentials
AWS&#95;ACCESS&#95;KEY&#95;ID = &#39;&lt;AWS&#95;ACCESS&#95;KEY&#95;ID&gt;&#39;
AWS&#95;SECRET&#95;ACCESS&#95;KEY = &#39;&lt;AWS&#95;SECRET&#95;KEY&gt;&#39;
AWS&#95;SES&#95;REGION = &#39;&lt;AWS&#95;SES&#95;REGION&gt;&#39;
&#32;&#32;&#32;&#32;&#35;API Base URL
API&#95;BASE&#95;URL = &lt;Base url to where you want to host your application&gt;</code></pre>

<h4>Me</h4>
You can find my Resume here - <a>http://bit.ly/1ET4En3</a>












