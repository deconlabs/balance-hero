import json
import time
import requests
from multiprocessing import Value, Process


class Master:
    def __init__(self, args):
        self.agents = dict()
        self.env = None
        self.uri = "http://localhost:3000"
        self.headers = {'Content-type': 'application/json'}

        self.quantity = args.quantity
        self.timer = args.timer

    def add_agent(self, agent):
        agent_id = len(self.agents)
        agent.set_id(agent_id)
        self.agents[agent_id] = agent

    def add_env(self, env):
        self.env = env

    def get_orderbook(self):
        res = requests.get(self.uri + "/orderBook")
        orderbook = json.loads(res.text)["orderBook"]
        return orderbook

    def get_is_alive(self):
        res = requests.get(self.uri + "/status")
        is_alive = json.loads(res.text)["isAlive"]
        return is_alive

    def get_is_success(self):
        res = requests.get(self.uri + "/status")
        is_success = json.loads(res.text)["isSuccess"]
        return is_success

    def reset(self):
        requests.post(self.uri + "/reset", headers=self.headers)
        requests.post(self.uri + "/setStack", headers=self.headers, data=json.dumps({"stack": self.quantity}))
        requests.post(self.uri + "/setTimer", headers=self.headers, data=json.dumps({"timer": self.timer}))

    def start(self):
        cnt = Value('i', 0)
        is_alive = Value('i', 1)

        def f(is_alive):
            while True:
                if not self.get_is_alive():
                    print("서버가 죽었어요!")
                    is_alive.value = 0
                    break
                time.sleep(1)

        procs = []
        proc = Process(target=f, args=(is_alive, ))
        proc.start()
        procs.append(proc)
        for id_, agent in self.agents.items():
            proc = Process(target=agent.start, args=(cnt, is_alive, len(self.agents)))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        return True

    def train(self, is_success, time):
        orderbook = self.get_orderbook()
        # TODO: 오더북만 이용해서 끝난 시간 알 수 있게 하기
        # TODO: infos 딕셔너리 만들어서 is_success, time 같이 넘겨주기
        infos = {
            "is_success": is_success,
            "time": time / 1000.
        }
        states, actions, rewards = self.env.step(orderbook, infos)
        print("states: ", states)
        print("actions: ", actions)
        print("rewards: ", rewards)

        # 주문을 하지 않은 에이전트는 학습할 필요가 없음
        for id_ in states.keys():
            self.agents[id_].learn(states[id_], actions[id_], rewards[id_])
