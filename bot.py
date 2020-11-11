import time

import search
import trains
import telebot
import visa
from telebot import types

bot = telebot.TeleBot("1275523107:AAF_5t_r80J55Pl-JcVeLcVVOsl7kadqAc4")


@bot.message_handler(commands=["start"])
def inline(message):
    bot.send_message(message.chat.id, text="Что хотите сделать, Александр?", reply_markup=main_menu_buttons())


def sleep_animation(message, duration, text):
    prog = "◽"
    for i in range(duration):
        if not search.is_searching:
            break
        if len(prog) > 3:
            prog = "◽"
        else:
            prog = f"{prog}◽"
        bot.edit_message_text(chat_id=message.chat.id, text=f'Мониторим {text}:\n{prog}',
                              message_id=message.message_id)
        time.sleep(1)


def search_on_baraholka(message):
    search.is_searching = True
    search_results = []
    try:
        while True:
            if not search.is_searching:
                break
            res = search.search(message.text)
            for product in res:
                print(f'product:{product}')
                print(f'search_results:{search_results}')
                if product[0] not in [result[0] for result in search_results]:
                    keyboard = types.InlineKeyboardMarkup()
                    link_button = types.InlineKeyboardButton(text=product[2], url=product[0])
                    delete_button = types.InlineKeyboardButton(text="✖️", callback_data="delete_message")
                    keyboard.add(link_button, delete_button)
                    bot.send_message(message.chat.id, text=f"\n{product[1]}", reply_markup=keyboard)
                    search_results.append(product)
            sleep_animation(message=search.global_mess, duration=60, text=message.text)
    except Exception as e:
        bot.send_message(message.chat.id, text=f"Ошибка:{e}")


def main_menu_buttons():
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Виза", callback_data="visa")
    but_2 = types.InlineKeyboardButton(text="Поезда", callback_data="trains")
    but_3 = types.InlineKeyboardButton(text="Поиск", callback_data="search")
    but_4 = types.InlineKeyboardButton(text="Стоп", callback_data="stop_monitor")
    key.add(but_1, but_2, but_3, but_4)
    return key


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    try:
        if c.data == 'visa' and visa.IS_MONITORING == False:
            while True:
                screenshot = visa.monitor()
                if not screenshot:
                    visa.IS_MONITORING = True
                    sleep_animation(message=c.message, duration=3600, text="Мониторим визы")
                else:
                    visa.IS_MONITORING = False
                    keyboard = types.InlineKeyboardMarkup()
                    link_button = types.InlineKeyboardButton(text="Сайт", url=visa.URL)
                    keyboard.add(link_button)
                    bot.send_photo(c.message.chat.id, visa.send_screenshot(), reply_markup=keyboard)
                    break
        elif c.data == 'trains':
            key = types.InlineKeyboardMarkup()
            but_1 = types.InlineKeyboardButton(text="Минск-Сев", callback_data="minsk")
            but_2 = types.InlineKeyboardButton(text="Ратомка", callback_data="ratomka")
            but_3 = types.InlineKeyboardButton(text="< Назад", callback_data="back_to_main")
            key.add(but_1, but_2, but_3)
            bot.edit_message_text(chat_id=c.message.chat.id, text="Откуда хотите поехать, Александр?:",
                                  message_id=c.message.message_id,
                                  reply_markup=key)
        elif c.data == 'minsk':
            bot.edit_message_text(text=trains.get_trains(
                "https://pass.rw.by/ru/route/?from=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA-%D0%A1%D0%B5%D0%B2%D0%B5%D1%80%D0%BD%D1%8B%D0%B9&from_exp=2100450&from_esr=140102&to=%D0%A0%D0%B0%D1%82%D0%BE%D0%BC%D0%BA%D0%B0&to_exp=&to_esr=&front_date=%D1%81%D0%B5%D0%B3%D0%BE%D0%B4%D0%BD%D1%8F&date=today"),
                chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=main_menu_buttons())
        elif c.data == 'ratomka':
            bot.edit_message_text(trains.get_trains(
                "https://pass.rw.by/ru/route/?from=%D0%A0%D0%B0%D1%82%D0%BE%D0%BC%D0%BA%D0%B0&from_exp=&from_esr=&to=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA-%D0%A1%D0%B5%D0%B2%D0%B5%D1%80%D0%BD%D1%8B%D0%B9&to_exp=2100450&to_esr=140102&front_date=%D1%81%D0%B5%D0%B3%D0%BE%D0%B4%D0%BD%D1%8F&date=today"),
                chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=main_menu_buttons())
        elif c.data == 'search':
            search.global_mess = c.message
            bot.edit_message_text(text="Что хотите найти на куфаре и барахолке?", chat_id=c.message.chat.id, message_id=c.message.message_id)
            bot.register_next_step_handler(c.message, search_on_baraholka)
        elif c.data == 'back_to_main':
            bot.edit_message_text(chat_id=c.message.chat.id, text="Что хотите сделать, Александр?",
                                  message_id=c.message.message_id,
                                  reply_markup=main_menu_buttons())
        elif c.data == 'delete_message':
            bot.delete_message(chat_id=c.message.chat.id, message_id=c.message.message_id)
        elif c.data == 'stop_monitor':
            search.is_searching = False
    except Exception as e:
        bot.send_message(c.message.chat.id, text=f"Ошибка:{e}")


if __name__ == '__main__':
    bot.infinity_polling()
