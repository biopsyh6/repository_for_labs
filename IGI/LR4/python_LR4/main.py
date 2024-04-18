import user_input
from Tasks.Task3.task3 import Task3
from Tasks.Task1.task1 import Task1
from Tasks.Task2.task2 import Task2
from Tasks.Task4.task4 import Task4
from Tasks.Task5.task5 import Task5
# Program that solves problems in laboratory work.
# Laboratory work 4. "Working with files, classes, serializers, regular expressions and standard libraries.".
# Version 1.
# Kolesnikov Pavel Vladimirovich.
# 16.04.2024
table = []
while True:
    task = user_input.choose_task()
    match task:
        case 1:
            task1 = Task1()
            task1.solve()
        case 2:
            task2 = Task2()
            task2.solve()
        case 3:
            Task3.solve()
        case 4:
            task4 = Task4()
            task4.solve()
        case 5:
            task5 = Task5()
            task5.solve()
        case 0:
            print("Программа завершена.")
            break
        case _:
            print("Неверный номер задания. Выберите существующее задание.")



