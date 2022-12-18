import telebot

from config import keys,TOKEN
from extensions import  ConvertionException,ValueConverter
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start','help'])
def help (message:telebot.types.Message):

    text='Чтобы конвертировать валюту необходимо ввести боту команду в формате:\n<имя валюты > \
    <в какую валюту перевести> \
    <количество переводимой валюты>\
    <Чтобы получить писок доступных валют /values>  '
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text", ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise ConvertionException(f"Неверное количество параметров ввода")
        quote, base, amount = values
        total_base = ValueConverter.getConvert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка ввода данных.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать комманду\n{e}")
    else:
        amount = float(amount)
        if amount >= 1:
            total_base = str(float(amount * total_base))
        text = f"цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling()