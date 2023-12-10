import py_compile
import re
import requests, json
import telebot, sys

# docker-compose loses stdout
import sys
sys.stdout = sys.stderr

bot: telebot.TeleBot
TOKEN="6599398767:AAHPQrapoSpeNRuMVDP6J813RcV4_0ZVrso" 
bot = telebot.TeleBot(TOKEN)
# back_adress="0.0.0.0:6000"
back_adress="back:6000"

headers={
    'Content-type':'application/json', 
    'Accept':'application/json'
}

# chat id -> search settings
user_settings: dict[int: dict[str: str]] = dict()
user_settings.setdefault(dict)


@bot.message_handler(content_types=['text'], regexp="^[0-9]+")
def suggest_gpu(message):
    budget = int(message.text)
    brand = user_settings[message.chat.id]["brand"]
    chipset = user_settings[message.chat.id]["chipset"]
    enc = json.encoder.JSONEncoder()
    budget_json = enc.encode({"price" : budget, "brand" : brand, "chipset" : chipset})
    print(budget_json)
    req = requests.get(f"http://{back_adress}/suggest", json=budget_json, headers=headers)
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
    req = requests.get(f"http://{back_adress}/brands", headers=headers)
    brands = json.loads(req.content)
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(*["set to " + brand for brand in brands])
    user_settings[message.chat.id]['active_setting'] = "brand"
    bot.send_message(message.chat.id, "which one?", reply_markup=markup)
    pass


@bot.message_handler(commands=['set_chipset'])
def set_brand(message):
    req = requests.get(f"http://{back_adress}/chipsets", headers=headers)
    chipsets = json.loads(req.content)
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(*["set to " + chipsets for chipsets in chipsets])
    user_settings[message.chat.id]['active_setting'] = "chipset"
    bot.send_message(message.chat.id, "which one?", reply_markup=markup)
    pass


@bot.message_handler(content_types=['text'], regexp="set\sto\s[a-zA-Z]+")
def set_value(message):
    active_setting = user_settings[message.chat.id]['active_setting']
    if active_setting == "NONE":
        print("No active setting")
        return
    elif active_setting == 'brand':
        val = message.text[7:]
        user_settings[message.chat.id]["brand"] = val
        bot.send_message(message.chat.id, f"changed brand to <{val}>", reply_markup=telebot.types.ReplyKeyboardRemove())
    elif active_setting == 'chipset':
        val = message.text[7:]
        user_settings[message.chat.id]["chipset"] = val
        bot.send_message(message.chat.id, f"changed chipset to <{val}>", reply_markup=telebot.types.ReplyKeyboardRemove())
    user_settings[message.chat.id]['active_setting'] = "NONE"
    
@bot.message_handler(commands=['scrape'])
def scrape(message):
    bot.send_message(text="starting", chat_id=message.chat.id)
    requests.post(f"http://{back_adress}/refresh", headers=headers)
    bot.send_message(text="over", chat_id=message.chat.id)
    
@bot.message_handler(commands=['start', 'reset'])
def start(message):
    user_settings[message.chat.id] = dict()
    user_settings[message.chat.id]['brand'] = 'ANY'
    user_settings[message.chat.id]['chipset'] = 'ANY'
    user_settings[message.chat.id]['active_setting'] = "NONE"
    bot.send_message(message.chat.id, "done")
    
if __name__ == "__main__":
    bot.infinity_polling()
    pass