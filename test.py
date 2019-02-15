"""
Multiprocessing 사용 예제
모든 프로세스가 생성될때까지 작업 시작하지 않도록 공유하는 cnt 변수 넘겨줘서 대기하도록 하는 예제
"""

from multiprocessing import Process, Value
import requests
import json
import time

headers = {'Content-type': 'application/json'}


class Test:
    def f(self, cnt, id_):
        with cnt.get_lock():
            cnt.value += 1

        while(True):
            print(id_, cnt.value)
            if cnt.value == 1000:
                break

        for i in range(100):
            data = json.dumps(
                {
                    "id": id_,
                    "amount": 1
                }
            )
            requests.post("http://localhost:3000/purchase", headers=headers, data=data)
            time.sleep(0.5 + id_ * 0.001)


test = Test()

requests.post("http://localhost:3000/setStack", headers=headers, data=json.dumps({"stack": 100000000}))
requests.post("http://localhost:3000/setTimer", headers=headers, data=json.dumps({"timer": 100000000}))

cnt = Value('i', 0)
procs = []
for id_ in range(1000):
    proc = Process(target=test.f, args=(cnt, id_,))
    procs.append(proc)
    proc.start()

for proc in procs:
    proc.join()

print("DONE!")
