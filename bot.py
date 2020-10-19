import subprocess
import time

import requests
import telebot
from selenium import webdriver

bot = telebot.TeleBot('1234408699:AAEbP0lO7h3BV3XK0Ug1qzc9jPR8_DGtoUI')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока')


@bot.message_handler(commands=['start'])
def start_message(message):
    subprocess.run("brew cask install chromedriver", shell=True)
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver.get("https://google.com")
    bot.send_message(message.chat.id, 'chrome installed')
    # driver.save_screenshot("screen.png")

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
        while True:
            r = requests.get("https://algeria.blsspainvisa.com/english/book_appointment.php")
            if "Appointment dates are not available." in str(r.content):
                time.sleep(60)
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
