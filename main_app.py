import telebot
from options import keys, TOKEN
from extensions import ConvertException, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Для того что бы приступить к конвертации валюты введите команду /convert ,\n' \
'увидеть список доступных валют: /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Введите валюту, из которой конвертировать'
    bot.send_message(message.chat.id,text)
    bot.register_next_step_handler(message, base_handler)

def base_handler(message:telebot.types.Message):
    base = message.text.strip()
    text = 'Введите валюту, в которую хотите конвертировать'
    bot.send_message(message.chat.id,text)
    bot.register_next_step_handler(message,sym_handler,base)

def sym_handler(message:telebot.types.Message, base):
    sym = message.text.strip()
    text = 'Введите количество конвертруемой валюты:'
    bot.send_message(message.chat.id,text)
    bot.register_next_step_handler(message,amount_handler, base, sym)

def amount_handler(message:telebot.types.Message,base,sym):
    amount = message.text.strip()
    total_base = APIException.convert(base,sym,amount)
    text = f'Цена {amount} {base} в {sym} состовляет : {total_base}'
    bot.send_message(message.chat.id,text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
   try:
        values = message.text.split()

        if len(values) !=3:
             raise ConvertException('Слишком много параметров')

        quote,base,amount = values
        total_base = APIException.convert(quote, base, amount)
   except ConvertException as e:
       bot.reply_to(message, f'Ошибка пользователя\n {e}')
   except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
   else:
        text = f'Цена {amount} в {base} {quote} в состовляет : {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()

