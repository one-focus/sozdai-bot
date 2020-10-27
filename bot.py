import time

import trains
import telebot
import visa
from telebot import types

bot = telebot.TeleBot("1275523107:AAF_5t_r80J55Pl-JcVeLcVVOsl7kadqAc4")


@bot.message_handler(commands=["start"])
def inline(message):
    bot.send_message(message.chat.id, text="Чего угодно?", reply_markup=main_menu_buttons())


def main_menu_buttons():
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Виза", callback_data="visa")
    but_2 = types.InlineKeyboardButton(text="Поезда", callback_data="trains")
    but_3 = types.InlineKeyboardButton(text="Скриншот", callback_data="screen")
    key.add(but_1, but_2, but_3)
    return key


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'visa':
        while True:
            screenshot = visa.monitor()
            if not screenshot:
                prog = "◽"
                for i in range(3600):
                    if len(prog) > 3:
                        prog = "◽"
                    else:
                        prog = f"{prog}◽"
                    bot.edit_message_text(chat_id=c.message.chat.id, text=f'Мониторинг дат:\n{prog}',
                                          message_id=c.message.message_id)
                    time.sleep(1)
            else:
                keyboard = types.InlineKeyboardMarkup()
                link_button = types.InlineKeyboardButton(text="Сайт", url=visa.URL)
                keyboard.add(link_button)
                bot.send_photo(c.message.chat.id, visa.send_screenshot(), reply_markup=keyboard)
                break
    elif c.data == 'trains':
        key = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(text="из Минск-Северного", callback_data="minsk")
        but_2 = types.InlineKeyboardButton(text="из Ратомки", callback_data="ratomka")
        but_3 = types.InlineKeyboardButton(text="< Назад", callback_data="back_to_main")
        key.add(but_1, but_2, but_3)
        bot.edit_message_text(chat_id=c.message.chat.id, text="Направление", message_id=c.message.message_id,
                              reply_markup=key)
    elif c.data == 'minsk':
        res = trains.get_trains(
            "https://pass.rw.by/ru/route/?from=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA-%D0%A1%D0%B5%D0%B2%D0%B5%D1%80%D0%BD%D1%8B%D0%B9&from_exp=2100450&from_esr=140102&to=%D0%A0%D0%B0%D1%82%D0%BE%D0%BC%D0%BA%D0%B0&to_exp=&to_esr=&front_date=%D1%81%D0%B5%D0%B3%D0%BE%D0%B4%D0%BD%D1%8F&date=today")
        bot.edit_message_text(chat_id=c.message.chat.id, text=res, message_id=c.message.message_id)
    elif c.data == 'ratomka':
        res = trains.get_trains(
            "https://pass.rw.by/ru/route/?from=%D0%A0%D0%B0%D1%82%D0%BE%D0%BC%D0%BA%D0%B0&from_exp=&from_esr=&to=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA-%D0%A1%D0%B5%D0%B2%D0%B5%D1%80%D0%BD%D1%8B%D0%B9&to_exp=2100450&to_esr=140102&front_date=%D1%81%D0%B5%D0%B3%D0%BE%D0%B4%D0%BD%D1%8F&date=today")
        bot.send_message(c.message.chat.id, res)
    elif c.data == 'screen':
        keyboard = types.InlineKeyboardMarkup()
        link_button = types.InlineKeyboardButton(text="Сайт", url=visa.URL)
        keyboard.add(link_button)
        bot.send_photo(c.message.chat.id, visa.send_screenshot(), reply_markup=keyboard)
    elif c.data == 'back_to_main':
        bot.edit_message_text(chat_id=c.message.chat.id, text="Чего угодно?", message_id=c.message.message_id,
                              reply_markup=main_menu_buttons())


if __name__ == '__main__':
    bot.infinity_polling()
