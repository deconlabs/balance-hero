import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import glob
import json
from arguments import argparser
from collections import deque


import sys


def visualize(path, args=None):  # path = new_test

    mechs_name = ['random', 'uniform', 'increasing', 'decreasing', 'convex', 'concave']

    for mech in range(0, 6):
        all_dir = sorted(os.listdir(os.path.join('logs', path)))  # n = 30
        all_dir = [dir for dir in all_dir if 'mechanism=' + str(mech) in dir]

        all_json_files = []
        for dir_ in all_dir:  # 30 folders in each mechanism folder
            json_files = sorted(glob.glob(os.path.join('logs', path, dir_, '*')))  # 500개의  json file
            all_json_files.append(json_files)

        all_json_files = np.array(all_json_files)
        # print(all_json_files.shape)
        # sys.exit()

        summarized_success = []
        summarized_dealtime = []

        for episode_files in all_json_files.T:  # n.of episode_files = about 30

            # print(episode_files)
            # print(type(episode_files))
            # print(episode_files.shape)
            is_success = deque(maxlen=30)
            deal_time = deque(maxlen=30)

            for episode_file in episode_files:
                # print(episode_file)
                with open(episode_file) as f:
                    data = json.load(f)
                    is_success.append(data['dealSuccess'])
                    if not data['dealSuccess']:
                        deal_time.append(3000)
                    else:
                        deal_time.append(data['dealTime'])

            summarized_success.append(np.mean(is_success))
            summarized_dealtime.append(np.mean(deal_time))


        n_episode = len(summarized_success)
        window = args.window

        success_rate = np.array(
            [np.mean(summarized_success[step * window: (step + 1) * window]) for step in range(n_episode // window)])
        success_rate = success_rate[~np.isnan(success_rate)]

        xx = np.arange(len(success_rate))
        yy = success_rate
        sns.regplot(xx, yy, order=5, ci=None, truncate=True, label=mechs_name[mech])



    middle_path = os.path.join('images', path)
    if not os.path.exists(middle_path):
        os.makedirs(middle_path)
    plt.title("success_rate_recent20")
    plt.xlabel("Episodes")
    plt.ylabel("success_rate(%)")
    plt.legend()
    plt.savefig(middle_path + '/total_graphs', dpi=300)
    plt.close()

if __name__ == '__main__':
    args = argparser()
    visualize(args.vis_dir, args)
