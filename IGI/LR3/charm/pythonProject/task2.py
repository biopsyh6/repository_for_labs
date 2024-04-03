import user_input2


def solve_task():
    """
    Find the sum and find the number of even natural numbers.

    :return: sum, count of even natural numbers
    """
    lis = []
    even_natural_count = 0
    while True:
        number = user_input2.input_number()
        if number > 0 and number % 2 == 0:
            even_natural_count += 1
            lis.append(number)
        if number == 0:
            summ = sum(lis)
            break
    return summ, even_natural_count
