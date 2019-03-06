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


# def draw_is_success_graph(n_episode, is_success, path):
#     xx = np.arange(n_episode)
#     yy = is_success
#     cmap = plt.get_cmap("tab10")
#
#     ax = sns.regplot(xx, yy, order=5, color=cmap(0), truncate=True)
#
#     ax.plot(xx, yy, label='Success Rate', color=cmap(0), alpha=0.3)
#     ax.set_title("is_success_recent")
#     ax.set_xlabel("Episodes")
#     ax.set_ylabel("is_success")
#
#     # Ignore Outliers
#     ylim_cnt = max(int(len(yy) * 0.2), 1)
#     sorted_yy = sorted(yy)
#     ylim_min = np.mean(sorted_yy[:ylim_cnt])
#     ylim_max = np.mean(sorted_yy[-ylim_cnt:])
#     ax.set_ylim(ylim_min - 0.02, ylim_max + 0.05)
#
#     middle_path = os.path.join('images', path)
#     if not os.path.exists(middle_path):
#         os.makedirs(middle_path)
#     plt.savefig(os.path.join(middle_path, "is_success.png"), dpi=300)
#     plt.close()


def slide_window_success_rate_no_overlap(n_episode, window, is_success, path):
    success_rate = np.array([np.mean(is_success[step * window: (step + 1) * window]) for step in range(n_episode // window)])
    success_rate = success_rate[~np.isnan(success_rate)]

    xx = np.arange(len(success_rate))
    yy = success_rate
    cmap = plt.get_cmap("tab10")

    ax = sns.regplot(xx, yy, order=5, ci= None, color=cmap(0), truncate=True)

    # ax.plot(xx, yy, label='Success Rate', color=cmap(0), alpha=0.3)
    ax.set_title("success_rate_recent20")
    ax.set_xlabel("Episodes")
    ax.set_ylabel("success_rate(%)")

    # Ignore Outliers
    ylim_cnt = max(int(len(yy) * 0.2), 1)
    sorted_yy = sorted(yy)
    ylim_min = np.mean(sorted_yy[:ylim_cnt])
    ylim_max = np.mean(sorted_yy[-ylim_cnt:])
    ax.set_ylim(ylim_min - 0.02, ylim_max + 0.05)

    middle_path = os.path.join('images', path)
    if not os.path.exists(middle_path):
        os.makedirs(middle_path)
    plt.savefig(os.path.join(middle_path, args.mech+"slide_window_success_rate.png"), dpi=300)
    plt.close()


def draw_dealtime_graph(n_episode, deal_time, path):
    xx = np.arange(n_episode)
    yy = np.array(deal_time)
    cmap = plt.get_cmap("tab10")

    ax = sns.regplot(xx, yy, order=5, color=cmap(0), ci=None)

    # ax.plot(xx, yy, label='Deal Time', color=cmap(0), alpha=0.3)
    ax.set_title("Deal Time Trend(ms)")
    ax.set_xlabel("Episodes")
    ax.set_ylabel("Deal Time")

    # Ignore Outliers
    ylim_cnt = max(int(len(yy) * 0.2), 1)
    sorted_yy = sorted(yy)
    ylim_min = np.mean(sorted_yy[:ylim_cnt])
    ylim_max = np.mean(sorted_yy[-ylim_cnt:])
    ax.set_ylim(ylim_min - 10, ylim_max + 10)

    middle_path = os.path.join('images', path)
    if not os.path.exists(middle_path):
        os.makedirs(middle_path)
    plt.savefig(os.path.join(middle_path, args.mech+"deal_time.png"), dpi=300)
    plt.close()


# def draw_purchase_graph(orderbook, start_time, timer, path, idx):
#     # try:
#     #     print(orderbook[0]['when'])
#     # except:
#     #     print(orderbook)
#     quantity = np.max([order["when"] for order in orderbook])
#     prev_point = (0, quantity)
#     for order in orderbook:
#         id_ = order['id']
#         amount = order['amount']
#         timestamp = order['timestamp']
#
#         next_point = (timestamp - start_time, prev_point[1] - amount)
#         plt.plot(*list(zip(prev_point, next_point)), label=id_)
#         plt.annotate(id_, xy=prev_point)
#
#         prev_point = next_point
#
#     plt.xlim(0, timer)
#     plt.ylim(0, quantity)
#     plt.xlabel("Deal_time(ms)")
#     plt.ylabel("remain_amount")
#     plt.title("purchase tracker")
#
#     middle_path = os.path.join('images', path)
#     if not os.path.exists(middle_path):
#         os.makedirs(middle_path)
#     plt.savefig(os.path.join(middle_path, "purchase_amount_{}".format(idx)), dpi=300)
#     plt.close()

import sys
def visualize(path, args=None): #path = new_test

    all_dir = sorted(os.listdir(os.path.join('logs',path))) # n = 30

    all_dir = [dir for dir in all_dir if 'mechanism='+args.mech in dir]


    all_json_files = []
    for dir_ in all_dir:    #30 folders in each mechanism folder
        json_files = sorted(glob.glob(os.path.join('logs', path,dir_, '*'))) #500개의  json file
        all_json_files.append(json_files)

    all_json_files=np.array(all_json_files)
    # print(all_json_files.shape)
    # sys.exit()

    summarized_success =[]
    summarized_dealtime=[]


    for episode_files in all_json_files.T: # n.of episode_files = about 30
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


    # draw_is_success_graph(len(is_success), np.array(is_success), path)
    # print((summarized_success))
    # print(len(summarized_dealtime))

    slide_window_success_rate_no_overlap(len(summarized_success), args.window, np.array(summarized_success), path)
    draw_dealtime_graph(len(summarized_dealtime), summarized_dealtime, path)


if __name__ == '__main__':
    args = argparser()
    visualize(args.vis_dir, args)
