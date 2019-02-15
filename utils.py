import json
import requests


def get_time(uri):
    # TODO: 고치기
    try:
        res = requests.get(uri + "/timer")
        res = json.loads(res.text)
        time = res["timer"] - res["remain"]
        return time
    except json.decoder.JSONDecodeError as e:
        print(res)
        print(res.text)
        raise e
