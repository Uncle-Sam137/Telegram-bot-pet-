import random
import asyncio

char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$&?@"


async def gen_parol(lenght):
    rezparol = ""
    for _ in range(4):

        if _ == 1:
            rezparol += char[random.randint(61, len(char) - 1)]

        elif _ == 2:
            rezparol += char[random.randint(9, 35)]
        elif _ == 3:
            rezparol += char[random.randint(35, 61)]
        else:
            rezparol += char[random.randint(0, 9)]

    for _ in range(lenght - len(rezparol)):
        rezparol += random.choice(char)
    return rezparol

