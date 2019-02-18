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

        self.stack_to_state = self.create_stack_to_state()
        self.q_tables = {state: self.create_q_table(stack) for stack, state in self.stack_to_state.items()}
        self.beta_tables = {state: self.softmax(self.q_tables[state]) for state in self.stack_to_state.values()}

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

    def create_q_table(self, stack):
        # TODO: 최대 구매 수량 제한을 에이전트별로 다르게 하는 것도 괜찮을까?
        max_n_actions = (self.max_purchase_quantity // self.amount_bin_size) + 1
        n_actions = (stack // self.amount_bin_size) + 1
        n_actions = min(max_n_actions, n_actions)
        return np.zeros(n_actions)

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

    def softmax(self, x):
        if not isinstance(x, np.ndarray):
            x = np.array(x)
        x = x / self.temperature
        e_x = np.exp(x - np.max(x))
        return e_x / np.sum(e_x)

    def set_id(self, id_):
        self.id = id_

    def get_action(self, state, deterministic=False):
        beta_table = self.beta_tables[state]
        if deterministic:
            action = np.random.choice(np.flatnonzero(beta_table == beta_table.max()))
        else:
            action = np.random.choice(np.arange(beta_table.size), 1, p=beta_table)
        action = int(action)
        return action

    def learn(self, state, action, reward):
        try:
            q1 = self.q_tables[state][action]
            q2 = reward

            self.q_tables[state][action] += self.lr * (q2 - q1) / self.beta_tables[state][action]
            self.beta_tables[state] = self.softmax(self.q_tables[state])
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
            action = self.get_action(state)
            if action != 0:
                amount = action * self.amount_bin_size
                is_successful = self.purchase(amount, self.id)
                print("id: {}, state: {}, action: {}, amount: {}, success: {}"
                      .format(self.id, state, action, amount, is_successful))
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
