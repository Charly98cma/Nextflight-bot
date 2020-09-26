# Date and time management package
from time_management import request_time_of

# Dict of error messages
errDict = {
    "net" : "<i>Unknown date and time </i>",
    "window_start" : "<i>Unknown window open date and time </i>",
    "window_end" : "<i>Unknown window close date and time </i>",
    "desc" : "<i>Unknown description</i>",
    "orbit" : "<i>Unknown orbit</i>",
    "type" : "<i>Unknown mission type</i>",
    "location" : "<i>Unknown location</i>",
    "pad" : "<i>Unknown launch pad</i>"
}


def getValue(results, field):
    try:
        return results[field]
    except:
        errDict[field]

def getValueTimes(results, field, userTZ):
    try:
        return request_time_of(results[field], userTZ)
    except:
        return errDict[field]
