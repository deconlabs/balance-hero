# balance-hero
'balance hero' simulator.

## TODO
- [x] 이자율 에이전트마다 다르게 하기 / 이름도 바꾸기(rates에서)
- [x] 커미션 포인트 계산
- [x] utils.py로 빼주기
- [x] query interval 바꾸기. 에이전트마다 평균값만 부여해주고 평균값에서 샘플링. 지난번 프로젝트 like 구하는 것처럼
- [x] 최대 구매 수량 제한 걸기(일괄적으로 최대 구매 수량 제한 똑같이 구현)
- [x] 에이전트 오더마다 시간(t)을 다르게 줘야하는데 일괄적으로 주게 되어있어 수정
- [x] 에이전트 행동 2단계로 나누기 1 - (구매 / 비구매) 2 - 구매한다면 몇개나 살지로? - 리서치 필요
- [x] 매 에피소드마다 Synchronous하게 로그를 기록하느랴 File I/O에 로드가 걸리는 부분 해결
- [x] 전체적으로 리워드가 전부 (-)이고 에이전트마다 차이도 너무 커서 수정 필요함(가장 시급한 건 time 제곱 수정)
- [ ] 에이전트 별 최대 구매 수량 제한 다르게 해볼까?
- [ ] 하이퍼파라미터 튜닝
- [ ] 시각화
- [ ] 주석
