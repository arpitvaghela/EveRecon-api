import json
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_speaker_email(speaker, email, event, event_id, community):
    message = Mail(
        from_email='yashraj@techprobex.com',
        to_emails=email,
        html_content='<strong>and easy to do anywhere, even with Python</strong>'
        )
    message.dynamic_template_data = {
        "speaker" : speaker,
        "event" : event,
        "community": community,
        "url" : os.environ.get('HOST', "") + 'events/' + str(event_id)
    }
    message.template_id = 'd-5c4412e8a167433a929998864cdab9f4'
    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("Exception occured while sending an email")   
    
# send_speaker_email("Yashraj Kakkad", "yashrajkakkad@gmail.com", "ML 101", 1, "Dummy Community")