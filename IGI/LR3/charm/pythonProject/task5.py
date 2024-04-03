def positive_sum(float_list):
    """
    Find sum of positive elements.

    :param float_list: float list
    :return: sum
    """
    pos_sum = 0
    for num in float_list:
        if num > 0:
            pos_sum += num
    return pos_sum
def multiplication(data):
    """
    Multiply the list elements located between the maximum and minimum absolute elements.

    :param data: list
    :return: multiplication
    """
    minimal_ind = data.index(min(data, key=abs))
    maximal_ind = data.index(max(data, key=abs))
    mul = 1
    if minimal_ind > maximal_ind:
        minimal_ind, maximal_ind = maximal_ind, minimal_ind
    for i in range(minimal_ind + 1, maximal_ind):
        mul *= data[i]
    if mul == 1:
        mul = 0
        return mul
    return mul
def print_list(data):
    """
    Print list.

    :param data: list
    :return: unpacked list
    """
    print(*data)
