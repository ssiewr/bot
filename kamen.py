from random import choice
from telebot import TeleBot
import random

TOKEN = '6479165684:AAEKd2KIti0tSSzLSyXdl7r2T38T7xg3oPw'
bot = TeleBot(TOKEN)

game_choice = ['камень', 'ножницы', 'бумага']

class Game:
    comp = 0
    user = 0
    
    def update(self, user_winner: bool) -> str:
        if user_winner:
            self.user += 1
            return 'победа'
        self.comp += 1
        return 'проиг'
    
    def get_score(self) -> str:
        return f'вы: {self.user}\nбоярыня: {self.comp}'
    
    def reset(self):
        self.comp = 0
        self.user = 0

gm = Game()

@bot.message_handler(func=lambda x: x.text.lower() in game_choice)
def game(message):
    user_choice = message.text.lower()
    comp_choice = choice(game_choice)
    
    bot.send_message(message.chat.id, comp_choice)
    
    if user_choice == comp_choice:
        msg = 'ничьч'
    elif user_choice == 'камень' and comp_choice == 'ножницы':
        msg = gm.update(user_winner=True)

    elif user_choice == 'бумага' and comp_choice == 'камень':
        msg = gm.update(user_winner=True)

    elif user_choice == 'ножницы' and comp_choice == 'бумага':
        msg = gm.update(user_winner=True)

    else:
        gm.update(user_winner=False)
        
    try:
        img = open(msg + '.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
    except:
        print('блин')
        
    bot.send_message(message.chat.id, msg)
    
@bot.message_handler(commands=['points'])
def get_point(message):
    bot.send_message(message.chat.id, gm.get_score())
    
@bot.message_handler(commands=['reset'])
def reset(message):
    gm.reset()
    bot.send_message(message.chat.id, 'очки обнулены')
    
@bot.message_handler(commands=['lootbox'])
def lootbox(message):
    if gm.user == 0:
        bot.send_message(message.chat.id, 'недостаток очков лл')
        return
    gm.user -= 1
    number = random.randint(1, 100)
    if number <= 80:
        image = 'kartofel.png'
    elif number <= 95:
        image = 'pelmeny.png'
    else:
        image = 'borch.png'
    img = open(image, 'rb')
    bot.send_photo(message.chat.id, img)
    img.close()
    bot.send_message(message.chat.id, f"осталось очков: {gm.user}")
    
bot.polling(non_stop=True)