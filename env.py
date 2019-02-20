import mechanism


class Env:
    def __init__(self, args):
        self.state_bin_size = args.state_bin_size
        self.amount_bin_size = args.amount_bin_size
        self.price = args.price
        self.quantity = args.quantity
        self.stack_to_state = self.create_stack_to_state()
        self.commission_pool = args.commission_pool
        self.mechanism = args.mechanism
        self.cp_rate = args.cp_rate
        self.cp_minimum = args.cp_minimum
        self.cp_table = self.create_cp_table()
        self.total_cp = sum(self.cp_table)
        self.n_agent = args.n_agent

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

    def get_cp(self, amount, when):
        return sum(self.cp_table[when - amount:when])

    def get_benefit(self, cp):
        return self.commission_pool * cp / self.total_cp

    def step(self, orderbook, infos):
        amounts, whens, times = self.refine_orderbook(orderbook)
        # print("amounts: ", amounts)

        if infos["is_success"]:
            # 성공한 경우 딜이 끝난 시간은 마지막 오더의 timestamp
            end_time = max(times.values())
        else:
            # 실패한 경우 딜이 끝난 시간은 시작한 시간 + 딜 진행 시간
            end_time = infos["start_time"] + infos["timer"]

        infos["end_time"] = end_time

        for id_ in times.keys():
            times[id_] = (end_time - times[id_]) / 1000.  # millisecond

        if infos["is_success"]:
            cps = {id_: self.get_cp(amounts[id_], whens[id_])
                   for id_ in amounts.keys()}
            benefits = {id_: self.get_benefit(cps[id_])
                        for id_ in amounts.keys()}
        else:
            benefits = {id_: 0 for id_ in amounts.keys()}

        rewards = benefits
        return rewards, times

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
