import user_input1
import random
from Tasks.Task1 import serializer


class Abiturient:

    def __init__(self, surname, instrument, speciality):
        self.surname = surname
        self.instrument = instrument
        self.speciality = speciality

    def __str__(self):
        return f"{self.surname}, {self.instrument}, {self.speciality}"

class Task1:
    def __init__(self):
        self.data = []

    def add_abiturient(self, surname, instrument, speciality):
        """
        Add abiturient
        :param surname:
        :param instrument:
        :param speciality:
        :return:
        """
        abiturient = Abiturient(surname, instrument, speciality)
        self.data.append(abiturient)

    def solve(self):
        """
        Solve this task
        :return:
        """
        self.data_input()
        self.write_to_files()
        data1 = serializer.Serializer.deserialize_from_csv("task1.csv")
        data2 = serializer.Serializer.deserialize_from_pickle("task1.pickle")

        specialities = set([abiturient["speciality"] for abiturient in self.data])
        print("Список абитуриентов в зависимости от специальности:")
        for speciality in specialities:
            print(f"Специальность: {speciality}")
            for abiturient in data2:
                if abiturient["speciality"] == speciality:
                    print(f"{abiturient["surname"]} - {abiturient["instrument"]}")
            print()

        surname = input("Введите фамилию для вывода информации: ")
        result = [item for item in data2 if item["surname"] == surname]
        for item in result:
            print(item["surname"], item["instrument"], item["speciality"], sep='\n')

    def write_to_files(self):
        """
        Serialization to files
        :return:
        """
        serializer.Serializer.serialize_to_csv("task1.csv", self.data)
        serializer.Serializer.serialize_to_pickle("task1.pickle", self.data)

    def data_input(self):
        """
        Data initialization
        :return:
        """
        choose = user_input1.choose_way()
        if choose == 1:
            for i in range(5):
                surname = input("Введите фамилию: ")
                instrument = input("Введите инструмент: ")
                speciality = input("Введите специальность: ")
                self.data.append({"surname": surname, "instrument": instrument, "speciality": speciality})
        else:
            surnames = ["Smith", "Agustin", "Evans", "Stone", "Morgan", "Peters", "Jackson", "Grant", "Bradley",
                        "Barlow", "Collins", "Jordan", "Williams", "Bronte", "Adams"]
            instruments = ["Accordion", "Bagpipe", "Balalaika", "Cello", "Clarinet", "Cymbals", "Grand piano"]
            specialities = ["Musical education", "Music theory", "Instrumental performance", "Instruments of the folk's orchestra"]
            for i in range(5):
                random.shuffle(surnames)
                random.shuffle(instruments)
                random.shuffle(specialities)
                self.data.append({"surname": surnames[0], "instrument": instruments[0], "speciality": specialities[0]})