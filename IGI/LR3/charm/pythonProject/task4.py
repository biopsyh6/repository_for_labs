def check_string():
    """
    Analyze text.

    :return: number of words ending in a consonant, average word length, words with average length, message,
     every seventh word
    """
    word_count = 0
    all_sum = 0
    every_seventh_word = []
    count_every_seventh_word = 0
    message = ""
    text = ("So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and "
        "stupid, whether the pleasure of making a daisy-chain would be worth the trouble of "
        "getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.")
    text_list = text.split()
    for word in text_list:
        word = word.strip(",.-:;!?()[]{}")
        if word[-1].lower() not in ["a", "e", "i", "o", "u", "y"]:
            word_count += 1
        all_sum += len(word)
        count_every_seventh_word += 1
        if count_every_seventh_word == 7:
            every_seventh_word.append(word)
            count_every_seventh_word = 0
    average_length = int(all_sum / len(text_list))
    words_with_average_length = []
    for word in text_list:
        word = word.strip(",.-:;!?()[]{}")
        if len(word) == average_length:
            words_with_average_length.append(word)
    if len(words_with_average_length) == 0:
        message = f"Слов длиной {average_length} символов в строке нет"

    return word_count, average_length, words_with_average_length, message, every_seventh_word
