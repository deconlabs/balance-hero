#!/usr/bin/env bash

# python3 run.py --n_episode=500 --mechanism=1 --q_eps_decay=0.99 --p_eps_decay=0.99 --commission_pool=200.0
python3 run.py --n_episode=500 --mechanism=2 --q_eps_decay=0.99 --p_eps_decay=0.99 --commission_pool=200.0 --cp_rate=0.2
