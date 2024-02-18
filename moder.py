from time import time
from random import randint
from telebot import TeleBot, types

TOKEN = '6479165684:AAEKd2KIti0tSSzLSyXdl7r2T38T7xg3oPw'

bot = TeleBot(TOKEN)

with open('bad_word.txt', 'r', encoding='utf-8') as f:
    data = [word.strip().lower() for word in f.readlines()]
    
sum_check = 0

def is_group(message):
    return message.chat.type in ('group', 'supergroup')

@bot.message_handler(commands=['check'])
def default_test(message):
    global sum_check
    keyboard = types.InlineKeyboardMarkup()
    numbers = ['один', "два", "три", "четыре", "пять", 
               "шесть", "семь", "восемь", "девять", "десять"]
    keys = []
    for indx, number in enumerate(numbers):
        keys.append(types.InlineKeyboardButton(
            text=number, callback_data=indx+1))
    keyboard.row(*keys)
    n1 = randint(1, 5)
    n2 = randint(1, 5)
    sum_check = n1 + n2
    bot.send_message(
        message.chat.id, f'решите пример {n1} + {n2} = ?', reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: call.data)
def callback_inline(call):
    global sum_check
    if int(call.data) == sum_check:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text = 'проверка пройдена')
    if int(call.data) != sum_check:
        bot.ban_chat_member(call.message.chat.id,
                            call.from_user.id)

@bot.message_handler(func=lambda message: message.entities is not None and is_group(message))
def delete_links(message):
    for entity in message.entities:
        if entity.type in ['url', 'text_link']:
            bot.delete_message(message.chat.id, message.message_id)
            
def has_bad_word(text):
    message_word = text.split(' ')
    for word in message_word:
        if word in data:
            return True
    return False
            
@bot.message_handler(func=lambda message: has_bad_word(message.text.lower()) and is_group(message))
def bad_bad_words(message):
    bot.restrict_chat_member(
        message.chat.id,
        message.from_user.id,
        until_date=time()+1200)
    
    bot.send_message(message.chat.id, text='бан на 20 мин',
                     reply_to_message_id=message.message_id)
    
    bot.delete_message(message.chat.id, message.message_id)
    
bot.polling(non_stop=True)