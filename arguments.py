import argparse


def argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--n_agent', type=int, default=20,
                        help='에이전트 수')
    parser.add_argument('--n_episode', type=int, default=2300,
                        help='에피소드 수')
    parser.add_argument('--mechanism', type=int, default=1,
                        help='mechanism (0, 1, 2, ...) 추후 추가')  # 수정요망
    parser.add_argument('--cp_rate', type=float, default=1.0,
                        help='커미션포인트의 변화율(기울기, 곡률)')
    parser.add_argument('--cp_minimum', type=float, default=1.0,
                        help='커미션포인트의 최솟값')

    parser.add_argument('--commission_pool', type=float, default=200.0,
                        help='reserved pool for distributing commision')

    parser.add_argument('--quantity', type=int, default=100,
                        help='물품 판매 수량')
    parser.add_argument('--price', type=float, default=1.0,
                        help='물품의 가격')
    parser.add_argument('--amount_bin_size', type=int, default=1,
                        help='최소 구매 단위')
    parser.add_argument('--max_purchase_quantity', type=int, default=10,
                        help='최대 구매 수량')

    parser.add_argument('--timer', type=float, default=3000,
                        help='딜 진행 시간')

    parser.add_argument('--state_bin_size', type=int, default=10,
                        help='state 단위')
    parser.add_argument('--window', type=int, default=20,
                        help='State마다 저장되는 time의 moving mean window size')

    parser.add_argument('--q_eps_decay', type=float, default=0.998,
                        help='decay rate for q_eps')
    parser.add_argument('--p_eps_decay', type=float, default=0.998,
                        help='decay rate for p_eps')

    parser.add_argument('--query_minimum', type=float, default=0.5,
                        help='default(minimum) query interval')
    parser.add_argument('--query_diff', type=float, default=0.01,
                        help='에이전트간 쿼리 인터벌 차이 비율')
    parser.add_argument('--query_std', type=float, default=0.01,
                        help='쿼리 정규분포에 사용되는 표준편차')

    parser.add_argument('--http_port', type=str, default='3000',
                        help='서버가 이용할 포트')
    parser.add_argument('--vis_dir', type=str, default='_',
                        help='Visualization을 CLI에서 실행하기 위한 argument')

    parser.add_argument('--print_interval', type=int, default=20,
                        help='터미널 출력 간격')
    parser.add_argument('--checkpoint_interval', type=int, default=5,
                        help='체크포인트 저장 간격')

    parser.add_argument('--visual', type=bool, default=True,
                        help='물품 판매 수량')  # 수정요망

    args = parser.parse_args()
    return args
