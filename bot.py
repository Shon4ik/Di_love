import telebot
from telebot import types
import random
import sqlite3
from sms import photoDi, otmazka, sticker, podbadrivanie, happy
import time

bot = telebot.TeleBot('7711594368:AAElEdW38R6c3UN2u5eYZ1sbyBYNGTZn5Ck')

ALLOWED_USERS = {545582766, 438606276}
ADMIN_ID = 545582766

def access_check(func):
    def wrapper(message):
        if message.chat.id in ALLOWED_USERS:
            return func(message)
        else:
            bot.send_message(message.chat.id, "Иди отсюда вонючка.")
            return  # Прерываем выполнение, если доступ запрещен
    return wrapper

def init_db():
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            points INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def get_points(user_id):
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        points = result[0]
    else:
        points = 0
        cursor.execute('INSERT INTO users (user_id, points) VALUES (?, ?)', (user_id, points))
        conn.commit()

    conn.close()
    return points


@bot.message_handler(commands=['set_points'])
def set_points(message):
    if message.from_user.id == ADMIN_ID:  # Проверка на админа
        try:
            # Разбираем сообщение на части: команда /set_points <user_id> <points>
            _, user_id, points = message.text.split()

            # Преобразуем user_id и points в целые числа
            user_id = int(user_id)
            points = int(points)

            # Вызываем функцию для изменения баллов в базе данных
            change_points(user_id, points)

            # Отправляем сообщение, что баллы изменены
            bot.send_message(message.chat.id, f"Баллы для пользователя {user_id} изменены на {points}")
        except ValueError:
            bot.send_message(message.chat.id, "Неверный формат. Используй: /set_points <user_id> <points>")
    else:
        bot.send_message(message.chat.id, "Ты не администратор!")

def change_points(user_id, points):
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()

    # Вставляем или обновляем данные о пользователе и его баллах
    cursor.execute('''INSERT OR REPLACE INTO users (user_id, points) 
                      VALUES (?, ?)''', (user_id, points))

    conn.commit()
    conn.close()


