import argparse


def argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--quantity', type=int, default=1000,
                        help='물품 판매 수량')
    parser.add_argument('--price', type=float, default=1.0,
                        help='물품의 가격')
    parser.add_argument('--timer', type=float, default=3000,
                        help='딜 진행 시간')
    parser.add_argument('--amount_bin_size', type=int, default=10,
                        help='최소 구매 단위')
    parser.add_argument('--state_bin_size', type=int, default=100,
                        help='state 단위')
    parser.add_argument('--max_purchase_quantity', type=int, default=200,
                        help='최대 구매 수량')
    parser.add_argument('--n_agent', type=int, default=10,
                        help='에이전트 수')
    parser.add_argument('--n_episode', type=int, default=1000,
                        help='에피소드 수')
    parser.add_argument('--lr', type=float, default=0.01,
                        help='learning rate')
    parser.add_argument('--temperature', type=float, default=2.0,
                        help='temperature for softmax')
    parser.add_argument('--commision_pool', type=float, default=10.0,
                        help='reserved pool for distributing commision')
    parser.add_argument('--mechanism', type=int, default=0,
                        help='mechanism (0, 1, 2, ...) 추후 추가')

    args = parser.parse_args()
    return args
