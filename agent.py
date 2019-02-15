import numpy as np
import requests
import json
import time
import random


class Agent():
    def __init__(self, args):
        self.quantity = args.quantity
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
        self.query_interval = 0.5

    def create_q_table(self, stack):
        n_actions = (stack // self.amount_bin_size) + 1
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
            print(self.q_tables)
            raise e

    def get_stack(self):
        res = requests.get(self.uri + "/stack")
        stack = json.loads(res.text)["stack"]
        return stack

    def purchase(self, amount, id_):
        data = json.dumps({
            "id": id_,
            "amount": amount
        })
        res = requests.post(self.uri + "/purchase", headers=self.headers, data=data)
        msg = json.loads(res.text)["msg"]
        result = False
        if 'success' in msg.lower():
            result = True
        return result

    def start(self, cnt, is_alive, n_agent):
        random.seed()
        np.random.seed()

        with cnt.get_lock():
            cnt.value += 1
        while cnt.value != n_agent:
            pass

        while is_alive.value == 1:
            stack = self.get_stack()
            if stack == 0:
                break
            state = self.stack_to_state[self.process_stack(stack)]
            action = self.get_action(state)
            if action != 0:
                amount = action * self.amount_bin_size
                print("id: {}, action: {}, amount: {}".format(self.id, action, amount))
                is_successful = self.purchase(amount, self.id)
                if is_successful:
                    break
            time.sleep(self.query_interval)
        return True

    def process_stack(self, stack):
        processed = None
        if stack < self.state_bin_size:
            processed = stack
        else:
            processed = (stack // self.state_bin_size) * self.state_bin_size
        return processed
