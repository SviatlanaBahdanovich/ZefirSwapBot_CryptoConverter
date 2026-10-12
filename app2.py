import telebot
from config import TOKEN, keys
from extension import CryptoConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_message(message: telebot.types.Message):
    text = 'To get started, enter the command in the following format (separated by spaces):' \
        ' \n- <Name of the currency whose price you want to know>  \n- <Name of the currency in which you want to know ' \
        ' the price of the first currency> \n- <Amount of the first currency>\n\
Enter your values: /enter_values'


    bot.reply_to(message, text)


@bot.message_handler(commands=['enter_values'])
def values(message: telebot.types.Message):
    text = 'Your values:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


# base, quote, amount = message.text.split(' ')
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise APIException('Wrong parameters quantity - should be exactly 3 arguments')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'User error. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Failed to process the command\n{e}')
    else:
        text = f'Price {amount} {base} в {quote}: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

