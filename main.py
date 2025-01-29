import random
import asyncio

from aiogram import Dispatcher, Bot, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

import config
from Games import ugaday_slova, ugaday_shislo, cezar, gen_password, wether_parse
from keyboards import kbs

dp = Dispatcher()


class States(StatesGroup):
    visel_state = State()
    shar_state = State()
    ch_ug_state = State()
    ces_state = State()
    gen_pas_state = State()
    wether_state = State()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Привет, <b>{message.from_user.full_name}</b>! 👋 Я твой универсальный помощник!\n\n"
            f"✨Вот что я умею:\n"
            f"🎮 Игры: сыграй в увлекательные игры.\n"
            f"☀️ Прогноз погоды: узнай погоду в любом городе мира.\n"
            f"🔒 Шифрование и дешифрование текста: сохраняй свои данные в безопасности.\n"
            f"🔑 Генерация паролей: создай надёжные пароли для твоих аккаунтов.\n\n"
            f"Как пользоваться:\n"
            f"Все доступные функции находятся на кнопках ниже ⬇️. Просто нажми на нужную!",

        parse_mode='HTML', reply_markup=kbs.menu
    )






@dp.callback_query(F.data == 'visel')
async def visel(callback: CallbackQuery, state: FSMContext):
    word = ugaday_slova.chooseword()  # Генерируем слово
    await state.set_state(States.visel_state)
    await state.update_data(word=word, tries=6, guessed_letters=[], display_word=["_" for _ in word])
    await callback.message.answer(f'🎮 Добро пожаловать в игру "Виселица"!\n'
                                     f'Задача: угадать слово по буквам.\n\n'
                                     f'📜 Правила игры:\n'
                                     f'1️⃣ Я загадаю слово, и ты будешь видеть количество букв в нём в виде прочерков (например: _ _ _ _ _).\n'
                                     f'2️⃣ У тебя будет ограниченное количество попыток, а именно 6.\n'
                                     f'3️⃣ Если ты угадываешь букву, она появляется на своём месте в слове.\n'
                                     f'4️⃣ Если ты ошибаешься, у тебя уменьшается количество попыток.\n\n'
                                     f'❗ Как играть:\n'
                                     f'Просто напиши букву в чат.')



@dp.message(States.visel_state)
async def visel_class(message: Message, state: FSMContext):
    result = await ugaday_slova.play(message.text, state)

    if result[:2] in ['Вы', 'По']:
        await state.clear()
        await message.answer(result, reply_markup= await kbs.get_keyboard('visel'))
    else:
        await message.answer(result)


@dp.callback_query(F.data == 'shar')
async def shar(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.shar_state)
    await callback.message.answer(f'🎱 Добро пожаловать в игру "Волшебный шар"!\n\n'
                                     f'🔮 Как играть:\n'
                                     f'1️⃣ Задай любой вопрос, на который можно ответить "да" или "нет".\n'
                                     f'2️⃣ Напиши свой вопрос в чат.\n'
                                     f'3️⃣ Я дам вам загадочный и мудрый ответ!\n\n'
                                     f'✨ Пример вопросов:\n\n'
                                     f'«Сбудется ли моё желание?»\n'
                                     f'«Стоит ли мне пойти в отпуск?»\n'
                                     f'«Увижу ли я сегодня радугу?»\n\n'
                                     f'💫 Напиши свой вопрос, и давай посмотрим, что скажет волшебный шар!')


# Пупупу - хихи хаха
@dp.message(States.shar_state)
async def shar_class(message: Message, state: FSMContext):
    sp = [
        "Бесспорно",
        "Предрешено",
        "Никаких сомнений",
        "Определённо да",
        "Можешь быть уверен в этом",
        "Мне кажется - да",
        "Вероятнее всего",
        "Хорошие перспективы",
        "Знаки говорят - да",
        "Да",
        "Пока неясно, попробуй снова",
        "Спроси позже",
        "Лучше не рассказывать",
        "Сейчас нельзя предсказать",
        "Сконцентрируйся и спроси опять",
        "Даже не думай",
        "Мой ответ - нет",
        "По моим данным - нет",
        "Перспективы не очень хорошие",
        "Весьма сомнительно",
    ]
    await  state.clear()
    await message.answer(random.choice(sp), parse_mode='HTML', reply_markup= await kbs.get_keyboard('shar'))


