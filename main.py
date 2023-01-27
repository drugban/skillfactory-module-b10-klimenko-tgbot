import telebot
from config import keys, TOKEN
from extensions import ConvertionException, Converter

bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения содержащие команды '/start' or '/help' ответным сообщением
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n Чтобы увидеть список доступных валют, введите: /values'
    bot.reply_to(message, text)


# Обрабатываются все сообщения содержащие команды '/values'
@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


# Конвертируем валюту
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = Converter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


# Обрабатываются все фотографии ответным сообщением
@bot.message_handler(content_types=['photo'])
def handle_photo(message: telebot.types.Message):
    bot.reply_to(message, f'Nice meme XDD')


# Обрабатывается все голосовые сообщения
@bot.message_handler(content_types=['voice'])
def repeat(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'У тебя очень красивый голос!')


bot.polling(none_stop=True)
