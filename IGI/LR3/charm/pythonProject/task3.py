def check_punctuation(text):
    """
    Analyze text.

    :param text: text
    :return: number of punctuation marks
    """
    count = 0
    flag_point = False
    open_brackets = {"(": 0, "[": 0, "{": 0, "'": 0}
    for letter in text:
        if letter not in [",", ":", ";", "-", "!", "?", "(", ")", "'", ".", "{", "}", "[", "]"]:
            flag_point = False
        if letter == ".":
            if flag_point:
                continue
            count += 1
            flag_point = True
        if letter in [",", ":", ";", "-", "!", "?"]:
            count += 1
            flag_point = False
        if letter in ["(", "[", "{", "'"]:
            open_brackets[letter] += 1
        if letter in [")", "]", "}", "'"]:
            matching_bracket = "(" if letter == ")" else "[" if letter == "]" else "{" if letter == "}" else "'"
            if open_brackets[matching_bracket] > 0:
                open_brackets[matching_bracket] -= 1
                count += 1
    return count
