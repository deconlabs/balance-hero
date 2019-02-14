import os
from env import Env
from agent import Agent
from master import Master


def run():
    try:
        os.chdir("./server")
        os.system("npm install --silent")
        os.system("npm start &")
    finally:
        os.chdir("../")

    env = Env()
    agents = [Agent() for _ in range(args.n_agents)]
    master = Master()

    for agent in agents:
        master.add_agent(agent)
    master.add_env(env)

    for idx in range(args.n_episode):
        # 서버의 stack, timer 초기화
        master.reset()
        # 에피소드 시작
        master.start()
        # 에이전트 학습
        is_success = master.get_is_success()
        master.train(is_success)

    print("끝")
