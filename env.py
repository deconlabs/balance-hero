class Env:
    def __init__(self, args):
        self.state_bin_size = args.state_bin_size
        self.amount_bin_size = args.amount_bin_size
        self.price = args.price
        self.quantity = args.quantity
        self.stack_to_state = self.create_stack_to_state()
        self.commision_pool = args.commision_pool
        self.mechanism = args.mechanism
        self.total_cp = self.calculate_total_cp(self.mechanism)
        # TODO: rates dictionary 잘 만들기
        self.rates = None
        self.n_agent = args.n_agent

    def calculate_total_cp(self, mec):
        # uniform
        return self.quantity

    def refine_orderbook(self, orderbook):
        amounts, whens, states = dict(), dict(), dict()
        for order in orderbook:
            amounts[order["id"]] = order["amount"]
            whens[order["id"]] = order["when"]
            states[order["id"]] = self.stack_to_state[self.process_stack(order["when"])]
        return amounts, whens, states

        # 오더 여러번 할 수 있는 경우를 위한 코드
        # orders = defaultdict(lambda: [])
        # for order in orderbook:
        #     orders[order["id"]].append({"amount": order["amount"],
        #                                 "when": order["when"],
        #                                 "state": order["when"] // self.bin_size})
        # return orders

    def get_cost(self, amount, r, t):
        try:
            m = self.price * amount
            return m * ((1 + r) ** t)
        except OverflowError as e:
            print(m, r, t)
            raise e

    def get_cp(self, amount, when):
        # uniform
        return amount

    def get_benefit(self, cp):
        return self.commision_pool * cp / self.total_cp

    def step(self, orderbook, infos):
        amounts, whens, states = self.refine_orderbook(orderbook)
        print("amounts: ", amounts)

        is_success = infos["is_success"]
        t = infos["time"]
        # TODO: rates 딕셔너리 제대로 만들기
        self.rates = {id_: 0.01 for id_ in range(self.n_agent)}

        costs = {id_: self.get_cost(amounts[id_], self.rates[id_], t)
                 for id_ in amounts.keys()}
        if is_success:
            cps = {id_: self.get_cp(amounts[id_], whens[id_])
                   for id_ in amounts.keys()}
            benefits = {id_: self.get_benefit(cps[id_])
                        for id_ in costs.keys()}
        else:
            benefits = {id_: 0 for id_ in costs.keys()}

        rewards = {id_: benefits[id_] - costs[id_] for id_ in costs.keys()}
        actions = {id_: int(amount / self.amount_bin_size) - 1 for id_, amount in amounts.items()}
        return states, actions, rewards

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

    def process_stack(self, stack):
        processed = None
        if stack < self.state_bin_size:
            processed = stack
        else:
            processed = (stack // self.state_bin_size) * self.state_bin_size
        return processed
