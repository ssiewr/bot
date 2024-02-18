import json
from telebot import TeleBot, types

TOKEN = '6479165684:AAEKd2KIti0tSSzLSyXdl7r2T38T7xg3oPw'

bot = TeleBot(TOKEN)

game = False
indx = 0
points = 0

with open('my_quizz.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    
def get_next_question(data: dict, indx: int) -> object:
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    btn_row1 = [types.KeyboardButton(data[indx]['вариант'][i]) for i in range(2)]
    markup.add(*btn_row1) 
    
    btn_row2 = [types.KeyboardButton(data[indx]['вариант'][i + 2]) for i in range(2)]
    markup.add(*btn_row2) 
    
    markup.add(types.KeyboardButton('выход'))
    return markup

@bot.message_handler(commands=['points'])
def get_score(message):
    bot.send_message(message.chat.id, f'набрано очков: {points}')
    
@bot.message_handler(commands=['quizz'])
def quiz(message):
    global game, indx
    game = True
    markup = get_next_question(data, indx)
    if 'image' in data[indx]:
        img = open(data[indx]['image'], 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
    bot.send_message(message.chat.id, text=data[indx]['вопрос'], reply_markup=markup)
    
@bot.message_handler()
def victorina(message):
    global game, indx, points
    if game:
        if message.text == data[indx]['ответ']:
            bot.send_message(message.chat.id, 'верно')
            points += 1
        elif message.text == 'выход':
            game = False
            bot.send_message(message.chat.id, 'лан')
            return
        else:
            markup = get_next_question(data, indx)
            bot.send_message(message.chat.id, f"неправильно, {data[indx]['ответ']}")
        indx += 1
        if len(data) < indx: 
            markup = get_next_question(data, indx)
            if 'image' in data[indx]:
                img = open(data[indx], 'rb')
                bot.send_photo(message.chat.id, img)
                img.close()
            bot.send_message(bot.chat.id, text=data[indx]['вопрос'], reply_markup=markup)
            
bot.polling(non_stop=True)