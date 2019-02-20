import numpy as np
import requests
import json
import time
import random
import utils


class Agent():
    def __init__(self, args):
        self.quantity = args.quantity
        self.max_purchase_quantity = args.max_purchase_quantity
        self.amount_bin_size = args.amount_bin_size
        self.state_bin_size = args.state_bin_size

        self.temperature = args.temperature
        self.lr = args.lr
        self.rate = utils.get_interest_rate()
        self.price = args.price

        # TODO: epsilon을 state마다 따로 둘까? 아니면 action마다 따로 둬야 하나?
        # TODO: Q_Epsilon은 State마다 따로 두고,
        # TODO: P_Epsilon은 (State,Action)마다 따로 줄까?
        self.q_eps = 1.0
        self.p_eps = 1.0
        self.q_eps_decay = args.q_eps_decay
        self.p_eps_decay = args.p_eps_decay

        self.window = args.window
        self.stack_to_state = self.create_stack_to_state()
        self.benefit_tables = {state: self.create_benefit_table(stack) for stack, state in self.stack_to_state.items()}
        self.times = {state: utils.MovingAverage(self.window) for state in self.stack_to_state.values()}

        self.uri = "http://localhost:3000"
        self.headers = {'Content-type': 'application/json'}
        self.id = None

        self.query_minimum = args.query_minimum
        self.query_diff = args.query_diff
        self.query_std = args.query_std

    def get_query_interval(self):
        # TODO: query interval 에이전트 특성으로 좀 주고 평균에 따라 정규분포 샘플링 등 해서
        # 에이전트마다 차이가 있으나 너무 deterministic하지 않게 바꿔줘야 함: diff, std 조정

        # TODO: 현재 쿼리 인터벌이 너무 줄세우는 식으로 진행이 되는데 좀 섞이게끔 해야할 것 같음
        # 너무 123456789 이게 심한 것 같은데.. 잘 모르겠다
        mu = self.query_minimum + self.id * self.query_diff
        return max(self.query_minimum, random.gauss(mu, self.query_std))

    def create_benefit_table(self, stack):
        # TODO: 최대 구매 수량 제한을 에이전트별로 다르게 하는 것도 괜찮을까?
        max_n_actions = (self.max_purchase_quantity // self.amount_bin_size) + 1
        n_actions = (stack // self.amount_bin_size) + 1
        n_actions = min(max_n_actions, n_actions)
        benefit_table = [utils.MovingAverage(self.window) for _ in range(n_actions)]
        return benefit_table

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

    def set_id(self, id_):
        self.id = id_

    def act(self, state, q_eps, p_eps, deterministic=False):
        benefit_table = self.benefit_tables[state]
        avg_benefits = np.array([table.avg for table in benefit_table])

        if np.random.random() > q_eps or deterministic:
            action = np.random.choice(np.array(range(len(avg_benefits)))[avg_benefits == avg_benefits.max()])
        else:
            action = np.random.choice(range(len(avg_benefits)))
        action = int(action)

        if action == 0:
            return action

        amount = action * self.amount_bin_size

        expected_benefit = avg_benefits[action]
        expected_cost = self.get_cost(amount=amount,
                                      r=self.rate,
                                      t=self.times[state].avg)
        # print("id {}: B/C = {:.2}/{:.2}".format(self.id, expected_benefit, expected_cost))

        if np.random.random() > p_eps or deterministic:
            if expected_benefit < expected_cost:
                action = 0
            else:
                pass
        else:
            if np.random.random() > 0.5:
                action = 0
            else:
                pass
        return action

    def learn(self, state, action, reward, time):
        try:
            self.benefit_tables[state][action].update(reward)
            self.times[state].update(time)

        except IndexError as e:
            print("id: {}, state: {}, action: {}".format(self.id, state, action))
            print({key: len(value) for key, value in self.beta_tables.items()})
            raise e

    def purchase(self, amount, id_):
        data = json.dumps({
            "id": id_,
            "amount": amount
        })
        res = requests.post(utils.URI + "/purchase", headers=utils.HEADERS, data=data)
        msg = json.loads(res.text)["msg"]
        result = False
        if 'success' in msg.lower():
            result = True
        return result

    def start(self, cnt, is_alive, s_a_dict, n_agent):
        random.seed()
        np.random.seed()

        with cnt.get_lock():
            cnt.value += 1
        while cnt.value != n_agent:
            pass

        while is_alive.value == 1:
            # 매 번 쿼리 인터벌이 조금씩 변화
            time.sleep(self.get_query_interval())
            stack = utils.get_stack()
            if stack == 0:
                break

            state = self.stack_to_state[self.process_stack(stack)]
            action = self.act(state, self.q_eps, self.p_eps)
            if action != 0:
                amount = action * self.amount_bin_size
                is_successful = self.purchase(amount, self.id)
                # print("id: {}, state: {}, action: {}, amount: {}, success: {}"
                #       .format(self.id, state, action, amount, is_successful))
                if is_successful:
                    # 성공적으로 구매를 했다면 구매 당시의 (state, action)을 s_a_dict에 기록
                    s_a_dict[self.id] = {"state": state, "action": action}
                    break
        return True

    def process_stack(self, stack):
        processed = None
        if stack < self.state_bin_size:
            processed = stack
        else:
            processed = (stack // self.state_bin_size) * self.state_bin_size
        return processed

    def get_cost(self, amount, r, t):
        try:
            # TODO: t의 스케일을 어떻게 조절해야 할 지 모르겠다.
            # 지금으로써는 3초 지나면 3제곱, 20초 지나면 20제곱으로 엄청나게 크다
            m = self.price * amount
            return m * ((1 + r) ** t)
        except OverflowError as e:
            print(m, r, t)
            raise e

    def update_eps(self):
        self.q_eps *= self.q_eps_decay
        self.p_eps *= self.p_eps_decay
