import telebot, processing, sys
bot: telebot.TeleBot
suggestor: processing.Suggestor
TOKEN=sys.argv[1]  
bot = telebot.TeleBot(TOKEN)
suggestor = processing.Suggestor()

@bot.message_handler(content_types=['text'], regexp="[0-9]+")
def suggest_gpu(message):
    price = int(message.text)
    gpu = suggestor.suggest(price)
    if gpu is None:
        ret = "Нет таких дешевок!\n"
    else:
        ret = f"Лучшая карта дешевле {price}:\n {gpu.get_full_name()} за {gpu.price}\n"
        ret += f"на чипсете {gpu.chipset}\n"
        ret += f"она имееет {gpu.VRAM} Mb VRAM\n"
        ret += f"{gpu.core_count} ядер " if gpu.core_count else ""
        ret += f"частотой {gpu.base_freq}({gpu.boost_freq} в boost)\n" if gpu.base_freq else ""
        ret += f"поддерцивает разрешение {gpu.max_definition}\n"
        ret += f"{gpu.HDMI_count if gpu.HDMI_count else 0} HDMI и {gpu.DisplayPort_count if gpu.DisplayPort_count else 0} DisplayPort" 
        ret += f"гарантия {gpu.guarantee} месяцев" if gpu.guarantee else ""
        # print("suggersing")
        # print(ret)
    bot.send_message(text=ret, chat_id=message.chat.id)



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(text="Введи цену в рублях и я подскажу, что выбрать", chat_id=message.chat.id)
     

if __name__ == "__main__":
    bot.infinity_polling()
    pass