import os
from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
api_key = os.environ["TWILIO_API_KEY"]
api_secret = os.environ["TWILIO_API_SECRET"]

# Read call settings from the environment (.env) instead of hard-coding them.
VOICE_URL = f"https://{os.environ['NGROK_DOMAIN']}/voice"
TO_NUMBER = os.environ["TO_NUMBER"]
FROM_NUMBER = os.environ["FROM_NUMBER"]

client = Client(api_key, api_secret, account_sid)

call = client.calls.create(
    url=VOICE_URL,
    method="POST",
    to=TO_NUMBER,
    from_=FROM_NUMBER,
)

print("Call SID:", call.sid)
