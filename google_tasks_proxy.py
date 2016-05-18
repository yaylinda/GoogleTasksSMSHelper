import google_tasks_helper as gth

from twilio.rest import TwilioRestClient

client = TwilioRestClient("AC0c7758225ce3034d632bb220f32ff726", "38e17469cbb07fe090410949be98e1aa")

# message = client.messages.create(to="7133675720", from_="+18327914274", body="Hello there!")

for message in client.messages.list(to="+18327914274"):
    print message.body