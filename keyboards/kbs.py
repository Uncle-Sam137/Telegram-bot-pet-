from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Главное меню с кнопками для разных игр и функций
menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Виселица', callback_data='visel'), InlineKeyboardButton(text='Волшебный шар', callback_data='shar')],
    [InlineKeyboardButton(text='Числовая угадайка', callback_data='ch_ug')],
    [InlineKeyboardButton(text='Де/Шифрование текста', callback_data='ces')],
    [InlineKeyboardButton(text='Генератор паролей', callback_data='gen_pas')],
    [InlineKeyboardButton(text='Какая сейчас погода?', callback_data='wether')],
])

# Клавиатура с возможностью вернуться в меню или начать игру заново
async def get_keyboard(state):
    posle_igr = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Заново', callback_data=state), InlineKeyboardButton(text='В меню', callback_data='to_menu')]
    ])
    return posle_igr