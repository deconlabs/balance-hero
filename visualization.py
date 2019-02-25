import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import glob
import json
from arguments import argparser


def draw_is_success_graph(n_episode, is_success, path):
    xx = np.arange(n_episode)
    yy = is_success
    cmap = plt.get_cmap("tab10")

    ax = sns.regplot(xx, yy, order=5, color=cmap(0), truncate=True)

    ax.plot(xx, yy, label='Success Rate', color=cmap(0), alpha=0.3)
    ax.set_title("is_success_recent")
    ax.set_xlabel("Episodes")
    ax.set_ylabel("is_success")

    # Ignore Outliers
    ylim_cnt = max(int(len(yy) * 0.2), 1)
    sorted_yy = sorted(yy)
    ylim_min = np.mean(sorted_yy[:ylim_cnt])
    ylim_max = np.mean(sorted_yy[-ylim_cnt:])
    ax.set_ylim(ylim_min - 0.02, ylim_max + 0.05)

    middle_path = os.path.join('images', path)
    if not os.path.exists(middle_path):
        os.makedirs(middle_path)
    plt.savefig(os.path.join(middle_path, "is_success.png"), dpi=300)
    plt.close()


def slide_window_success_rate_no_overlap(n_episode, window, is_success, path):
    success_rate = np.array([np.mean(is_success[step: step * window]) for step in range(n_episode // window)])
    success_rate = success_rate[~np.isnan(success_rate)]

    xx = np.arange(len(success_rate))
    yy = success_rate
    cmap = plt.get_cmap("tab10")

    ax = sns.regplot(xx, yy, order=5, color=cmap(0), truncate=True)

    ax.plot(xx, yy, label='Success Rate', color=cmap(0), alpha=0.3)
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
    plt.savefig(os.path.join(middle_path, "slide_window_success_rate.png"), dpi=300)
    plt.close()


def draw_dealtime_graph(n_episode, deal_time, timer, path):
    xx = np.arange(n_episode)
    yy = np.array(deal_time)
    cmap = plt.get_cmap("tab10")

    ax = sns.regplot(xx, yy, order=5, color=cmap(0), )

    ax.plot(xx, yy, label='Deal Time', color=cmap(0), alpha=0.3)
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
    plt.savefig(os.path.join(middle_path, "deal_time.png"), dpi=300)
    plt.close()


def draw_purchase_graph(orderbook, start_time, timer, path, idx):
    # try:
    #     print(orderbook[0]['when'])
    # except:
    #     print(orderbook)
    quantity = np.max([order["when"] for order in orderbook])
    prev_point = (0, quantity)
    for order in orderbook:
        id_ = order['id']
        amount = order['amount']
        timestamp = order['timestamp']

        next_point = (timestamp - start_time, prev_point[1] - amount)
        plt.plot(*list(zip(prev_point, next_point)), label=id_)
        plt.annotate(id_, xy=prev_point)

        prev_point = next_point

    plt.xlim(0, timer)
    plt.ylim(0, quantity)
    plt.xlabel("Deal_time(ms)")
    plt.ylabel("remain_amount")
    plt.title("purchase tracker")

    middle_path = os.path.join('images', path)
    if not os.path.exists(middle_path):
        os.makedirs(middle_path)
    plt.savefig(os.path.join(middle_path, "purchase_amount_{}".format(idx)), dpi=300)
    plt.close()


def visualize(path, args=None):
    if path.startswith('logs/'):
        path = path[5:]
    json_files = sorted(glob.glob(os.path.join('logs', path, '*')))
    is_success = []
    deal_time = []
    orders = []
    start_times = []
    for file in json_files:
        with open(file) as f:
            data = json.load(f)
            is_success.append(data['dealSuccess'])
            deal_time.append(data['dealTime'])
            orders.append(data['orders'])
            start_times.append(data['startTime'])

    draw_is_success_graph(len(is_success), np.array(is_success), path)
    slide_window_success_rate_no_overlap(len(is_success), args.window, np.array(is_success), path)
    draw_dealtime_graph(len(deal_time), deal_time, args.timer, path)

    idx = 0
    for orderbook, start_time in zip(orders, start_times):
        # print(idx)
        if start_time != -1 and deal_time[idx]!=0:
            # print(json_files[idx])
            draw_purchase_graph(orderbook, start_time, args.timer, path, idx)
            print('{}th purchase graph is drawn'.format(idx))
        idx += 1


if __name__ == '__main__':
    args = argparser()
    visualize(args.vis_dir, args)
