import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет!\nЯ умею конвертировать валюты по курсу European Central Bank.\n' \
'Для начала работы введите команду в формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nНапример, евро рубль 150\nУвидеть доступные валюты: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))  # каждая валюта переносится на строчку вниз
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Что-то не так с параметрами.\nМне нужны две разные валюты и количество.')

        base, quote, amount = values
        total_base = CurrencyConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Конвертирую {base} в {quote}:\n{amount} {keys[base]} = {total_base} {keys[quote]}\n'
        bot.send_message(message.chat.id, text)


bot.polling()