import telebot, processing
bot: telebot.TeleBot
suggestor: processing.Suggestor
TOKEN="6686967575:AAGcXVJTUnHX-dyISl8ruB_MWuJlMvP82s0"
bot = telebot.TeleBot(TOKEN)
suggestor = processing.Suggestor()

@bot.message_handler(content_types=['text'], regexp="[0-9]+")
def suggest_gpu(message):
    price = int(message.text)
    gpu = suggestor.suggest(price)
    ret = f"Лучшая карта дешевле {price}:\n {gpu.get_full_name()} за {gpu.price}\n"\
        + f"на чипсете {gpu.chipset}\n"\
        + f"она имееет {gpu.VRAM} Mb VRAM с пропускной способностью {gpu.bandwidth} Gb/s,\n"\
        + f"{gpu.core_count} ядер, частотой {gpu.base_freq}({gpu.boost_freq} в boost)\n"\
        + f"поддерцивает разрешение {gpu.max_definition}, {gpu.HDMI_count} и {gpu.DisplayPort_count} HDMI и DisplayPort портов соответственно" \
        + f"гарантия {gpu.guarantee} месяцев"
    print("suggersing")
    bot.send_message(text=ret, chat_id=message.chat.id)



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
     
if __name__ == "__main__":
    bot.infinity_polling()
    pass