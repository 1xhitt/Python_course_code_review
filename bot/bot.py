import re
import requests
import json
import telebot
import sys
import config
# docker-compose loses stdout
import sys
sys.stdout = sys.stderr

bot: telebot.TeleBot
bot = telebot.TeleBot(config.TOKEN)

# chat id -> search settings
user_settings: dict[int: dict[str: str]] = dict()
user_settings.setdefault(dict)


@bot.message_handler(content_types=['text'], regexp="^[0-9]+")
def suggest_gpu(message):
    budget = int(message.text)
    brand = user_settings[message.chat.id]["brand"]
    chipset = user_settings[message.chat.id]["chipset"]
    enc = json.encoder.JSONEncoder()
    budget_json = enc.encode(
        {"price": budget, "brand": brand, "chipset": chipset})
    print(budget_json)
    req = requests.get(f"http://{config.BACK_ADRESS}/suggest",
                       json=budget_json, headers=config.HEADERS)
    gpu = json.loads(req.content)
    if None == gpu["price"]:
        ret = "Нет таких дешевок!\n"
    else:
        ret = f"Лучшая карта дешевле {budget}:\n {gpu['brand']} {gpu['name']} за {gpu['price']}\n"
        ret += f"на чипсете {gpu['chipset']}\n"
        ret += f"она имееет {gpu['VRAM']} Gb VRAM частотой {gpu['VRAM_freq']} MHz\n"
        ret += f"и частоту ядра {gpu['base_freq']}({gpu['boost_freq']} в boost)\n"
        ret += f"{gpu['HDMI_count']} HDMI и {gpu['DisplayPort_count']} DisplayPort\n"
        ret += gpu["url"]
    bot.send_message(text=ret, chat_id=message.chat.id)


@bot.message_handler(commands=['set_brand'])
def set_brand(message):
    req = requests.get(
        f"http://{config.BACK_ADRESS}/brands", headers=config.HEADERS)
    brands = json.loads(req.content)
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(*["На " + brand for brand in brands])
    user_settings[message.chat.id]['active_setting'] = "brand"
    bot.send_message(message.chat.id, "На какой?", reply_markup=markup)
    pass


@bot.message_handler(commands=['set_chipset'])
def set_brand(message):
    req = requests.get(
        f"http://{config.BACK_ADRESS}/chipsets", headers=config.HEADERS)
    chipsets = json.loads(req.content)
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(*["На " + chipsets for chipsets in chipsets])
    user_settings[message.chat.id]['active_setting'] = "chipset"
    bot.send_message(message.chat.id, "На какой?", reply_markup=markup)
    pass


@bot.message_handler(content_types=['text'], regexp="На\s[a-zA-Z]+")
def set_value(message):
    active_setting = user_settings[message.chat.id]['active_setting']
    if active_setting == "NONE":
        print("No active setting")
        return
    elif active_setting == 'brand':
        val = message.text[3:]
        user_settings[message.chat.id]["brand"] = val
        bot.send_message(
            message.chat.id, f"Изменил искомый брэнд на <{val}>", reply_markup=telebot.types.ReplyKeyboardRemove())
    elif active_setting == 'chipset':
        val = message.text[3:]
        user_settings[message.chat.id]["chipset"] = val
        bot.send_message(
            message.chat.id, f"Изменил искомый чипсет на <{val}>", reply_markup=telebot.types.ReplyKeyboardRemove())
    user_settings[message.chat.id]['active_setting'] = "NONE"


@bot.message_handler(commands=['scrape'])
def scrape(message):
    bot.send_message(text="Начинаю скрапить", chat_id=message.chat.id)
    requests.post(f"http://{config.BACK_ADRESS}/refresh",
                  headers=config.HEADERS)
    bot.send_message(text="Всё готово", chat_id=message.chat.id)


@bot.message_handler(commands=['start', 'reset'])
def start(message):
    user_settings[message.chat.id] = dict()
    user_settings[message.chat.id]['brand'] = 'ANY'
    user_settings[message.chat.id]['chipset'] = 'ANY'
    user_settings[message.chat.id]['active_setting'] = "NONE"
    bot.send_message(message.chat.id, "Всё готово")


if __name__ == "__main__":
    bot.infinity_polling()
    pass
