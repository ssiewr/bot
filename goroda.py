from random import choice
from telebot import TeleBot, types

TOKEN = '6943625153:AAHP9KUDuX_D-M2uySqkuAoso7uQ_YsZG6k'

bot = TeleBot(TOKEN)

game = False # старт и стоп игры
used_words = [] # список использованных слов
letter = '' # буква на которую надо приидумать слово

with open('cities.txt', 'r', encoding='utf-8') as file:
    cities = [word.strip().lower() for word in file.readlines()]
    
def select_letter(text: str) -> str:
    i = 1
    while text[-1*i] in ('ь', 'ъ', 'ы', 'й'):
        i += 1
    return text[-1*i]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'пр')
    
@bot.message_handler(commands=['goroda'])
def goroda(message):
    global game, letter
    game = True
    city = choice(cities)
    letter = select_letter(city)
    bot.send_message(message.chat.id, city)

@bot.message_handler()
def play(message):
    global user_words, letter, game
    print('нужная буква:', letter)
    if game:
        if message.text.lower() in used_words:
            bot.send_message(message.chat.id, 'было')
            return
        if message.text.lower()[0] != letter:
            bot.send_message(message.chat.id, 'не та буква')
            return
        if message.text.lower() in cities:
            letter = select_letter(message.text.lower())
            used_words.append(message.text.lower())
            
            for city in cities:
                if city[0] == letter and city not in used_words:
                    letter = select_letter(city)
                    bot.send_message(message.chat.id, city)
                    used_words.append(city)
                    return
                
            bot.send_message(message.chat.id, 'ну блин')
            game = False
            return
        bot.send_message(message.chat.id, 'нуне' )
        
bot.polling(non_stop=True)

