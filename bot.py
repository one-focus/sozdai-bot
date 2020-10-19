import time

import requests
import telebot

bot = telebot.TeleBot('1234408699:AAEbP0lO7h3BV3XK0Ug1qzc9jPR8_DGtoUI')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока')


@bot.message_handler(commands=['start'])
def start_message(message):
    while True:
        r = requests.get("https://algeria.blsspainvisa.com/english/book_appointment.php")
        if "Appointment dates are not available." in r.content:
            time.sleep(60)
            bot.send_message(message.chat.id, 'No appointmetns')
        else:
            bot.send_message(message.chat.id,
                             'Доступны аппоинтменты: https://algeria.blsspainvisa.com/english/book_appointment.php')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
        while True:
            r = requests.get("https://algeria.blsspainvisa.com/english/book_appointment.php")
            if "Appointment dates are not available." in r.content:
                time.sleep(60)
                bot.send_message(message.chat.id, 'No appointmetns')
            else:
                bot.send_message(message.chat.id,
                                 'Доступны аппоинтменты: https://algeria.blsspainvisa.com/english/book_appointment.php')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'я тебя люблю':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)


bot.polling(none_stop=True)
