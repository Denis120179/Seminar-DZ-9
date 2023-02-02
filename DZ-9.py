# ИГРА С БОТОМ В КОНФЕТЫ

import telebot
from telebot import types
import random

bot = telebot.TeleBot("Напишите свой TOKEN")

user_sweet = 0
bot_sweet = 0
sweets = 221
max_sweets = 28
name1 = "игрок"
name2 = "bot" 
player = " "


@bot.message_handler(commands = ["start"])

def start(message): 
    bot.send_message(message.chat.id, "/Menu")   

@bot.message_handler(commands = ["Menu"])

def Menu(message):   
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    but1 = types.KeyboardButton("Правила игры")
    but2 = types.KeyboardButton("Игра")
    markup.add(but1) 
    markup.add(but2) 
    bot.send_message(message.chat.id, "Выбери пункт", reply_markup=markup)

@bot.message_handler(content_types = "text")

def controller(message):    
    if message.text == "Правила игры":
        bot.send_message(message.chat.id, "Условие задачи: На столе лежит 221 конфета. Играют два игрока," 
        "делая ход друг после друга. Первый ход определяется жеребьёвкой. За один ход можно забрать не более,"
        "чем 28 конфет. Выигрывает игорок, сделавший ход последним.")                
    
    elif message.text == "Игра":
        bot.send_message(message.chat.id, "Введите имя игрока")         
        bot.register_next_step_handler(message, game) 

def game(message): 
    global player, name1, name2
    first_turn = random.choice([name1, name2])    
    player = name1 if first_turn == name1 else name2
    bot.send_message(message.chat.id, f"Первым ходит {player}") 
    count(message)

def count(message):  
    global player, name1, name2      
    if sweets > 0: 
        if player == name1:
            bot.send_message(message.chat.id, "Сколько конфет берете?")   
            bot.register_next_step_handler(message, user_turn)
        else:
           bot_turn(message) 
    else:
        winner = name2 if player == name1 else name1
        bot.send_message(message.chat.id, f"Победитель {winner}")

def bot_turn(message):
    global sweets, bot_sweet, player
    if sweets == max_sweets:
        bot_sweet = sweets
    elif sweets < max_sweets:
        bot_sweet = sweets
    elif sweets%max_sweets == 0:
        bot_sweet = max_sweets-1
    else:
        bot_sweet = sweets%max_sweets-1
        if bot_sweet == 0:
            bot_sweet = 1 
    sweets -= bot_sweet
    bot.send_message(message.chat.id, f"Бот взял {bot_sweet} конфет")
    bot.send_message(message.chat.id, f"Осталось {sweets} конфет")
    player = name2 if player == name1 else name1
    count(message)
    
def user_turn(message):
    global sweets, player, user_sweet
    user_sweet = int(message.text)
    sweets -= user_sweet
    bot.send_message(message.chat.id, f"Осталось {sweets} конфет")
    player = name2 if player == name1 else name1
    count(message)

bot.infinity_polling()  

# СОЗДАНИЕ КАЛЬКУЛЯТОРА НА БОТЕ

import telebot
from telebot import types

typeNums = 0
res = 0

bot = telebot.TeleBot("Напишите свой TOKEN")

@bot.message_handler(commands = ["start"])

def calculator(message):    
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    but1 = types.KeyboardButton("Рациональные числа")
    but2 = types.KeyboardButton("Комплексные числа")
    markup.add(but1) 
    markup.add(but2) 
    bot.send_message(message.chat.id, "Выбери числа", reply_markup=markup)

@bot.message_handler(content_types = "text")

def buttons(message): 
    global typeNums  
    a = types.ReplyKeyboardRemove() 
    if message.text == "Рациональные числа":
        bot.send_message(message.chat.id, "Введите выражение, разделяя знаки пробелами")                
        bot.register_next_step_handler(message, controller) 
        typeNums = 0

    elif message.text == "Комплексные числа":
        bot.send_message(message.chat.id, "Введите выражение, разделяя знаки пробелами")                
        bot.register_next_step_handler(message, controller) 
        typeNums = 1

def controller(message):
    global res
    line = message.text.split()
    znak = line[1]
    if typeNums == 0:
        a = int(line[0])    
        b = int(line[2])
    if typeNums == 1:
        a = complex(line[0])    
        b = complex(line[2])
    if znak == '+':
        res = a+b
    elif znak == '-':
        res = a-b
    elif znak == '*':
        res = a*b
    elif znak == '/':
        res = a/b
    elif znak == '//' and typeNums == 0:
        res = a//b
    elif znak == '%' and typeNums == 0:
        res = a%b
    elif typeNums == 1 and znak == '//' or znak == '%':
        bot.send_message(message.chat.id, "Неверный ввод или недопустимая операция, проверьте выражение")
        bot.register_next_step_handler(message, controller)
        return
    bot.send_message(message.chat.id, str(res)) 

bot.infinity_polling()