import os
from env import Env
from agent import Agent
from master import Master
from arguments import argparser


def run():
    try:
        os.chdir("./server")
        os.system("npm install --silent")
        os.system("npm start &")
    finally:
        os.chdir("../")

    args = argparser()

    env = Env(args)
    agents = [Agent(args) for _ in range(args.n_agent)]
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


if __name__ == '__main__':
    run()
