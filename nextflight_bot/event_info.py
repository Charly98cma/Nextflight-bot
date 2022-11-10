# Package to make HTTP requests (Launch Library 2 API)
import requests
# Value management
import value_management as vm

URL = "https://ll.thespacedevs.com/2.0.0/event/upcoming/"


def event_Command(userTZ):

    parameters = {"limit": 1}
    results = requests.get(
        URL,
        parameters
    ).json()["results"][0]

    next_msg = "<b>" + results["name"] + "</b>\n\n" +\
        "Date: " + vm.getValueTimes(results, "date", userTZ) + "\n\n" +\
        vm.getValue(results, "description") + "\n\n" +\
        vm.getValue(results, "location")

    # URL of the article describing the event
    try:
        next_msg += "\n<a href=\"" + vm.getValue(results, "news_url") + "\">Press release</a>"
    except:
        pass

    # URL in which the event will be hosted
    try:
        next_msg += "\n\n<a href=\"" + vm.getValue(results, "video_url") + "\">Youtube Stream</a>"
    except:
        pass

    return next_msg
