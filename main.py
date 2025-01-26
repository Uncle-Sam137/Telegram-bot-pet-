import random
import asyncio

from aiogram import Dispatcher, Bot, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from Games import ugaday_slova, ugaday_shislo, cezar, gen_password
from keyboards import kbs

dp = Dispatcher()


class States(StatesGroup):
    visel_state = State()
    shar_state = State()
    ch_ug_state = State()
    ces_state = State()
    gen_pas_state = State()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"<b>{message.from_user.full_name}</b>, добро пожаловать!\nЭтот бот много чего умеет",
        parse_mode='HTML', reply_markup=kbs.menu
    )


@dp.callback_query(F.data == 'visel')
async def visel(callback: CallbackQuery, state: FSMContext):
    word = ugaday_slova.chooseword()  # Генерируем слово
    await state.set_state(States.visel_state)
    await state.update_data(word=word, tries=6, guessed_letters=[], display_word=["_" for _ in word])
    await callback.message.edit_text("Игра началась! Введите букву.")


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
    await callback.message.edit_text('Привет, я магический шар, и я знаю ответ на любой твой вопрос.\nСпрашивай, что хочешь. Но ответ будет только да или нет ... А на, что ты расчитывал от меня?')

# Пупупупу - хихи хаха
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
    await message.answer(random.choice(sp), parse_mode='HTML', reply_markup= await kbs.get_keyboard('shar'))


@dp.callback_query(F.data == 'ch_ug')
async def ch_ug(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.ch_ug_state)
    x = random.randint(1, 2)
    await state.update_data(iskomoe=x, tries=0)
    await callback.message.answer(f'Введите число от {1} до {100}')


@dp.message(States.ch_ug_state)
async def ch_ug_class(message: Message, state: FSMContext):
    rez = await ugaday_shislo.play(message.text, state)

    data = await state.get_data()
    x = data.get('tries')
    if rez[:2] == 'Вы':
        rez = rez + f'\nВам понадобилось {x} попыток'
        await state.clear()
        await message.answer(rez, reply_markup= await kbs.get_keyboard('ch_ug'))
    else:
        await message.answer(rez)


@dp.callback_query(F.data == 'ces')
async def ces(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.ces_state)
    await callback.message.answer('В этом разделе ты можешь расшифровать или зашифровать текст, шифром Цезаря.\n'
                                  'Для начала, мы шифруем или расшифровываем текст?\n'
                                  'Введи + или -')


@dp.message(States.ces_state)
async def ces_class(message: Message, state: FSMContext):
    data = await state.get_data()
    step = data.get('step', 1)

    # Шаг 1: Выбор режима (+ или -)
    if step == 1:
        if message.text in '+-':
            await state.update_data(mode=message.text, step=2)
            await message.answer("На каком языке текст?\nВведите `ru` для русского или `en` для английского.")
        else:
            await message.answer("Введите корректное значение: `+` или `-`.")

    # Шаг 2: Выбор языка (ru или en)
    elif step == 2:
        if message.text in ['ru', 'en']:
            await state.update_data(lang=message.text, step=3)
            await message.answer("Введите шаг сдвига (число):")
        else:
            await message.answer("Введите корректное значение: `ru` или `en`.")

    # Шаг 3: Указание шага сдвига
    elif step == 3:
        if message.text.isdigit():
            await state.update_data(shift=int(message.text), step=4)
            await message.answer("Введите текст для шифрования/расшифровки:")
        else:
            await message.answer("Введите корректное число для шага сдвига.")

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
    await callback.message.answer('В это разделе ты можешь сгенерировать надежный пароль\n'
                                  'Введи желаемую длину пароля, но не менее 9 символов, иначе такой короткий пароль никуда не подойдет')


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


@dp.callback_query(F.data == 'to_menu')
async def visel(callback: CallbackQuery):
    await callback.message.edit_text(f"Что еще хочешь поделать?", parse_mode='HTML', reply_markup=kbs.menu)


async def main():
    bot = Bot(token='7625823488:AAHMSGgnYffER6t6jzMX32E4XheLk5tQmyU')
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
