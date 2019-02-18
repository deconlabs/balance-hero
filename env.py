import mechanism
import numpy as np


class Env:
    def __init__(self, args):
        self.state_bin_size = args.state_bin_size
        self.amount_bin_size = args.amount_bin_size
        self.price = args.price
        self.quantity = args.quantity
        self.stack_to_state = self.create_stack_to_state()
        self.commision_pool = args.commision_pool
        self.mechanism = args.mechanism
        self.cp_rate = args.cp_rate
        self.cp_minimum = args.cp_minimum
        self.cp_table = self.create_cp_table()
        self.total_cp = sum(self.cp_table)
        self.n_agent = args.n_agent

        self.credits = self.create_credit_dict()
        self.rates = self.create_rate_dict()

    def create_credit_dict(self):
        # 에이전트의 신용등급 분포
        # 대출거래고객의 신용등급 분포에 따라 랜덤 배정
        # 2018년 12월 개인신용평가 관련 통계자료 기준
        # http://www.niceinfo.co.kr/creditrating/cb_score_3.nice

        p = np.array([0.2820866, 0.16822173, 0.1433743, 0.11848693, 0.10438483,
                      0.06542559, 0.03797563, 0.03051768, 0.03119231, 0.0183344])
        return {id_: np.random.choice(np.arange(1, 11), 1, p=p)[0] for id_ in range(self.n_agent)}

    def create_rate_dict(self):
        # 상위 5개 은행 대출 이자율의 평균
        # 은행 순위: 2018년 9월 금감원 금융정보통계시스템 기준
        # http://fisis.fss.or.kr/fss/fsiview/indexw_ng.html

        # 에이전트의 신용등급별에 따라 이자율이 다름
        # 이자율 출처: 전국은행연합회
        # https://portal.kfb.or.kr/main/main.php

        rates_ = [0.03734, 0.03734, 0.04508, 0.04508, 0.06042, 0.06042, 0.07946, 0.07946, 0.09475, 0.09475]
        return {id_: rates_[self.credits[id_] - 1] for id_ in range(self.n_agent)}

    def refine_orderbook(self, orderbook):
        amounts, whens, times = dict(), dict(), dict()
        for order in orderbook:
            amounts[order["id"]] = order["amount"]
            whens[order["id"]] = order["when"]
            times[order["id"]] = order["timestamp"]
        return amounts, whens, times

        # 오더 여러번 할 수 있는 경우를 위한 코드
        # orders = defaultdict(lambda: [])
        # for order in orderbook:
        #     orders[order["id"]].append({"amount": order["amount"],
        #                                 "when": order["when"],
        #                                 "state": order["when"] // self.bin_size})
        # return orders

    def get_cost(self, amount, r, t):
        try:
            # TODO: t의 스케일을 어떻게 조절해야 할 지 모르겠다.
            # 지금으로써는 3초 지나면 3제곱, 20초 지나면 20제곱으로 엄청나게 크다
            m = self.price * amount
            return m * ((1 + r) ** t)
        except OverflowError as e:
            print(m, r, t)
            raise e

    def get_cp(self, amount, when):
        return sum(self.cp_table[when - amount:when])

    def get_benefit(self, cp):
        return self.commision_pool * cp / self.total_cp

    def step(self, orderbook, infos):
        amounts, whens, times = self.refine_orderbook(orderbook)
        print("amounts: ", amounts)
        start_time = infos["start_time"]
        for id_ in times.keys():
            times[id_] = (times[id_] - start_time) / 1000.  # millisecond

        costs = {id_: self.get_cost(amounts[id_], self.rates[id_], times[id_])
                 for id_ in amounts.keys()}
        if infos["is_success"]:
            cps = {id_: self.get_cp(amounts[id_], whens[id_])
                   for id_ in amounts.keys()}
            benefits = {id_: self.get_benefit(cps[id_])
                        for id_ in costs.keys()}
        else:
            benefits = {id_: 0 for id_ in costs.keys()}

        rewards = {id_: benefits[id_] - costs[id_] for id_ in costs.keys()}
        return rewards

    def create_stack_to_state(self):
        state_idx = 1
        stack_to_state = dict()
        while self.amount_bin_size * state_idx < self.state_bin_size:
            stack_to_state[self.amount_bin_size * state_idx] = state_idx
            state_idx += 1
        i = 1
        while self.state_bin_size * i <= self.quantity:
            stack_to_state[self.state_bin_size * i] = state_idx
            i += 1
            state_idx += 1
        return stack_to_state

    def create_cp_table(self):
        if self.mechanism == 0:
            return mechanism.cp_random(self.quantity)
        elif self.mechanism == 1:
            return mechanism.uniform(self.quantity)
        elif self.mechanism == 2:
            return mechanism.linear_upward(self.quantity, self.cp_rate, self.cp_minimum)
        elif self.mechanism == 3:
            return mechanism.linear_downward(self.quantity, self.cp_rate, self.cp_minimum)
        elif self.mechanism == 4:
            return mechanism.convex(self.quantity, self.cp_rate, self.cp_minimum)
        elif self.mechanism == 4:
            return mechanism.concave(self.quantity, self.cp_rate, self.cp_minimum)
