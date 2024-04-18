import csv
import pickle


class Serializer:
    @staticmethod
    def serialize_to_csv(file_path, data):
        """
        Serializes data to csv file
        :param file_path:
        :param data:
        :return:
        """
        try:
            with open(file_path, "w", newline="") as file:
                columns = ["surname", "instrument", "speciality"]
                writer = csv.DictWriter(file, fieldnames=columns)
                writer.writeheader()
                writer.writerows(data)
        except FileNotFoundError as e:
            print(f"Ошибка: {e}")

    @staticmethod
    def deserialize_from_csv(file_path):
        """
        Deserializes data from csv file
        :param file_path:
        :return: data
        """
        data = []
        try:
            with open(file_path, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
            return data
        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            return None

    @staticmethod
    def serialize_to_pickle(file_path, data):
        """
        Serializes data to pickle file
        :param file_path:
        :param data:
        :return:
        """
        try:
            with open(file_path, "wb") as file:
                pickle.dump(data, file)
        except FileNotFoundError as e:
            print(f"Ошибка: {e}")

    @staticmethod
    def deserialize_from_pickle(file_path):
        """
        Deserializes data from pickle file
        :param file_path:
        :return:
        """
        try:
            with open(file_path, "rb") as file:
                data = pickle.load(file)
            return data
        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            return None

