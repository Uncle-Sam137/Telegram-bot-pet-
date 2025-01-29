import aiosqlite
from datetime import datetime


# Проверка через базу данных, впервые ли пользователь пользуется ботом
async def check_db(user_id, full_name, user_name):
    # Открываем асинхронное соединение с базой данных
    async with aiosqlite.connect('users.db') as connect:
        async with connect.cursor() as cursor:
            # Проверяем, есть ли уже пользователь с таким user_id
            await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            check_user = await cursor.fetchone()

            # Если пользователь не найден, добавляем его в базу
            if check_user is None:
                # Получаем текущую дату и время
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

                # Вставляем нового пользователя в таблицу
                await cursor.execute(
                    'INSERT INTO users (user_id, full_name, date, user_name) VALUES (?, ?, ?, ?)',
                    (user_id, full_name, current_time, user_name)
                )
                # Сохраняем изменения в базе данных
                await connect.commit()

                return False  # Пользователь был добавлен
            else:
                # Если пользователь найден, возвращаем True
                return True  # Пользователь уже существует


import aiosqlite


async def list_users():
    # Открываем соединение с базой данных
    async with aiosqlite.connect('users.db') as connect:
        # Создаем курсор для выполнения SQL-запросов
        async with connect.cursor() as cursor:
            # Выполняем запрос для извлечения данных пользователей
            await cursor.execute('SELECT ID, full_name, date, user_name FROM users')

            # Извлекаем все строки результата запроса
            users = await cursor.fetchall()

            # Преобразуем результат в строку, соединяя данные пользователей
            users_str = '\n'.join([', '.join(map(str, user)) for user in users])

            return users_str
