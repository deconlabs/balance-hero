import time
from multiprocessing import Value, Process, Manager
import utils


class Master:
    def __init__(self, args):
        self.agents = dict()
        self.env = None

        self.quantity = args.quantity
        self.timer = args.timer

        self.infos = None

    def add_agent(self, agent):
        agent_id = len(self.agents)
        agent.set_id(agent_id)
        self.agents[agent_id] = agent

    def add_env(self, env):
        self.env = env

    def reset(self, path):
        utils.reset(path)
        utils.set_stack(self.quantity)
        utils.set_timer(self.timer)

        self.infos = dict()
        start_time = utils.get_start_time()
        assert start_time != -1
        self.infos["start_time"] = start_time

        for _, agent in self.agents.items():
            agent.update_eps()

    def start(self):
        cnt = Value('i', 0)
        is_alive = Value('i', 1)

        def f(is_alive):
            while True:
                if not utils.get_is_alive():
                    # print("서버가 죽었어요!")
                    is_alive.value = 0
                    break
                time.sleep(1)

        with Manager() as manager:
            s_a_dict = manager.dict()
            procs = []
            proc = Process(target=f, args=(is_alive, ))
            proc.start()
            procs.append(proc)
            for _, agent in self.agents.items():
                proc = Process(target=agent.start, args=(cnt, is_alive, s_a_dict, len(self.agents)))
                procs.append(proc)
                proc.start()

            for proc in procs:
                proc.join()
            self.infos["s_a_dict"] = s_a_dict.copy()
        return True

    def train(self):
        self.infos["is_success"] = utils.get_is_success()
        if self.infos["is_success"]:
            print("Deal: Success!")
        else:
            print("Deal: Failure!")
        self.infos["timer"] = self.timer

        s_a_dict = self.infos["s_a_dict"]
        states, actions = dict(), dict()
        for id_ in s_a_dict.keys():
            states[id_] = s_a_dict[id_]["state"]
            actions[id_] = s_a_dict[id_]["action"]

        orderbook = utils.get_orderbook()
        rewards, times = self.env.step(orderbook, self.infos)
        # print("states: ", states)
        # print("actions: ", actions)
        # print("rewards: ", rewards)
        # print("times: ", times)

        # 주문을 하지 않은 에이전트는 학습할 필요가 없음
        for id_ in states.keys():
            self.agents[id_].learn(states[id_], actions[id_], rewards[id_], times[id_])