@dp.callback_query(F.data == 'ch_ug')
async def ch_ug(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.ch_ug_state)
    x = random.randint(1, 100)
    await state.update_data(iskomoe=x, tries=0)
    await callback.message.answer(f'🎮 Добро пожаловать в игру "Числовая угадайка"!\n\n'
                                  f'🔢 Я загадал число от 1 до 100. Твоя задача — угадать его!\n\n'
                                  f'📜 Правила игры:\n'
                                  f'1️⃣ Ты будешь вводить числа.\n'
                                  f'2️⃣ Я скажу, если твоё число больше или меньше загаданного.\n'
                                  f'3️⃣ Попробуй угадать, сколько попыток тебе потребуется!\n\n'
                                  f'Начни угадывать! Напиши своё первое число.')


@dp.message(States.ch_ug_state)
async def ch_ug_class(message: Message, state: FSMContext):
    rez = await ugaday_shislo.play(message.text, state)

    data = await state.get_data()
    x = data.get('tries')
    if rez[:2] == '🎉 ':
        rez = rez + f'\nТебе понадобилось {x} попыток'
        await state.clear()
        await message.answer(rez, reply_markup= await kbs.get_keyboard('ch_ug'))
    else:
        await message.answer(rez)


@dp.callback_query(F.data == 'ces')
async def ces(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.ces_state)
    await callback.message.answer('🔓В этом разделе ты можешь шифром Цезаря расшифровать или зашифровать текст.\n'
                                  'Для начала, мы шифруем текст?\n'
                                  'Введи + или -')


@dp.message(States.ces_state)
async def ces_class(message: Message, state: FSMContext):
    data = await state.get_data()
    step = data.get('step', 1)

    # Шаг 1: Выбор режима (+ или -)
    if step == 1:
        if message.text in '+-':
            await state.update_data(mode=message.text, step=2)
            await message.answer("📚На каком языке текст?\nВведи `ru` для русского или `en` для английского.")
        else:
            await message.answer("❗️ Введи корректное значение: `+` или `-`.")

    # Шаг 2: Выбор языка (ru или en)
    elif step == 2:
        if message.text.lower() in ['ru', 'en']:
            await state.update_data(lang=message.text.lower(), step=3)
            await message.answer("🔑Введи ключ/шаг сдвига (положительное число):")
        else:
            await message.answer("❗️ Введи корректное значение: `ru` или `en`.")

    # Шаг 3: Указание шага сдвига
    elif step == 3:
        if message.text.isdigit():
            await state.update_data(shift=int(message.text), step=4)
            await message.answer("📝Введи текст для шифровки/расшифровки (на выбранном языке):")
        else:
            await message.answer("❗️ Введи корректное число для шага сдвига.")

    # Шаг 4: Шифрование текста
    elif step == 4:
        data = await state.get_data()
        mode = data['mode']
        lang = data['lang']
        shift = data['shift']
        text = message.text

        # Шифруем текст
        result = cezar.cezar_shifr(text, lang, shift, mode)

        await message.answer(f"Результат:\n{result}", reply_markup=await kbs.get_keyboard('ces'))
        await state.clear()  # Сбрасываем состояние


@dp.callback_query(F.data == 'gen_pas')
async def gen_pas(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.gen_pas_state)
    await callback.message.answer(f'Скоро получишь свой пароль! 🔐\n\n'
                                  f'Для начала напиши, какой длины тебе нужен пароль(число).\n'
                                  f'<strong>Важно:</strong> Пароль должен быть не менее 9 символов для безопасности.\n\n'
                                  f'Как только укажешь длину пароля, я создам его для тебя! ✨', parse_mode='HTML')


@dp.message(States.gen_pas_state)
async def gen_pas_class(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer('Введите корректное число')
    elif int(message.text) < 9:
        await message.answer('Число не менее 9')
    else:
        rez = await gen_password.gen_parol(int(message.text))
        await state.clear()
        await message.answer(rez, reply_markup= await kbs.get_keyboard('gen_pas'))


@dp.callback_query(F.data == 'wether')
async def wether(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.wether_state)
    await callback.message.answer('🌍Захотел прогуляться? \n🌤️Хорошая идея, давай узнаем, что там твориться за окном\n'
                                  'Напиши название города, чтобы я мог показать тебе погоду.\n\n'
                                  'Примеры:\n📍 Москва\n📍 Париж\n📍 Токио\n\n'
                                  'Порой сервис бывает загружен и придется немного подождать ответа')

@dp.message(States.wether_state)
async def wether_class(message: Message, state: FSMContext):
    rez = wether_parse.wether_prs(message.text)

    await message.answer(rez, reply_markup= await kbs.get_keyboard('wether'))


@dp.callback_query(F.data == 'to_menu')
async def visel(callback: CallbackQuery):
    await callback.message.answer(f"Вы снова в главном меню! 🚀\n"
                                     f"Выберите нужную функцию с помощью кнопок ниже:", parse_mode='HTML', reply_markup=kbs.menu)


async def main():
    bot = Bot(config.token)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
