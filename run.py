from env import Env
from agent import Agent
from master import Master
from arguments import argparser
import utils


def run():
    # try:
    #     os.chdir("./server")
    #     os.system("npm install --silent")
    #     os.system("npm start &")
    # finally:
    #     os.chdir("../")

    args = argparser()

    env = Env(args)
    agents = [Agent(args) for _ in range(args.n_agent)]
    master = Master(args)

    for agent in agents:
        master.add_agent(agent)
    master.add_env(env)

    for idx in range(args.n_episode):
        print("에피소드 {} 초기화".format(idx+1))
        # 서버의 stack, timer 초기화
        print("서버를 초기화하는중...")
        master.reset()
        # 에피소드 시작
        print("에피소드 시작...")
        master.start()
        # 에이전트 학습
        print("에이전트 학습 중...")
        is_success = utils.get_is_success()
        time = utils.get_time(is_success, args.timer)
        master.train(is_success, time)

    print("끝")


if __name__ == '__main__':
    run()
