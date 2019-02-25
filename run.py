from env import Env
from agent import Agent
from master import Master
from arguments import argparser
import numpy as np
import sys
import utils
from visualization import visualize


def run():
    args = argparser()

    path = utils.create_log_dir(sys.argv)
    utils.start(args.http_port)

    env = Env(args)
    agents = [Agent(args) for _ in range(args.n_agent)]
    master = Master(args)

    for agent in agents:
        master.add_agent(agent)
    master.add_env(env)

    success_list = []
    time_list = []

    for idx in range(args.n_episode):
        print('=' * 80)
        print("Episode {}".format(idx + 1))
        # 서버의 stack, timer 초기화
        print("서버를 초기화하는중...")
        master.reset(path)

        # 에피소드 시작
        master.start()
        # 에이전트 학습
        master.train()
        print('=' * 80)
        success_list.append(master.infos["is_success"])
        time_list.append(master.infos["end_time"] - master.infos["start_time"])

        if (idx + 1) % args.print_interval == 0:
            print("=" * 80)
            print("EPISODE {}: Avg. Success Rate / Time: {:.2} / {:.2}"
                  .format(idx + 1, np.mean(success_list), np.mean(time_list)))
            success_list.clear()
            time_list.clear()
            print("=" * 80)

        if (idx + 1) % args.checkpoint_interval == 0:
            utils.save_checkpoints(path, agents, idx + 1)

    if args.visual:
        visualize(path, args)
    print("끝")
    utils.close()


if __name__ == '__main__':
    run()
