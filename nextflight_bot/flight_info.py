# Package to make HTTP requests (Launch Library 2 API)
import requests
# Value management
import value_management as vm

# Basic URL of Launch Library API
URL = "https://ll.thespacedevs.com/2.0.0/launch/upcoming/"


def next_Command(userTZ):
    results = getResult()

    next_msg = "<b>" + results["name"] + "</b>\n\n" +\
        "NET: " + vm.getValueTimes(results, "net", userTZ) + "\n" +\
        "Wind.Open: " + vm.getValueTimes(results, "window_start", userTZ) + "\n" +\
        "Wind.Close: " + vm.getValueTimes(results, "window_end", userTZ) + "\n\n" +\
        vm.getValue(results["mission"], "description") + "\n\n" +\
        vm.getValue(results["mission"]["orbit"], "abbrev") + " - " +\
        vm.getValue(results["mission"], "type") + "\n" +\
        vm.getValue(results["pad"], "name") + " - " +\
        vm.getValue(results["pad"]["location"], "name")

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
    parameters = {"limit": 1, "offset": 0, "mode": "detailed"}
    while True:
        results = requests.get(
            URL,
            params=parameters
        ).json()["results"][0]

        if (results["status"]["name"] not in ["Success", "Failed", "Partial Failure"]):
            break

        parameters["offset"] += 1
    return results
