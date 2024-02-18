from telebot import TeleBot, types
from utils import random_duck, random_fox, random_dog
import wikipedia

wikipedia.set_lang("ru")

TOKEN = '6479165684:AAEKd2KIti0tSSzLSyXdl7r2T38T7xg3oPw'

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['duck'])
def duck(message):
    image = random_duck()
    bot.send_photo(message.chat.id, image)
    
@bot.message_handler(commands=['fox'])
def fox(message):
    image = random_fox()
    bot.send_photo(message.chat.id, image)
    
@bot.message_handler(commands=['dog'])
def dog(message):
    image = random_dog()
    bot.send_photo(message.chat.id, image)
    
@bot.message_handler(commands=['wiki'])
def wiki(message):
    text = ' '.join(message.text.split(' ')[1:])
    results = wikipedia.search(text)
    markup = types.InlineKeyboardMarkup()
    for res in results:
        markup.add(types.InlineKeyboardButton(res, callback_data=res))
    bot.send_message(
        message.chat.id, text='чек', reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: call.data)
def answer(call):
    page = wikipedia.page(call.data)
    bot.send_message(call.message.chat.id, text=page.title)
    bot.send_message(call.message.chat.id, text=page.summary)
    bot.send_message(call.message.chat.id, text=page.url)
    
bot.polling(non_stop=True)