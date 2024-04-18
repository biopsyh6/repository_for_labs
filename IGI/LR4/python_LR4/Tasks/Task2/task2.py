import re
import user_input2
from Tasks.Task2.FileService import FileService


class Task2:
    def __init__(self):
        self.text_data = ""

    def solve(self):
        result = ""
        self.read_text_file()
        povest, pobud, vopr = self.analyze_sentences_types(self.text_data)
        result += f"В тексте {povest + pobud + vopr} предложений.\n"
        result += f"Повествовательных: {povest}.\n"
        result += f"Побудительных: {pobud}.\n"
        result += f"Вопросительных: {vopr}.\n"
        avg_len_sentence = self.get_average_length_sentence(self.text_data)
        result += f"Средняя длина предложения: {avg_len_sentence}.\n"
        avg_len_word = self.get_average_length_word(self.text_data)
        result += f"Средняя длина слова: {avg_len_word}.\n"
        count_emoj = self.get_smiles_count(self.text_data)
        result += f"Количество смайликов: {count_emoj}.\n"
        length = user_input2.input_number()
        text = self.replace_last_three_chars(self.text_data, length)
        result += f"Текст с заменой на $ \n{text}\n"
        s = input("Введите строку, где будет присутствовать время:\n")
        times = Task2.find_time(s)
        result += f"Найденное время в строке: {times}\n"
        count_words_with_max_length = Task2.count_words_with_max_length(s)
        result += f"Количество слов с максимальной длинной: {count_words_with_max_length}.\n"
        words_with_dots_after = Task2.words_with_dots_after(s)
        result += f"Слова, за которыми следует запятая или точка:\n{words_with_dots_after}\n"
        longest_word_with_e = Task2.longest_word_with_e(s)
        result += f"Самое длинное слово, которое заканчивается на 'е': {longest_word_with_e}\n"
        print(result)
        FileService.save_to_file("Task2_answer", result)
        FileService.archive_file("Task2_answer", "Task2archive.zip")
        FileService.get_archive_info("Task2archive.zip")



    def read_text_file(self, file_path="task2_data.txt"):
        """
        Read file
        :param file_path:
        :return: readed data
        """
        try:
            with open(file_path, 'r') as file:
                self.text_data = file.read()
        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            return None

    def regex_count(self, reg, text=""):
        """
        Get coincidence by regex pattern
        :param reg:
        :param text:
        :return: matches
        """
        if text == "":
            text = self.text_data
        matches = re.findall(reg, text)
        return matches

    def analyze_sentences_types(self, text):
        """
        Get narrative, incentive and interrogative sentences
        :param text:
        :return: sentences
        """
        povest = len(re.findall(r"\.{3,}|\.(\s|$)", text))
        pobud = len(re.findall(r"\!{3,}|\!(\s|$)", text))
        vopr = len(re.findall(r"\?{3,}|\?(\s|$)", text))
        return povest, pobud, vopr

    @staticmethod
    def get_average_length_sentence(text):
        """
        Average sentence length
        :param text:
        :return: length
        """
        sentences = re.findall(r"([^!?.]+)(\!|\?|\.{3,}|\.)", text)
        sentences_len = 0
        for sent in sentences:
            words = re.findall(r"\b[A-z]+\b", str(sent))
            flag = True
            for word in words:
                if word[0] == "n" and flag:
                    word = word[1:]
                flag = False
                sentences_len += len(word)
        return round(sentences_len / len(sentences))

    @staticmethod
    def get_words(text):
        """
        Get list with words in text
        :param text:
        :return: words list
        """
        return re.findall(r"\b[A-z]+\b", text)

    @staticmethod
    def get_average_length_word(text):
        """
        Average word length
        :param text:
        :return: length
        """
        words = Task2.get_words(text)
        words_len = 0
        for word in words:
            words_len += len(word)
        avg_len_word = round(words_len / len(words))
        return avg_len_word

    @staticmethod
    def get_smiles_count(text):
        """
        Get smiles count
        :param text:
        :return: count
        """
        return len(re.findall(r"(;|:)(\-*)(\(+|\)+|\[+|\]+)", text))

    @staticmethod
    def replace_last_three_chars(text, length):
        """
        Replace last three chars in word
        :param text:
        :param length:
        :return: updated text
        """
        pattern = r"\b(\w{" + str(length) + r"})\b"
        processed_text = re.sub(pattern, lambda match: match.group(1)[:-3] + "$", text) #Передаем совпадение в match
        return processed_text

    @staticmethod
    def find_time(text):
        """
        Find time in sentence
        :param text:
        :return: formatted_times
        """
        pattern = r"\b([01]\d|2[0-3]):([0-5]\d)\b"
        times = re.findall(pattern, text)
        formatted_times = [time[0] + ":" + time[1] for time in times]
        return formatted_times

    @staticmethod
    def count_words_with_max_length(text):
        """
        Count words with max length
        :param text:
        :return: count
        """
        words = re.findall(r"\b\w+\b", text)
        max_length = max(len(word) for word in words)
        max_length_words = [word for word in words if len(word) == max_length]
        return len(max_length_words)

    @staticmethod
    def words_with_dots_after(text):
        """
        Get words with dots after
        :param text:
        :return: words
        """
        pattern = r"\b\w+(?=,|\.)"
        words = re.findall(pattern, text)
        return words

    @staticmethod
    def longest_word_with_e(text):
        """
        Get the longest word with e at the end of word
        :param text:
        :return: word
        """
        pattern = r"\b\w+e\b"
        words = re.findall(pattern, text)
        if words:
            longest_word = max(words, key=len)
            return longest_word
        else:
            return "Слово отсутствует.\n"
