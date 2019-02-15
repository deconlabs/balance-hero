import json
import requests


def get_time(uri, is_success, timer):
    if is_success:
        time = timer
    else:
        try:
            res = requests.get(uri + "/timer")
            res = json.loads(res.text)
            time = res["timer"] - res["remain"]
        except KeyError:
            time = timer
    return time
