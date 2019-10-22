import telebot
from telebot import types
import random
import os
import pydatabase
import teleuser
import classes
import pandas as pd

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
    user = teleuser.Session(message.chat.id)
    lectr = classes.Teacher(user.data['name'])
    db = pydatabase.Database()
    src = message.document.file_name
    if user.data['state'] == 1 and '.xlsx' in src:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"temp/{user.data['group']}/{lectr.subject}.xlsx", 'wb') as new_file:
            new_file.write(downloaded_file)
        db.excelDBread(user.data['group'], lectr.subject)
        bot.send_message(message.chat.id, 'Дані записані в базу')
    if user.data['state'] == 2 and '.xlsx' in src:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        x = open(f"temp/tempxlsx.xlsx", 'w')
        x.close()
        with open(f"temp/tempxlsx.xlsx", 'wb') as new_file:
            new_file.write(downloaded_file)
        db.addStd()
        bot.send_message(message.chat.id, 'Студента додано.')


@bot.message_handler(content_types=['text'])
def mess(message):
    try:
        stds = pydatabase.getNamesOfSTD()
        lectr = pydatabase.getNamesOfTeach()
        user = teleuser.Session(message.chat.id)
        print(message.text)
        print(user.data['prev_msg'])

        if message.text == 'Logout':
            user.writestate(None)
            bot.send_message(message.chat.id, 'Меню', reply_markup=keys())

        if user.data["prev_msg"] and user.data["prev_msg"] in 'Кабінет студента' and message.text:
            mess = message.text.split(',')
            data = pydatabase.getpasswdstd()
            if mess[0] in stds and mess[1] == data[mess[0]]:
                bot.send_message(message.chat.id, f'Вітаємо, {mess[0]}', reply_markup=std_keys())
                user.writestate(0)
                user.writename(mess[0])
            else:
                bot.send_message(message.chat.id, "Невірне ім'я чи пароль")

        if user.data["prev_msg"] and user.data["prev_msg"] in 'Кабінет викладача':
            mess = message.text.split(',')
            data = pydatabase.getpasswdteach()
            if mess[0] in lectr and mess[1] == data[mess[0]]:
                bot.send_message(message.chat.id, f'Вітаємо, {mess[0]}', reply_markup=lectr_keys())
                user.writestate(1)
                user.writename(mess[0])
        if message.text == 'Змінити оцінки' and user.data['state'] == 1:
            bot.send_message(message.chat.id, 'Вкажіть групу:')

        if 'IP' in message.text and user.data['state']:
            try:
                user.data['group'] = message.text
                peopl = classes.Teacher(user.data['name'])
                peopl.changeMarks(message.text)
                with open(f'temp/{message.text}/{peopl.subject}.xlsx', 'rb') as doc:
                    bot.send_document(message.chat.id, doc)
                    bot.send_message(message.chat.id,
                                     'Відредагуйте цей документ і надішліть його цьому боту. Міняти можна тільки оцінки!')
            except:
                bot.send_message(message.chat.id, 'Такої групи не існує')

        if message.text == 'Кабінет студента':
            bot.send_message(message.chat.id, """Введіть ваше ім'я і пароль у форматі: \n"Фамілія Ім'я,пароль" """)
        #
        if message.text == 'Кабінет викладача':
            bot.send_message(message.chat.id, """Введіть ваше ім'я і пароль у форматі: \n"Фамілія Ім'я,пароль" """)

        if message.text == 'Кабінет деканату':
            bot.send_message(message.chat.id, 'Введіть пароль до входу в деканат:')

        if user.data['prev_msg'] == 'Кабінет деканату' and message.text == 'timehascome':
            user.data['state'] = 2
            bot.send_message(message.chat.id, 'Вітаємо в кабінеті деканату.', reply_markup=dean_keys())

        if message.text == 'Пошук студента' and user.data['state'] == 2:
            bot.send_message(message.chat.id, "Введіть фамілію і ім'я студента")

        if message.text == 'Добавити студента' and user.data['state'] == 2:
            with open('temp/stds/Some_std.xlsx', 'rb') as doc:
                bot.send_document(message.chat.id, doc)
                bot.send_message(message.chat.id,
                                 'Відредагуйте цей документ і надішліть його цьому боту. Редагувати дозволено тільки 2 колонку!')

        if user.data['prev_msg'] == 'Пошук студента' and user.data['state'] == 2:
            db = pydatabase.Database()
            bot.send_message(message.chat.id, db.StdInfo(message.text))

        if message.text == 'Видалити студента' and user.data['state'] == 2:
            bot.send_message(message.chat.id, "Введіть фамілію і ім'я студента")

        if user.data['prev_msg'] == 'Видалити студента' and user.data['state'] == 2:
            db = pydatabase.Database()
            db.del_std(message.text)
            bot.send_message(message.chat.id, 'Успіх!')

        if message.text == 'Змінити курс студента' and user.data['state'] == 2:
            bot.send_message(message.chat.id, "Введіть дані: 'Фамілія і ім'я,курс")

        if user.data['prev_msg'] == 'Змінити курс студента' and user.data['state'] == 2 and ',' in message.text:
            db = pydatabase.Database()
            d = message.text.split(',')
            std = d[0]
            course = d[1]
            db.changeCourse(std, course)

        if message.text == 'Отримати довідку':
            if user.data['state'] == 0:
                foto = open('Certificates/dov2.jpg', 'rb')
                bot.send_photo(message.chat.id, foto)
            else:
                foto = open('Certificates/dov1.jpg', 'rb')
                bot.send_photo(message.chat.id, foto)
        #

        #
        if message.text == 'Отримати оцінки' and user.data['state'] == 0:
            std = pydatabase.Database(user.data['name'])
            bot.send_message(message.chat.id, std.excelDBwrite())
        user.writemess(message.text)
        user.close()
    except:
        bot.send_message(message.chat.id, 'Попробуйте ще раз.')


def keys():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton('Кабінет студента')
    btn2 = types.KeyboardButton('Кабінет викладача')
    btn3 = types.KeyboardButton('Кабінет деканату')
    markup.add(btn1, btn2, btn3)
    return markup


def std_keys():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton('Отримати оцінки')
    btn2 = types.KeyboardButton('Отримати довідку')
    btn3 = types.KeyboardButton('Logout')
    markup.add(btn1, btn2, btn3)
    return markup


def lectr_keys():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton('Змінити оцінки')
    btn2 = types.KeyboardButton('Отримати довідку')
    btn3 = types.KeyboardButton('Logout')
    markup.add(btn1, btn2, btn3)
    return markup


def dean_keys():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton('Пошук студента')
    btn2 = types.KeyboardButton('Видалити студента')
    btn3 = types.KeyboardButton('Змінити курс студента')
    btn4 = types.KeyboardButton('Змінити групу студента')
    btn5 = types.KeyboardButton('Добавити студента')
    btn6 = types.KeyboardButton('Logout')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup


def dov_keys():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton('Студент')
    btn2 = types.KeyboardButton('Викладач')
    btn3 = types.KeyboardButton('Logout')
    markup.add(btn1, btn2, btn3)
    return markup


bot.polling()
