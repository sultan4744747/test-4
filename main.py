import telebot
from telebot import types
import random
import time

token = token
bot = telebot.TeleBot(token)

hp = 0
damage = 0
exp = 0
lvl = 1


def create_monster():
    rnd_name = random.choice(monster)
    rnd_hp = random.randint(130, 150)
    rnd_damage = random.randint(130, 170)

    return [rnd_name, rnd_hp, rnd_damage]


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton('Начать игру')
    btn2 = types.KeyboardButton('Об игре')

    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, text='Готов начать игру?', reply_markup=markup)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton('Начать игру')
    btn2 = types.KeyboardButton('Об игре')

    markup.add(btn1, btn2)
    return markup

def start_quest():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = "В путь"
    btn2 = "В главное меню"

    markup.add(btn1, btn2)

    return markup


def combat():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = "Бежать"
    btn2 = "В главное меню"
    btn3 = "Атаковать"

    markup.add(btn1, btn2, btn3)

    return markup


@bot.message_handler(content_types=['text'])
def answer(message):
    global hp, damage, exp, lvl

    victim = create_monster()

    if (message.text == 'Начать игру'):

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = 'Эльф'
        btn2 = 'Гном'

        markup.add(btn1, btn2)

        bot.send_message(message.chat.id, text='Выберите расу', reply_markup=markup)
    elif (message.text == 'В главное меню'):
        hp = damage = 0

        bot.send_message(message.chat.id, text='Вы вернулись в главное меню', reply_markup=main_menu())

    if (message.text == 'Эльф'):

        hp += 300
        damage += 80

        bot.send_message(message.chat.id, text=f'Вы выбрали эльфа, hp = {hp}, damage = {damage}. Готов начать?',
                         reply_markup=start_quest())


    elif (message.text == 'Гном'):

        hp += 300
        damage += 90

        bot.send_message(message.chat.id, text=f'Вы выбрали гнома, hp = {hp}, damage = {damage}. Готов начать?',
                         reply_markup=start_quest())

    if (message.text == 'В путь'):

        event = random.randint(1, 2)

        if event == 1:

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn12 = "В путь"
            btn13 = "В главное меню"

            markup.add(btn12, btn13)

            bot.send_message(message.chat.id, 'Пока никто не встретился... Идем дальше ?', reply_markup=markup)

        elif event == 2:

            # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            #
            # btn9 = 'Атаковать'
            # btn10 = 'Бежать'
            # btn11 = 'В главное меню'
            #
            # markup.add(btn11, btn10, btn9)

            bot.send_message(message.chat.id, text="А вот и монстр!")

            time.sleep(2)

            bot.send_message(message.chat.id, text=f'Ого!Встретился монстр!Монстра зовут {victim[0]},у него {victim[1]}'
                                                   f'очков здоровья и вот такой урон:{victim[2]}',
                             reply_markup=combat())

    if (message.text == 'Атаковать'):

        victim[1] -= damage
        if victim[1] <= 0:
            exp += 10 * lvl

            if exp >= lvl * 50:
                lvl += 1
                hp += 15
                damage += 20

                bot.send_message(message.chat.id, text=f'Ваш уровень повысился.Здоровье:{hp},Урон:{damage},'
                                                       f'Уровень:{lvl},Опыт:{exp}')

            bot.send_message(message.chat.id,
                             text=f'Враг повержен.Ты получаешь:{10 * lvl} опыта.Продолжаем путешествие ?',
                             reply_markup=start_quest())

        elif victim[1] > 0:

            hp -= victim[2]

            bot.send_message(message.chat.id, text=f'Оставшееся здоровье у монстра {victim[1]}.Монстр нас атакует')

            if hp <= 0:

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn3 = 'Вернуться в главное меню'

                markup.add(btn3)

                bot.send_message(message.chat.id, text='Вы проиграли.Монстр победил.', reply_markup=main_menu())

            elif hp > 0:

                bot.send_message(message.chat.id, text=f'Оставшееся здоровье у монстра {victim[1]}.'
                                                       f'Оставшееся здоровье героя {hp},Что будешь делать?',
                                 reply_markup=combat())
    elif (message.text == 'Бежать'):

        plan = random.randint(1, 2)
        if plan == 1:

            bot.send_message(message.chat.id, text=f'Вы сумели сбежать от монстра!Продолжаем путешествие?',
                             reply_markup=start_quest())

        elif plan == 2:

            hp -= victim[2]

            bot.send_message(message.chat.id, text=f'Вы не смогли сбежать.Монстр нас атакует')

            if hp <= 0:

                bot.send_message(message.chat.id, text='Вы проиграли.Монстр победил.', reply_markup=main_menu())


            elif hp > 0:

                bot.send_message(message.chat.id, text=f'Оставшееся здоровье у монстра {victim[1]}.'
                                                       f'Оставшееся здоровье героя {hp},Что будешь делать?',
                                 reply_markup=combat())


    elif (message.text == 'Об игре'):

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn13 = 'В главное меню'

        markup.add(btn13)

        bot.send_message(message.chat.id, text='Это игра ПОДЗЕМЕЛЬЕ.В которой тебе нужно побороть зло.\nУдачи!!!')


monster = ["СЛИЗЬ", "ЗОМБИ", "ВОР"]

bot.polling(non_stop=True)
