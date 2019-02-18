import json
import requests

URI = "http://localhost:3000"
HEADERS = {'Content-type': 'application/json'}


def get_time(is_success, timer):
    if is_success:
        time = timer
    else:
        try:
            res = requests.get(URI + "/timer")
            res = json.loads(res.text)
            time = res["timer"] - res["remain"]
        except KeyError:
            time = timer
    return time


def get_is_success():
    res = requests.get(URI + "/status")
    is_success = json.loads(res.text)["isSuccess"]
    return is_success


def get_orderbook():
    res = requests.get(URI + "/orderBook")
    orderbook = json.loads(res.text)["orderBook"]
    return orderbook


def get_is_alive():
    res = requests.get(URI + "/status")
    is_alive = json.loads(res.text)["isAlive"]
    return is_alive


def get_stack():
    res = requests.get(URI + "/stack")
    stack = json.loads(res.text)["stack"]
    return stack
