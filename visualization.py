import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def draw_success_rate_graph(n_episode, window, success_rate, path):
    plt.plot(np.arange(n_episode) + window, success_rate, label='success_rate')
    plt.title("success_rate_recent20")
    plt.xlabel("Episodes")
    plt.ylabel("success_rate(%)")
    plt.show()

    middle_path = os.path.join('images', path)
    if not os.path.exists(middle_path):
        os.makedirs(middle_path)
    plt.savefig(os.path.join(middle_path, "success_rate.png"))
    plt.close()
    print('drew success_rate_graph !')


def draw_dealtime_graph(n_episode, deal_time, path):
    plt.plot(np.arange(n_episode), deal_time, label='deal_time')
    plt.title("deal_time_trend(ms)")
    plt.xlabel("Episodes")
    plt.ylabel("deal_time")
    plt.show()

    middle_path = os.path.join('images', path)
    if not os.path.exists(middle_path):
        os.makedirs(middle_path)
    plt.savefig(os.path.join(middle_path,"deal_time.png"))
    plt.close()

    print(os.path.join(middle_path,"deal_time.png")+'is drawn' )

def draw_purchase_graph(orderbook, start_time, quantity, path,idx):
    prev_point = (0, quantity)
    for order in orderbook:
        id_ = order['id']
        amount = order['amount']
        timestamp = order['timestamp']

        next_point = (timestamp - start_time, prev_point[1] - amount)
        plt.plot(*list(zip(prev_point, next_point)), label=id_)
        plt.xlabel("Deal_time(ms)")
        plt.ylabel("remain_amount")
        plt.title("purchase tracker")
        plt.annotate(id_, xy=prev_point)

        prev_point = next_point

    middle_path = os.path.join('images', path)
    if not os.path.exists(middle_path):
        os.makedirs(middle_path)
    plt.savefig(os.path.join(middle_path, "purchase_amount_{}".format(idx)))
    plt.close()


import os
import glob
import json


def visualize(path, args=None):
    json_files = glob.glob(os.path.join('logs',path, '*'))
    print(json_files)
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

    suc_rate = [np.mean(success_rate[i:i + 20]) for i in range(len(success_rate) - 20)]


    draw_success_rate_graph(len(suc_rate), 20, suc_rate, path)
    draw_dealtime_graph(len(deal_time), deal_time, path)
    idx = 0
    for orderbook, start_time in zip(orders, start_times):
        if start_time != -1 :
            draw_purchase_graph(orderbook, start_time, 1000,  path, idx )
            print('{}th purchase graph was drawn'.format(idx))
            idx += 1


if __name__ == '__main__':
    visualize(path=sys.argv[1], )
