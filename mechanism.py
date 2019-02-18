import random


# Random
def cp_random(quantity):
    return [random.random() for _ in range(quantity)]


# Uniform
def uniform(quantity):
    return [1 for _ in range(quantity)]


# Linear graph slopes upward from left to right
def linear_upward(quantity, a, b):
    """
    :param quantity: 물품 판매 수량
    :param a: 기울기 (> 0)
    :param b: 최저점
    :return: array
    """
    return [a * i + b for i in range(quantity)]


# Linear graph slopes downward from left to right
def linear_downward(quantity, a, b):
    """
    :param quantity: 물품 판매 수량
    :param a: 기울기 (< 0)
    :param b: 최저점
    :return: array
    """
    return [a * i + (b - a * quantity) for i in range(quantity)]


# Convex
def convex(quantity, a, b):
    """
    :param quantity: 물품 판매 수량
    :param a: 곡률 (> 0)
    :param b: 최저점
    :return: array
    """
    return [a * (i - quantity / 2) ** 2 + b for i in range(quantity)]


# Concave
def concave(quantity, a, b):
    """
    :param quantity: 물품 판매 수량
    :param a: 곡률 (< 0)
    :param b: 최저점
    :return: array
    """
    return [a * (i - quantity / 2) ** 2 + (b - a * (quantity ** 2) / 4) for i in range(quantity)]
