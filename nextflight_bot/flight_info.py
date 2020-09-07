# Package to make HTTP requests (Launch Library 2 API)
import requests
# Date and time management package
from datetime import datetime
# Package to manage timezones
import pytz

# Basic URL of Launch Library API
URL = "https://ll.thespacedevs.com/2.0.0/launch/upcoming/"

def next_Command(userTZ):
    # API request to retrieve the next space flight
    parameters = {
        "limit" : 1,
        "offset" : 0,
        "mode" : "detailed"
    }
    # Loop to search the next launch because the API returns the most recent launch even if it has already happend
    while True:
        # mode can be "normal", "list", "detailed"
        results = requests.get(
            URL,
            params=parameters
        ).json()["results"][0]

        if (results["status"]["name"] not in ["Success", "Failed"]):
            break
        parameters["offset"] += 1

    # Name of rocket and payload
    name = results["name"]

    # Estimated launch date and time
    # REVIEW: Check the TZ works properly
    try:
        net = pytz.utc.localize(datetime.strptime(results["net"], "%Y-%m-%dT%H:%M:%SZ")).astimezone(userTZ[1]).strftime("%Y/%m/%d - %H:%M:%S")
    except:
        net = "<i>Unknown launch date and time </i>"

    # Launch window start
    # REVIEW: Check the TZ works properly
    try:
        win_start = pytz.utc.localize(datetime.strptime(results["window_start"], "%Y-%m-%dT%H:%M:%SZ")).astimezone(userTZ[1]).strftime("%Y/%m/%d - %H:%M:%S")
    except:
        win_start = "<i>Unknown window open date and time </i>"

    # Launch window end
    # REVIEW: Check the TZ works properly
    try:
        win_end = pytz.utc.localize(datetime.strptime(results["window_end"], "%Y-%m-%dT%H:%M:%SZ")).astimezone(userTZ[1]).strftime("%Y/%m/%d - %H:%M:%S")
    except:
        win_end = "<i>Unknown window close date and time </i>"

    # Mission description
    try:
        mission_desc = results["mission"]["description"]
    except:
        mission_desc = "<i>Unknown description</i>"

    # Abbreviation of mission orbit
    try:
        mission_orbit = results["mission"]["orbit"]["abbrev"]
    except:
        mission_orbit = "<i>Unknown orbit</i>"

    # Mission type
    try:
        mission_type = results["mission"]["type"]
    except:
        mission_type = "<i>Unknown mission type</i>"

    # Launch location
    try:
        location = results["pad"]["location"]["name"]
    except:
        location = "<i>Unknown location</i>"

    # Launch pad
    try:
        pad = results["pad"]["name"]
    except:
        pad = "<i>Unknown launch pad</i>"

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
        next_msg += "\n" + results["vidURLs"][0]["url"]
    except:
        pass

    # Infographic, image or no image at all
    photo = None
    try:
        photo = results["infographic"]
    except:
        try:
            photo = results["image"]
        except:
            pass

    return next_msg, photo
