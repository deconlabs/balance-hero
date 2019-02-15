# def f(a, b, N, x):
#     """
#     :param a: 기울기, 곡률
#     :param b: 가장 낮은 커미션 포인트 (b > 0)
#     :param N: 총 order의 수
#     :param x: input
#     :return: output
#     """
#     return y


# 우하향 선형 그래프를 위한
# y = ax + (c0 - aN)
def mechanism_v1(a, c0, N, x):
    """
    :param a: 기울기 (< 0)
    :param c0: 마지막 구매의 커미션포인트 (> 0)
    :param N: 총 order의 수
    :param x: input
    :return: output
    """
    return a * x + (c0 - a * N)


# 우상향 선형 그래프를 위한
# y = ax + b
def mechanism_v2(a, b, N, x):
    """
    :param a: 기울기 (> 0)
    :param b: 처음 구매의 커미션 포인트 (> 0)
    :param x: input
    :return: output
    """
    return a * x + b


# uniform
# y = u
def mechanism_v3(a, u, N, x):
    """
    :param u: 얻는 커미션 포인트 (> 0)
    :param x: input
    :return: output
    """
    return u


# Convex
# y = a(x - N / 2)^2 + c0
def mechanism_v4(a, c0, N, x):
    """
    :param a: 곡률 (> 0)
    :param c0: 가장 낮은 커미션포인트 (> 0)
    :param N: 총 order의 수
    :param x: input
    :return: output
    """
    return a * (x - N / 2) ** 2 + c0

# Concave
# y = a(x - N / 2)^2 + (b - a * N^2 / 4)
def mechanism_v5(a, b, N, x):
    """
    :param a: 곡률 (< 0)
    :param b: 처음과 마지막의 커미션 포인트 (> 0)
    :param N: 총 order의 수
    :param x: input
    :return: output
    """
    return a * (x - N / 2) ** 2 + (b - a * (N ** 2) / 4)
