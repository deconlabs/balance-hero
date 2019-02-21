import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import glob
import json
from arguments import argparser
import matplotlib
matplotlib.use('Agg')


def draw_success_rate_graph(n_episode, window, success_rate, path):
    xx = np.arange(n_episode) + window
    yy = success_rate
    cmap = plt.get_cmap("tab10")

    ax = sns.regplot(xx, yy, order=5, color=cmap(0),
                     scatter_kws={"alpha": 0.}, ci=None, truncate=True)

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
    plt.savefig(os.path.join(middle_path, "success_rate.png"), dpi=300)
    plt.close()


def draw_dealtime_graph(n_episode, deal_time, timer, path):
    xx = np.arange(n_episode)
    yy = deal_time
    cmap = plt.get_cmap("tab10")

    ax = sns.regplot(xx, yy, order=5, color=cmap(0),
                     scatter_kws={"alpha": 0.}, ci=None, truncate=True)

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


def draw_purchase_graph(orderbook, start_time, quantity, timer, path, idx):
    prev_point = (0, quantity)
    for order in orderbook:
        id_ = order['id']
        amount = order['amount']
        timestamp = order['timestamp']

        next_point = (timestamp - start_time, prev_point[1] - amount)
        plt.plot(*list(zip(prev_point, next_point)), label=id_)
        plt.xlim(0, timer)
        plt.ylim(0, quantity)
        plt.xlabel("Deal_time(ms)")
        plt.ylabel("remain_amount")
        plt.title("purchase tracker")
        plt.annotate(id_, xy=prev_point)

        prev_point = next_point

    middle_path = os.path.join('images', path)
    if not os.path.exists(middle_path):
        os.makedirs(middle_path)
    plt.savefig(os.path.join(middle_path, "purchase_amount_{}".format(idx)), dpi=300)
    plt.close()


def visualize(path, args=None):
    if path.startswith('logs/'):
        path = path[5:]
    json_files = glob.glob(os.path.join('logs', path, '*'))
    success_rate = []
    deal_time = []
    orders = []
    start_times = []
    for file in json_files:
        with open(file) as f:
            data = json.load(f)
            success_rate.append(data['dealSuccess'])
            deal_time.append(data['dealTime'])
            orders.append(data['orders'])
            start_times.append(data['startTime'])

    suc_rate = [np.mean(success_rate[i:i + args.window]) for i in range(0, len(success_rate) - args.window)]

    draw_success_rate_graph(len(suc_rate), args.window, suc_rate, path)
    draw_dealtime_graph(len(deal_time), deal_time, args.timer, path)
    idx = 0
    for orderbook, start_time in zip(orders, start_times):
        if start_time != -1:
            draw_purchase_graph(orderbook, start_time, args.quantity, args.timer, path, idx)
            idx += 1


if __name__ == '__main__':
    args = argparser()
    visualize(args.vis_dir, args)