@bot.message_handler(commands=['start'])
@access_check
def start(message):
    bot.send_message(message.chat.id, f'Привет! {message.from_user.first_name} \u2764\uFE0F')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Котик")
    btn2 = types.KeyboardButton("Порадуй меня")
    btn3 = types.KeyboardButton("Кто я?)")
    btn4 = types.KeyboardButton("Мне нужна подзарядка")
    btn5 = types.KeyboardButton("Покажи меня")
    btn6 = types.KeyboardButton("Заказ")
    btn7 = types.KeyboardButton("Магазин")
    keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(message.chat.id, "Выбирай, солнце) \u2764\uFE0F", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Магазин")
@access_check
def shop(message):
    user_id = message.from_user.id
    points = get_points(user_id)  # Получаем количество баллов пользователя
    bot.send_message(message.chat.id, "Добро пожаловать в мини-маркет)")
    time.sleep(1)

    bot.send_message(message.chat.id, "В данном разделе имеется возможность сделать заказ за так называемые баллы")
    time.sleep(1)

    bot.send_message(message.chat.id, "Баллы определяются администратором - мной)")
    time.sleep(1)

    bot.send_message(message.chat.id, "Эту валюту можно получать разными способами))))")
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAENZI5nbUAsyvVJWUSYQxc74FPcc4xFbgACCAADLNzcLCWvd09jKAfdNgQ')
    bot.send_message(message.chat.id, f"Ваши текущие баллы: {points}")


    shop_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Жамканье спинки")
    btn2 = types.KeyboardButton("Поцелуйчик")
    btn3 = types.KeyboardButton("Обнимашки")
    btn4 = types.KeyboardButton("Назад в меню")

    # Добавляем кнопки на клавиатуру
    shop_keyboard.add(btn1, btn2, btn3, btn4)

    # Отправляем клавиатуру пользователю
    bot.send_message(message.chat.id, "Выберите товар или вернитесь в меню:", reply_markup=shop_keyboard)

# Обработчики для товаров
@bot.message_handler(func=lambda message: message.text == "Жамканье спинки")
def handle_product_1(message):
    user_id = message.from_user.id
    points = get_points(user_id)  # Получаем текущие баллы пользователя

    price = 100  # Стоимость товара
    if points >= price:
        new_points = points - price
        change_points(user_id, new_points)
        bot.send_message(ADMIN_ID, f"Пользователь {message.from_user.first_name} (ID: {user_id}) купил Жамканье спинки.")# Обновляем количество баллов в базе
        bot.send_message(message.chat.id, f"Вы выбрали 'Жамканье спинки.'\n Стоимость: {price} баллов.\nБаллы списаны.\n Остаток: {new_points} баллов.")
    else:
        bot.send_message(message.chat.id, "У вас недостаточно баллов для покупки этого товара.")

@bot.message_handler(func=lambda message: message.text == "Поцелуйчик")
def handle_product_2(message):
    user_id = message.from_user.id
    points = get_points(user_id)  # Получаем текущие баллы пользователя

    price = 10  # Стоимость товара
    if points >= price:
        new_points = points - price
        change_points(user_id, new_points)
        bot.send_message(ADMIN_ID, f"Пользователь {message.from_user.first_name} (ID: {user_id}) купил Поцелуйчик.")# Обновляем количество баллов в базе
        bot.send_message(message.chat.id, f"Вы выбрали 'Поцелуйчик.'\nСтоимость: {price} баллов.\nБаллы списаны.\nОстаток: {new_points} баллов.")
    else:
        bot.send_message(message.chat.id, "У вас недостаточно баллов для покупки этого товара.")

@bot.message_handler(func=lambda message: message.text == "Обнимашки")
def handle_product_3(message):
    user_id = message.from_user.id
    points = get_points(user_id)  # Получаем текущие баллы пользователя

    price = 20  # Стоимость товара
    if points >= price:
        new_points = points - price
        change_points(user_id, new_points)
        bot.send_message(ADMIN_ID, f"Пользователь {message.from_user.first_name} (ID: {user_id}) купил Обнимашки.")# Обновляем количество баллов в базе
        bot.send_message(message.chat.id, f"Вы выбрали 'Обнимашки'\nСтоимость: {price} баллов.\nБаллы списаны.\nОстаток: {new_points} баллов.")
    else:
        bot.send_message(message.chat.id, "У вас недостаточно баллов для покупки этого товара.")


# Обработчик кнопки "Назад в меню"
@bot.message_handler(func=lambda message: message.text == "Назад в меню")
def go_back_to_main_menu(message):
    # Возвращаем пользователя в главное меню
    start(message)  # Вызываем функцию для старта, которая создает главное меню

@bot.message_handler(content_types=['text'])
@access_check
def handle_text(message):
    if message.text == 'Заказ':
        bot.send_message(message.chat.id, "Введите Ваш заказ)")
        bot.register_next_step_handler(message, forward_message_to_admin)
    elif message.text == "Котик":
        bot.send_message(message.chat.id, 'https://vk.com/id86960890')
    elif message.text == "Порадуй меня":
        bot.send_message(message.chat.id, random.choice(happy))
    elif message.text == 'Кто я?)':
        bot.send_sticker(message.chat.id, random.choice(sticker))
    elif message.text == 'Мне нужна подзарядка':
        bot.send_message(message.chat.id, random.choice(podbadrivanie))
    elif message.text == 'Покажи меня':
        bot.send_photo(message.chat.id, random.choice(photoDi), caption=random.choice(otmazka))
    return

def forward_message_to_admin(message):
    bot.send_message(ADMIN_ID, f"Сообщение от {message.from_user.first_name}:\n{message.text}")
    bot.send_message(message.chat.id, "Отправлено !")

# Инициализация базы данных при запуске бота
init_db()

bot.polling(True)
