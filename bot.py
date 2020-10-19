import subprocess
import time

import requests
import telebot
from selenium import webdriver
import os

bot = telebot.TeleBot('1234408699:AAEbP0lO7h3BV3XK0Ug1qzc9jPR8_DGtoUI')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока')
url = 'https://algeria.blsspainvisa.com/english/book_appointment.php'


@bot.message_handler(commands=['start'])
def start_message(message):
    send_screenshot(message)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
        while True:
            r = requests.get(url)
            if "Appointment dates are not available." in str(r.content):
                time.sleep(60)
            else:
                send_screenshot(message)
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'я тебя люблю':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)


def send_screenshot(message):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(url)
    driver.execute_scriptfind_element_by_class_name('popup-appCloseIcon').click()
    bot.send_photo(message.chat.id, driver.get_screenshot_as_png())
    bot.send_message(message.chat.id, "https://algeria.blsspainvisa.com/english/book_appointment.php")


bot.polling(none_stop=True)
