from env import Env
from agent import Agent
from master import Master
from arguments import argparser

import sys
import os


def run():
    # try:
    #     os.chdir("./server")
    #     os.system("npm install --silent")
    #     os.system("npm start &")
    # finally:
    #     os.chdir("../")

    args = argparser()

    """log를 저장할 dir 생성"""
    if not os.path.isdir('./logs/'):
        os.mkdir('./logs/')
    my_args = sys.argv
    path_ = []
    for idx in range(1, len(my_args)):
        path_.append(my_args[idx][2:])
    path = '_'.join(path_) + '/'
    if not os.path.isdir('./logs/' + path):
        os.mkdir('./logs/' + path)

    env = Env(args)
    agents = [Agent(args) for _ in range(args.n_agent)]
    master = Master(args)

    for agent in agents:
        master.add_agent(agent)
    master.add_env(env)

    for idx in range(args.n_episode):
        print("에피소드 {} 초기화".format(idx + 1))
        # 서버의 stack, timer 초기화
        print("서버를 초기화하는중...")
        master.reset(path)

        # 에피소드 시작
        print("에피소드 시작...")
        master.start()
        # 에이전트 학습
        print("에이전트 학습 중...")
        master.train()

    print("끝")


if __name__ == '__main__':
    run()
