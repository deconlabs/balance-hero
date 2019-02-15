class Env:
    def __init__(self, args):
        self.state_bin_size = args.state_bin_size
        self.amount_bin_size = args.amount_bin_size
        self.price = args.price
        self.quantity = args.quantity
        self.commision_pool = args.commision_pool
        self.mechanism = args.mechanism
        self.total_cp = self.calculate_total_cp(self.mechanism)
        self.rates = dict()

    def calculate_total_cp(self, mec):
        # uniform
        return self.quantity

    def refine_orderbook(self, orderbook):
        amounts, whens, states = dict(), dict(), dict()
        for order in orderbook:
            amounts[order["id"]] = order["amount"]
            whens[order["id"]] = order["when"]
            states[order["id"]] = order["state"] // self.state_bin_size
        return amounts, whens, states

        # 오더 여러번 할 수 있는 경우를 위한 코드
        # orders = defaultdict(lambda: [])
        # for order in orderbook:
        #     orders[order["id"]].append({"amount": order["amount"],
        #                                 "when": order["when"],
        #                                 "state": order["when"] // self.bin_size})
        # return orders

    def get_cost(self, amount, r, t):
        m = self.price * amount
        return m * ((1 + r) ** t)

    def get_cp(self, amount, when):
        # uniform
        return amount

    def get_benefit(self, cp):
        return self.commision_pool * cp / self.total_cp

    def step(self, orderbook, infos):
        amounts, whens, states = self.refine_orderbook(orderbook)

        is_success = infos["is_success"]
        t = infos["time"]

        costs = {id_: self.get_cost(amount, rate, t)
                 for id_, (amount, rate) in enumerate(zip(amounts, self.rates.values()))}
        if is_success:
            cps = {id_: self.get_cp(amount, when)
                   for id_, (amount, when) in enumerate(zip(amounts, whens))}
            benefits = {id_: self.get_benefit(cps[id_])
                        for id_ in costs.keys()}
        else:
            benefits = {id_: 0 for id_ in costs.keys()}

        rewards = {id_: benefits[id_] - costs[id_] for id_ in costs.keys()}
        actions = {id_: amount / self.amount_bin_size for id_, amount in amounts.items()}

        return states, actions, rewards
