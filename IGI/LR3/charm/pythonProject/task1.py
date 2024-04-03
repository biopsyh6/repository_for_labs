import math


def benchmark(func):
    """
    Measure execution time.

    :param func: function
    :return: function result
    """
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, *kwargs)
        end = time.time()
        print(f"Время выполнения {end-start} секунд")
        return result
    return wrapper


@benchmark
def solve_sin(x, eps):
    """
    Solve sinus.

    :param x: value in radians
    :param eps: calculation accuracy
    :return: sinus result, number of series members
    """
    S = 0  # Сумма ряда на старте
    i = 1  # Порядковый номер слагаемого в ряду Тейлора
    q = x
    itetations = 0
    # Пока очередное слагаемое больше погрешности
    while abs(q) > eps and itetations <= 500:
        S = S + q
        q = q * (-1) * (x*x) / ((2*i+1) * (2*i))
        i += 1
        itetations += 1
    return S, i