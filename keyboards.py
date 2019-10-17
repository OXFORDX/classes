import telebot
from telebot import types

token = '958037621:AAFB5ZOCMgVKo_7pQbifvqnQm0Oc4GxMthU'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привіт!', reply_markup=keys())


@bot.message_handler(content_types=['text'])
def mess(message):
    if message.text == 'Кабінет студента':
        bot.send_message(message.chat.id, 'Кабінет студента', reply_markup=std_keys())

    if message.text == 'Кабінет викладача':
        bot.send_message(message.chat.id, 'Кабінет студента', reply_markup=lectr_keys())

    if message.text == 'Отримати довідку':
        bot.send_message(message.chat.id, " efe ", reply_markup=dov_keys())
    if message.text == 'Студент':
        try:
            foto = open('dov1.jpg', 'rb')
            bot.send_photo(message.chat.id, foto)
        except Exception as e:
            print(e)

    if message.text == 'Викладач':
        try:
            foto = open('dov2.jpg', 'rb')
            bot.send_photo(message.chat.id, foto)
        except Exception as e:
            print(e)

    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Меню', reply_markup=keys())


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
    markup.add(btn1, btn2)
    return markup


def dov_keys():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Студент')
    btn2 = types.KeyboardButton('Викладач')
    btn3 = types.KeyboardButton('Назад')
    markup.add(btn1, btn2, btn3)
    return markup


bot.polling()
