import json
import time
import requests
from multiprocessing import Value, Process


class Master:
    def __init__(self):
        self.agents = dict()
        self.env = None
        self.uri = "http://localhost:3000"
        self.headers = {'Content-type': 'application/json'}

    def add_agent(self, agent):
        agent_id = len(self.agents)
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
        requests.post(self.uri + "/setStack", headers=self.headers, data=json.dumps({"stack": self.stack}))
        requests.post(self.uri + "/setTimer", headers=self.headers, data=json.dumps({"timer": self.timer}))

    def start(self):
        cnt = Value('i', 0)
        is_alive = Value('i', 1)

        def f(self, is_alive):
            while True:
                if not self.get_is_alive():
                    is_alive.value = 0
                time.sleep(1)

        procs = []
        proc = Process(target=f, args=(is_alive))
        proc.start()
        procs.append(proc)
        for id_, agent in self.agents.items():
            proc = Process(target=agent.start, args=(cnt, is_alive, len(self.agents)))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        return True

    def train(self, is_success):
        orderbook = self.get_orderbook()
        states, actions, rewards = self.env.step(orderbook, is_success)
        for id_, agent in self.agents.items():
            agent.learn(states[id_], actions[id_], rewards[id_])
