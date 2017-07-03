from twilio.rest import Client
from secrets import ACCOUNT_SID, AUTH_TOKEN

def sendText(pn_to, pn_from, msg):
	client = Client(ACCOUNT_SID, AUTH_TOKEN)
	try:
		client.messages.create(
		    to=pn_to,
		    from_=pn_from,
		    body=msg)
	except Exception as e:
		return e

	return True

