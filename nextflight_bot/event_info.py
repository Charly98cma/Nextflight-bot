# Package to make HTTP requests (Launch Library 2 API)
import requests
# Value management
from value_management import *

URL = "https://ll.thespacedevs.com/2.0.0/event/upcoming/"

def event_Command(userTZ):

    parameters = {
        "limit" : 1
    }
    results = requests.get(
        URL,
        parameters
    ).json()["results"][0]

    # Name of the event
    name = results["name"]
    # Date of the event on the user TZ
    date = getValueTimes(results, "date")
    # Description of the event
    description = getValue(results, "description")
    # Location of the event (building, space center, etc...)
    location = getValue(results, "location")
    # URL of the article describing the event
    newsURL = getValue(results, "news_irl")

    net_msg = "<b>" + name + "</b>\n\n" +\
        "Date: " + date + "\n\n" +\
        description + "\n\n" +\
        location + "\n" +\
        "<a href=" + newsURL + ">" + "Press release</a>"

    # URL in which the event will be hosted
    try:
        next_msg += getValue(results, "video_url")
    except:
        pass

    return next_msg
