import json
import requests
import numpy as np
from collections import deque
import time
import os
import shutil
from datetime import datetime


"""
에이전트의 신용등급 분포
대출거래고객의 신용등급 분포에 따라 랜덤 배정
2018년 12월 개인신용평가 관련 통계자료 기준
http://www.niceinfo.co.kr/creditrating/cb_score_3.nice
"""
CREDIT_DIST = np.array([0.2820866, 0.16822173, 0.1433743, 0.11848693, 0.10438483,
                        0.06542559, 0.03797563, 0.03051768, 0.03119231, 0.0183344])

"""
상위 5개 은행 대출 이자율의 평균
은행 순위: 2018년 9월 금감원 금융정보통계시스템 기준
http://fisis.fss.or.kr/fss/fsiview/indexw_ng.html

에이전트의 신용등급별에 따라 이자율이 다름
이자율 출처: 전국은행연합회
https://portal.kfb.or.kr/main/main.php
"""
RATES = [0.03734, 0.03734, 0.04508, 0.04508, 0.06042, 0.06042, 0.07946, 0.07946, 0.09475, 0.09475]


URI = "http://localhost:3000"
HEADERS = {'Content-type': 'application/json'}


class MovingAverage:
    def __init__(self, window):
        self.table = deque(maxlen=window)
        self._avg = 0.

    def update(self, item):
        self.table.append(item)
        self._avg = np.mean(self.table)

    @property
    def avg(self):
        return self._avg


def start(http_port, log_dir):
    global URI
    URI = "http://localhost:{}".format(http_port)

    os.chdir("./server")
    os.system("npm install --silent")
    os.system("HTTP_PORT={} npm start &".format(http_port))
    while True:
        try:
            res = requests.get(URI + "/isConnected")
            msg = json.loads(res.text)["msg"]
            if "connected" in msg.lower():
                break
        except Exception:
            time.sleep(1)
            pass
    os.chdir("../")


def close():
    requests.post(URI + "/stop", headers=HEADERS)


def reset(path):
    requests.post(URI + "/reset", headers=HEADERS, data=json.dumps({"path": path}))


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


def get_start_time():
    res = requests.get(URI + "/timer")
    res = json.loads(res.text)
    if "msg" in res:
        start_time = -1
    else:
        start_time = res["start"]
    return start_time


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


def get_interest_rate():
    credit = np.random.choice(np.arange(10), 1, p=CREDIT_DIST)[0]
    rate = RATES[credit]
    return rate


def set_stack(stack):
    requests.post(URI + "/setStack", headers=HEADERS, data=json.dumps({"stack": stack}))


def set_timer(timer):
    requests.post(URI + "/setTimer", headers=HEADERS, data=json.dumps({"timer": timer}))


def create_log_dir(argv):
    if not os.path.isdir('./logs/'):
        os.mkdir('./logs/')
    my_args = argv
    path_ = []
    if len(my_args) != 1:
        use_equality = ('=' in my_args[1])
    else:
        use_equality = False
        now = datetime.now().isoformat()
        path_.append(now)

    for idx in range(1, len(my_args)):
        if use_equality or idx % 2 == 1:
            path_.append(my_args[idx][2:])
        else:
            path_.append(my_args[idx])

    path = '_'.join(path_) + '/'
    # 기존에 같은 이름의 폴더가 있을 경우 삭제
    if os.path.isdir('./logs/' + path):
        shutil.rmtree('./logs/' + path)
    # 폴더 새로 생성
    os.mkdir('./logs/' + path)
    return path
