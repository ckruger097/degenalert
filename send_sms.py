# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


def send(info):
    message = client.messages \
        .create(
        messaging_service_sid=os.environ['messaging_service_sid'],
        body=info,
        to=os.environ['my_cell']
    )
    print(message.sid)
