import logging
import requests
from twilio.twiml.messaging_response import MessagingResponse

logger = logging.getLogger(__name__)


"""HTTP Cloud Function.
    Parameters
    ----------
    request (flask.Request) : The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>

    Returns
    -------
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.

"""
def whatsapp_webhook(request):
  message = request.values.get('Body', "").lower()
  twilio_response = MessagingResponse()
  msg = twilio_response.message()
  if message in restaurants:
    resp = requests.get(restaurants[message])
    if not (200 <= resp.status_code <= 299):
        logger.error(
            f'Failed to retrieve data for the following restaurant - {message}. Here is a more verbose reason {resp.reason}'
        )
        msg.body(
            'Sorry we could not process your request. Please try again or check a different restaurant'
        )
    else:
        data = resp.json()[0]
        logger.info(data)
        msg.body(
          f"Found a match with {message}. Unfortunately service is still in progress so this is all you'll get now."
        )
  else:
    logger.error(
      f'Failed to retrieve data for the following restaurant - {message}. No match in Dictionary.'
    )
    msg.body(
      'Sorry we could not process your request. Please try again or check a different restaurant'
    )
  return str(twilio_response)

restaurants = {
  'piato': 'https://www.semma.fi/modules/json/json/Index?costNumber=1408&language=fi',
  'maija': 'https://www.semma.fi/modules/json/json/Index?costNumber=1402&language=fi',
  'lozzi':'https://www.semma.fi/modules/json/json/Index?costNumber=1401&language=fi',
  'belvedere':'https://www.semma.fi/modules/json/json/Index?costNumber=1404&language=fi',
  'syke':'https://www.semma.fi/modules/json/json/Index?costNumber=1405&language=fi',
  'tilia':'https://www.semma.fi/modules/json/json/Index?costNumber=1413&language=fi',
  'uno':'https://www.semma.fi/modules/json/json/Index?costNumber=1414&language=fi',
  'ylisto':'https://www.semma.fi/modules/json/json/Index?costNumber=1403&language=fi',
  'kvarkki':'https://www.semma.fi/modules/json/json/Index?costNumber=140301&language=fi',
  'rentukka':'https://www.semma.fi/modules/json/json/Index?costNumber=1416&language=fi',
  'novelli':'https://www.semma.fi/modules/json/json/Index?costNumber=1409&language=fi',
  'fiilu':'https://www.foodandco.fi/modules/json/json/Index?costNumber=3364&language=fi',
  'taide':'https://www.foodandco.fi/modules/json/json/Index?costNumber=0301&language=fi'
}