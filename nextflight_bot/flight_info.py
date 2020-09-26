# Package to make HTTP requests (Launch Library 2 API)
import requests
# Value management
from value_management import *

# Basic URL of Launch Library API
URL = "https://ll.thespacedevs.com/2.0.0/launch/upcoming/"


def next_Command(userTZ):
    # Loop to search the next launch because the API returns the most recent launch even if it has already happend
    results = getResult()
    # Name of rocket and payload
    name = results["name"]
    # Estimated launch date and time
    net = getValueTimes(results, "net", userTZ)
    # Launch window start
    win_start = getValueTimes(results, "window_start", userTZ)
    # Launch window end
    win_end = getValueTimes(results, "window_end", userTZ)
    # Mission description
    mission_desc = getValue(results["mission"], "description")
    # Abbreviation of mission orbit
    mission_orbit = getValue(results["mission"]["orbit"], "abbrev")
    # Mission type
    mission_type = getValue(results["mission"], "type")
    # Launch location
    location = getValue(results["pad"]["location"], "name")
    # Launch pad
    pad = getValue(results["pad"], "name")

    # Message for the user
    next_msg = "<b>" + name + "</b>\n\n" +\
        "NET: " + net + "\n" +\
        "Wind.Open: " + win_start + "\n" +\
        "Wind.Close: " + win_end + "\n\n" +\
        mission_desc + "\n\n" +\
        mission_orbit + " - " + mission_type + "\n" +\
        pad + " - " + location

    # URL of the streaming
    try:
        next_msg += "\n\n<a href=\"" + results["vidURLs"][0]["url"] + "\">Stream</a>"
    except:
        pass

    # Infographic, image or no image at all
    photo = results["infographic"]
    if photo is None:
        photo = results["image"]
    return next_msg, photo


# API request to retrieve the next space flight
def getResult():
    # Mode can be "normal", "list" or "detailed"
    parameters = {
        "limit" : 1,
        "offset" : 0,
        "mode" : "detailed",
    }
    while True:
        results = requests.get(
            URL,
            params=parameters
        ).json()["results"][0]
        if (results["status"]["name"] not in ["Success", "Failed"]):
            break
        parameters["offset"] += 1
    return results
