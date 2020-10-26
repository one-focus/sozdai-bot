from lxml import html
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
                bot.send_message(message.chat.id, f'Cообщение не найдено: {str(r.content)}')
                send_screenshot(message)
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'минск':
        ra = requests.get(
            "https://pass.rw.by/ru/route/?from=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA-%D0%A1%D0%B5%D0%B2%D0%B5%D1%80%D0%BD%D1%8B%D0%B9&from_exp=2100450&from_esr=140102&to=%D0%A0%D0%B0%D1%82%D0%BE%D0%BC%D0%BA%D0%B0&to_exp=&to_esr=&front_date=%D1%81%D0%B5%D0%B3%D0%BE%D0%B4%D0%BD%D1%8F&date=today")
        ra_html = html.fromstring(ra.content)
        types = ra_html.xpath(
            '//div[@class="sch-table__body js-sort-body"]//div[@class="sch-table__train-type"]/span[@class="sch-table__route-type"]/text()')
        departures = ra_html.xpath(
            '//div[@class="sch-table__body js-sort-body"]//div[@class="sch-table__time train-from-time"]/text()')
        result = ""
        lenght = len(departures) if len(departures) < 3 else 3
        for i in range(lenght):
            result += f'{departures[i]} {types[i][:3]}\n'
        bot.send_message(message.chat.id, result)
    elif message.text.lower() == 'ратомка':
        ra = requests.get(
            "https://pass.rw.by/ru/route/?from=%D0%A0%D0%B0%D1%82%D0%BE%D0%BC%D0%BA%D0%B0&from_exp=&from_esr=&to=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA-%D0%A1%D0%B5%D0%B2%D0%B5%D1%80%D0%BD%D1%8B%D0%B9&to_exp=2100450&to_esr=140102&front_date=%D1%81%D0%B5%D0%B3%D0%BE%D0%B4%D0%BD%D1%8F&date=today")
        ra_html = html.fromstring(ra.content)
        types = ra_html.xpath(
            '//div[@class="sch-table__body js-sort-body"]//div[@class="sch-table__train-type"]/span[@class="sch-table__route-type"]/text()')
        departures = ra_html.xpath(
            '//div[@class="sch-table__body js-sort-body"]//div[@class="sch-table__time train-from-time"]/text()')
        result = ""
        lenght = len(departures) if len(departures) < 3 else 3
        for i in range(lenght):
            result += f'{departures[i]} {types[i][:3]}\n'
        bot.send_message(message.chat.id, result)
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
    chrome_options.add_argument("--window-size=1024,768")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(url)
    try:
        driver.find_element_by_class_name('popup-appCloseIcon').click()
    except Exception:
        pass
    bot.send_photo(message.chat.id, driver.get_screenshot_as_png(), reply_markup=InlineKeyboardButton("Option 1", callback_data='1'))
    bot.send_message(message.chat.id, "https://algeria.blsspainvisa.com/english/book_appointment.php")


bot.polling(none_stop=True)
