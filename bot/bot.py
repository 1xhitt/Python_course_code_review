import requests, json
import telebot, sys
bot: telebot.TeleBot
TOKEN="6599398767:AAHPQrapoSpeNRuMVDP6J813RcV4_0ZVrso" # no bloody clue how to pass an arg via docker-compose, so...
bot = telebot.TeleBot(TOKEN)
# back_adress="0.0.0.0:6000"
back_adress="back:6000"

headers={
    'Content-type':'application/json', 
    'Accept':'application/json'
}


@bot.message_handler(content_types=['text'], regexp="[0-9]+")
def suggest_gpu(message):
    budget = int(message.text)

    enc = json.encoder.JSONEncoder()
    budget_json = enc.encode({"price" : budget})
    print(budget_json)
    req = requests.get(f"http://{back_adress}/suggest", json=budget_json, headers=headers)
    gpu = json.loads(req.content)
    if None == gpu["price"]:
        ret = "Нет таких дешевок!\n"
    else:
        ret = f"Лучшая карта дешевле {budget}:\n {gpu['full_name']} за {gpu['price']}\n"
        ret += f"на чипсете {gpu['chipset']}\n"
        ret += f"она имееет {gpu['VRAM']} Gb VRAM частотой {gpu['VRAM_freq']} MHz\n"
        ret += f"и частоту ядра {gpu['base_freq']}({gpu['boost_freq']} в boost)\n"
        ret += f"{gpu['HDMI_count']} HDMI и {gpu['DisplayPort_count']} DisplayPort\n" 
        ret += gpu["url"]
    bot.send_message(text=ret, chat_id=message.chat.id)

@bot.message_handler(commands=['scrape'])
def send_welcome(message):
    bot.send_message(text="starting", chat_id=message.chat.id)
    
    requests.post(f"http://{back_adress}/refresh", headers=headers)
	
    bot.send_message(text="over", chat_id=message.chat.id)
    



if __name__ == "__main__":
    bot.infinity_polling()
    pass