eng_lower_alphabet = "abcdefghijklmnopqrstuvwxyz"
eng_upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
rus_lower_alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
rus_upper_alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def cezar_shifr(text: str, lang: str, shift: int, mode: str) -> str:
    rez = ""
    alphabet_lower = rus_lower_alphabet if lang == "ru" else eng_lower_alphabet
    alphabet_upper = rus_upper_alphabet if lang == "ru" else eng_upper_alphabet
    alphabet_len = len(alphabet_lower)

    if mode == "-":
        shift = -shift

    for char in text:
        if char in "., -!?:":  # Пропуск знаков препинания
            rez += char
        elif char in alphabet_upper:
            index = alphabet_upper.index(char)
            rez += alphabet_upper[(index + shift) % alphabet_len]
        elif char in alphabet_lower:
            index = alphabet_lower.index(char)
            rez += alphabet_lower[(index + shift) % alphabet_len]
        else:
            rez += char  # Для символов вне алфавита (например, цифры)

    return rez
