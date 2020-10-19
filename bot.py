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
    from selenium import webdriver
    import os
    bot.send_message(message.chat.id, "1")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    bot.send_message(message.chat.id, "2")
    subprocess.run("alias chrome='/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'", shell=True)
    subprocess.run("chrome --headless --disable-gpu --screenshot https://www.chromestatus.com/", shell=True)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    bot.send_message(message.chat.id, "3")
    driver.get("https://google.com")

    bot.send_message(message.chat.id, driver.title)
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
