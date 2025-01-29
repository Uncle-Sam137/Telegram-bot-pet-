# Алфавиты для английского и русского языков (верхний и нижний регистры)
ENG_LOWER_ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ENG_UPPER_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
RUS_LOWER_ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
RUS_UPPER_ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def cezar_shifr(text: str, lang: str, shift: int, mode: str) -> str:
    """
    Функция для шифрования или дешифрования текста с помощью шифра Цезаря.

    :param text: строка текста, которую нужно зашифровать или расшифровать
    :param lang: язык текста ("ru" для русского, "en" для английского)
    :param shift: шаг сдвига для шифра
    :param mode: режим работы функции ("+" для шифрования, "-" для дешифрования)
    :return: зашифрованный или расшифрованный текст
    """

    # Инициализация переменных для результата и выбор алфавита в зависимости от языка
    rez = ""
    alphabet_lower = RUS_LOWER_ALPHABET if lang == "ru" else ENG_LOWER_ALPHABET
    alphabet_upper = RUS_UPPER_ALPHABET if lang == "ru" else ENG_UPPER_ALPHABET
    alphabet_len = len(alphabet_lower)  # Длина алфавита (для цикличности сдвига)

    # Если режим дешифрования, меняем знак сдвига
    if mode == "-":
        shift = -shift

    # Проходим по каждому символу текста
    for char in text:
        if char in "., -!?:":  # Пропуск знаков препинания, оставляем их без изменений
            rez += char
        elif char in alphabet_upper:  # Если символ из верхнего регистра
            index = alphabet_upper.index(char)  # Находим индекс буквы в алфавите
            rez += alphabet_upper[(index + shift) % alphabet_len]  # Применяем сдвиг, учитывая цикличность
        elif char in alphabet_lower:  # Если символ из нижнего регистра
            index = alphabet_lower.index(char)  # Находим индекс буквы в алфавите
            rez += alphabet_lower[(index + shift) % alphabet_len]  # Применяем сдвиг, учитывая цикличность
        else:
            rez += char  # Для символов вне алфавита (например, цифры) оставляем без изменений

    return rez
