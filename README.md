GoMail
=============

<h3>A reliable REST API based email service to send emails</h3>

<h4>Why do you want this</h4>
Email is the most common way businesses interact with their customers to keep them engaged, interested and informed. Today, businesses are highly relied upon email service providers for doing the job right, but still there are events of failure that can lead to a huge loss in customer retention, money and efforts.

<h4>What does this do</h4>
GoMail provides an abstraction between two different service providers, making sure that if one fails, the service can failover to the other. This decreases the chances of failure in sending emails significantly. 

<h4>Take a test drive</h4>
<pre><code>curl -X POST /
      -H "Content-Type: multipart/form-data" /
      -F "from_address=testEmail@testem.ail" /
      -F "to_addresses=<b>&lt;Enter your email address&gt;</b>" /
      -F "subject=Testing my email service" /
      -F "body=Hi, this is a sample email from my email service" /
      -F "attachment=@pathtofile" /
    "http://ec2-54-67-40-84.us-west-1.compute.amazonaws.com:8080/api/v1/email-service/send-email/"
      </code></pre>

<h4>How does it work</h4>
GoMail uses Amazon Web Services-Simple Email Service (AWS SES) and SendGrid as the two email service providers. These services are highly reliable, provide extensive developer support and are easy to integrate with Python. GoMail chooses AWS SES as the default service to send email, but if it fails or SES goes down, it switches to Sendgrid to fulfill the request.












