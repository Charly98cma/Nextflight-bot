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
    date = getValueTimes(results, "date", userTZ)
    # Description of the event
    description = getValue(results, "description")
    # Location of the event (building, space center, etc...)
    location = getValue(results, "location")

    next_msg = "<b>" + name + "</b>\n\n" +\
        "Date: " + date + "\n\n" +\
        description + "\n\n" +\
        location

    # URL of the article describing the event
    try:
        next_msg += "\n<a href=\"" + getValue(results, "news_url") + "\">Press release</a>"
    except:
        pass

    # URL in which the event will be hosted
    try:
        next_msg += "\n\n<a href=\"" + getValue(results, "video_url") + "\">Youtube Stream</a>"
    except:
        pass

    return next_msg
