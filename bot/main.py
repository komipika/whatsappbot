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
  message = request.values.get("Body", "").lower()
  twilio_response = MessagingResponse()
  msg = twilio_response.message()

  
  if message in restaurants.keys():
    resp = getTodaysMenu(message)
    msg.body(
      resp
    )
    return str(twilio_response)
  if message == "kasvismenu":
    resp = getVegMenus()
    msg.body(
      resp
    )
    return str(twilio_response)

  if message == "help":
    resp = getSomeHelp()
    msg.body(
      resp
    )
    return str(twilio_response)
  
  msg.body(
    "Sorry we could not process your request. Please try again or check a different restaurant. You can type \"help\" for available commands."
  )
    
  return str(twilio_response)


def getTodaysMenu(message):
  resp = requests.get(restaurants[message])
  if not (200 <= resp.status_code <= 299):
    logger.error(
        f"Failed to retrieve data for the following restaurant - {message}. Here is a more verbose reason {resp.reason}"
    )
    return "Sorry we could not process your request. Please try again or check a different restaurant. You can type \"help\" for available commands."
  else:
    name = resp.json()["RestaurantName"]
    if not resp.json()["MenusForDays"]:
      return f"{name} is not offering anything today."
    time = resp.json()["MenusForDays"][0]["LunchTime"]
    menus = resp.json()["MenusForDays"][0]["SetMenus"]
    ret = f"Todays lunch menu for {name}: \n "
    ret += (f"Lunchtime at {time}, \n")
    for food in menus:
      tempStr = ""
      for comp in food["Components"]:
        tempStr += f"{comp} "
      tempName = food["Name"]
      ret += (f"{tempName}: {tempStr}, \n")    
    ret = ret.strip()
    ret = ret[:-1]
    return ret

  
def getVegMenus():
  logger.info("getting vege menus")
  ret = "Todays vegetable options are: \n"
  for key in restaurants:
    ret += getVeg(restaurants[key])
  ret = ret.strip()
  ret = ret[:-1]
  return ret

def getVeg(url):
  resp = requests.get(url)
  if not (200 <= resp.status_code <= 299):
    logger.error(
        f"Failed to retrieve data for the restaurant. Here is a more verbose reason {resp.reason}"
    )
    return ""
  else:
    if not resp.json()["MenusForDays"]:
      return ""
    name = resp.json()["RestaurantName"]
    logger.info(name)
    menus = resp.json()["MenusForDays"][0]["SetMenus"]
    ret = f"{name}:"
    for food in menus:
      tempStr = ""
      tempName = food["Name"]
      if tempName not in vegAlias:
        continue #go next if not a veg option
      for comp in food["Components"]:
        tempStr += f"{comp} "
      ret += (f" {tempStr}, \n")   

    if ret == f"{name}:":
      return "" #return empty string if no vegan options

    return ret


def getSomeHelp():
  ret = "Type \"Kasvismenu\" for all vegan lunch options for semma restaurants today. \n"
  ret += "You can also type restaurants name to get its full lunch menu. \n"
  ret += "Available restaurants: \n"
  for key in restaurants:
    ret += f"{key}, \n"
  ret = ret.strip()
  ret = ret[:-1] #trim last "," off
  return ret

#Dict of semmas' json menus in finnish
restaurants = {
  "piato": "https://www.semma.fi/modules/json/json/Index?costNumber=1408&language=fi",
  "maija": "https://www.semma.fi/modules/json/json/Index?costNumber=1402&language=fi",
  "lozzi":"https://www.semma.fi/modules/json/json/Index?costNumber=1401&language=fi",
  "belvedere":"https://www.semma.fi/modules/json/json/Index?costNumber=1404&language=fi",
  "syke":"https://www.semma.fi/modules/json/json/Index?costNumber=1405&language=fi",
  "tilia":"https://www.semma.fi/modules/json/json/Index?costNumber=1413&language=fi",
  "uno":"https://www.semma.fi/modules/json/json/Index?costNumber=1414&language=fi",
  "ylisto":"https://www.semma.fi/modules/json/json/Index?costNumber=1403&language=fi",
  "kvarkki":"https://www.semma.fi/modules/json/json/Index?costNumber=140301&language=fi",
  "rentukka":"https://www.semma.fi/modules/json/json/Index?costNumber=1416&language=fi",
  "novelli":"https://www.semma.fi/modules/json/json/Index?costNumber=1409&language=fi",
  "fiilu":"https://www.foodandco.fi/modules/json/json/Index?costNumber=3364&language=fi",
  "taide":"https://www.foodandco.fi/modules/json/json/Index?costNumber=0301&language=fi"
}

#different ways veg option are spelt in JSON
vegAlias = (
  "KASVISLOUNAS",
  "Kasvislounas",
  "kasvislounas",
  "KASVISKEITTO",
  "Kasviskeitto",
  "kasviskeitto",
  "Kasviskietto"
)