
import telebot
import random
from telebot import types

moves = ['камень', 'ножницы', 'бумага']
bot_token = '6476719645:AAHs18kysNydpbVp90-D8n7qMl-Hctd6bEc'
bot = telebot.TeleBot(token=bot_token)

name = 'Капибара'
energy = 70
happiness = 100
satiety = 30
health = 60
clear = 50

coin = 0

def clean():
    global happiness, clear
    happiness = happiness + 10
    clear = clear + 20

def feed():
    global energy, satiety
    energy = energy + 5
    satiety = satiety + 20

def heal():
    global health, happiness
    health = health + 15
    happiness = happiness + 15

def play():
    global energy, satiety, happiness
    energy = energy - 5
    satiety = satiety - 10
    happiness = happiness + 20
    satiety = satiety - 10

def sleep():
    global energy, satiety, happiness
    energy = 70
    satiety = satiety - 10
    happiness = happiness + 10

def check(message):
    global energy, satiety, happiness
    if satiety <= 0:
        bot.send_message(message.chat.id, f'{name} умер от голода. '
                                              f'Не забывайте кормить питомца!')
    elif satiety >= 10:
        bot.send_message(message.chat.id, f'{name} наелся и счастлив!')

    if happiness < 0:
        bot.send_message(message.chat.id, f'{name} умер от тоски. '
                                  f'С питомцем нужно чаще играть!')
    elif happiness > 100:
        bot.send_message(message.chat.id, f'{name} счастлив как никогда')

    if energy < 0:
        bot.send_message(message.chat.id, f'{name} умер от истощения.')
    elif energy > 70:
        bot.send_message(message.chat.id, f'{name} полон сил и энергии!')
    if health <= 0:
        bot.send_message(message.chat.id, f'{name} умер от болезни. '
                                              f'Не забывайте лечить питомца!')
    if clear <= 0:
        bot.send_message(message.chat.id, f'{name} умер от болезни. '
                                              f'Не забывайте мыть питомца!')

@bot.message_handler(commands=['clear'])
def play_handler(message):
    clean()
    bot.send_message(message.chat.id, f'{name} помылся и '
                                      f'теперь его чистота составляет {clear}!')
    check(message)


@bot.message_handler(commands=['play'])
def play_handler(message):
    play()
    bot.send_message(message.chat.id, f'{name} поиграл и '
                                      f'теперь его счастье составляет {happiness}!')
    check(message)


@bot.message_handler(commands=['feed'])
def feed_handler(message):
    feed()
    bot.send_message(message.chat.id, f'{name} вкусно покушал и '
                                      f'теперь его голод составляет {satiety}!')
    check(message)

@bot.message_handler(commands=['health'])
def heal_handler(message):
    heal()
    bot.send_message(message.chat.id, f'{name} был у ветеринара и '
                                      f'теперь его здоровье составляет {health}!')
    check(message)

@bot.message_handler(commands=['sleep'])
def sleep_handler(message):
    sleep()
    bot.send_message(message.chat.id,  f'{name} поспал! тебе его сон '
                                       f'составляет {energy}')
# Разработать функцию - для вывода характеристик питомца
@bot.message_handler(commands=['about'])
def about_pet(message):
    bot.send_message(message.chat.id, f'уровень счасться {happiness} '
                                      f'уровень голода {satiety} '
                                      f'уровень энергии {energy} '
                                      f'здоровье {health} '
                                      f'имя питомца {name} '
                                      f'уровень чистоты {clear}')


@bot.message_handler(commands=['rock'])
def reply_to_hello(message):

    markup = types.InlineKeyboardMarkup(row_width=1)
    button_1 = types.InlineKeyboardButton('🗿 камень', callback_data='камень')
    button_2 = types.InlineKeyboardButton('✂️ ножницы', callback_data='ножницы')
    button_3 = types.InlineKeyboardButton('📃 бумага', callback_data='бумага')

    markup.add(button_1, button_2, button_3)
    bot.send_message(message.chat.id, "давай поиграем в камень ножницы бумага?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global coin
    if call.message:
        user = call.data
        if user.lower() == 'камень' or user.lower() == 'ножницы' or user.lower() == 'бумага':
            computer = random.choice(moves)
            bot.send_message(call.message.chat.id, "я выбрал " + computer)
            if user.lower() == computer:
                bot.send_message(call.message.chat.id, 'ничья')
            elif (user.lower() == 'камень' and computer == 'ножницы' or user.lower() == 'ножницы'
                and computer == 'бумага' or user.lower() == 'бумага' and computer == 'камень'):
                bot.send_message(call.message.chat.id, 'Ты победил(а)!')
                coin = coin + 10
            else:
                bot.send_message(call.message.chat.id, 'Ты проиграл(а)!')
                coin = coin - 10
        else:
            bot.send_message(call.message.chat.id, 'неправильный вариант')
    bot.send_message(call.message.chat.id, f'у вас очков {coin}')


@bot.message_handler(content_types=['text'])
def text_handler(message):
    bot.send_message(message.chat.id, 'Такой команды нет, нажмите /feed чтобы покормить'
                                      ' /play для игры /sleep для сна, команда характеристики /about,'
                                      ' вылечить /health, команда для мытья /clear ,/rock чтобы поиграть в камень|ножницы|бумага')
bot.polling()
