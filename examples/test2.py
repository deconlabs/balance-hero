"""
Multiprocessing에서 Process의 시드가 전부 동일하게 설정되는 문제가 있어 시드를 일일이 지정해줘야 하는 예제
"""


from multiprocessing import Process
import numpy as np


class Test:
    def __init__(self, id):
        self.id = id
        self.arr = np.arange(10)
        self.p = np.array([0.1] * 10)

    def sample(self):
        # 시드 넣어줘야 함
        np.random.seed(None)
        print(self.id, np.random.choice(self.arr, 1, p=self.p))


tests = [Test(i) for i in range(10)]

procs = []
for id_ in range(10):
    proc = Process(target=tests[id_].sample)
    procs.append(proc)
    proc.start()

for proc in procs:
    proc.join()
