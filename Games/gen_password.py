import random

# Доступные символы для пароля
char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$&?@"


# Асинхронная функция для генерации пароля
def gen_parol(length: int) -> str:
    password = ""

    # Добавляем поочередно символы разных категорий, для соответствия большинства требований при создании пароля
    for i in range(4):
        if i == 1:
            # Добавляем символ из верхнего регистра или спецсимволов
            password += char[random.randint(61, len(char) - 1)]
        elif i == 2:
            # Добавляем символ из цифр
            password += char[random.randint(9, 35)]
        elif i == 3:
            # Добавляем символ из строчных букв
            password += char[random.randint(35, 61)]
        else:
            # Добавляем символ из цифр
            password += char[random.randint(0, 9)]

    # Заполняем оставшуюся длину пароля случайными символами
    for _ in range(length - len(password)):
        password += random.choice(char)

    # Возвращаем результат
    return password
