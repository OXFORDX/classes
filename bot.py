import telebot
from telebot import types
import random
import os
import pydatabase
import teleuser

token = '958037621:AAFB5ZOCMgVKo_7pQbifvqnQm0Oc4GxMthU'
bot = telebot.TeleBot(token)


def create_file(file):
    with open(file, 'w') as f:
        pass


@bot.message_handler(commands=['start'])
def start(message):
    user = teleuser.Session(message.chat.id)
    bot.send_message(message.chat.id, 'Привіт!', reply_markup=keys())
    user.writestate(message.text)


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = message.document.file_name
    file = src.split('.')[0] + str(random.randint(0, 10)) + '.xlsx'
    create_file(file)
    with open(message.chat.id, 'wb') as new_file:
        new_file.write(downloaded_file)


@bot.message_handler(content_types=['text'])
def mess(message):
    stds = pydatabase.getNamesOfSTD()
    user = teleuser.Session(message.chat.id)
    if user.data["prev_msg"] and user.data["prev_msg"] in 'Кабінет студента' and message.text in stds:
        bot.send_message(message.chat.id, 'Введіть пароль: ')
        user.writename(message.text)

    if user.data['prev_msg'] == user.data['name']:
        bot.send_message(message.chat.id, f'Вітаємо, {message.text}', reply_markup=std_keys())
        user.writestate(0)

    if message.text == 'Кабінет студента':
        user.writestate(0)
        bot.send_message(message.chat.id, "Введіть ваше ім'я")
    #
    if message.text == 'Кабінет викладача':
        print(message.text)
        bot.send_message(message.chat.id, 'Кабінет викладача', reply_markup=lectr_keys())
    #
    if message.text == 'Назад':
        user.writestate(None)
        bot.send_message(message.chat.id, 'Меню', reply_markup=keys())
    #
    if message.text == 'Отримати оцінки' and user.data['state'] == 0:
        std = pydatabase.Database(user.data['name'])
        bot.send_message(message.chat.id, std.excelDBwrite())
    user.writemess(message.text)
    user.close()


def keys():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Кабінет студента')
    btn2 = types.KeyboardButton('Кабінет викладача')
    btn3 = types.KeyboardButton('Кабінет декаанату')
    btn4 = types.KeyboardButton('Отримати довідку')
    markup.add(btn1, btn2, btn3, btn4)
    return markup


def std_keys():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Отримати оцінки')
    btn2 = types.KeyboardButton('Назад')
    markup.add(btn1, btn2)
    return markup


def lectr_keys():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Добавити оцінку')
    btn2 = types.KeyboardButton('Назад')
    btn3 = types.KeyboardButton('Отримати оцінки')
    markup.add(btn1, btn3, btn2)
    return markup


def dov_keys():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Студент')
    btn2 = types.KeyboardButton('Викладач')
    btn3 = types.KeyboardButton('Назад')
    markup.add(btn1, btn2, btn3)
    return markup


bot.polling()
