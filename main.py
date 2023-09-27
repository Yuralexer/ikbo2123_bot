import telebot
from telebot import types
import pendulum
import requests
from bs4 import BeautifulSoup as bs

# -= Токен бота =- #

bot = telebot.TeleBot('6440852245:AAE6CiE5QkugkNk2VHKlybHezUx2jdfkg-w')

# -= Страницы бота =- #

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_homeworks = types.KeyboardButton("📚 Домашние задания")
    btn_topics = types.KeyboardButton("📝 Темы докладов")
    markup.add(btn_homeworks, btn_topics)
    bot.send_message(message.from_user.id, f"Привет, {message.from_user.username}!\nЧто вы хотели бы узнать?", reply_markup=markup)

def four_zero_four(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
    markup.add(btn_back)
    bot.send_message(message.from_user.id, "Упс... Походу я не могу обработать ваш запрос 😔", reply_markup=markup)

def select_data_homeworks(message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    btn_homeworksfortomorrow = types.KeyboardButton("📆 На завтра")
    btn_allactivehomeworks = types.KeyboardButton("📋 Все активные")
    markup.add(btn_homeworksfortomorrow, btn_allactivehomeworks)
    bot.send_message(message.from_user.id, "Выберите, какие ДЗ вы хотите увидеть ( 📆 На завтра / 📋 Все активные )")

def homework_for_tomorrow(message):
    tomorrow = list(int(i) for i in pendulum.tomorrow("Europe/Moscow").format('DD.MM.YYYY').split('.'))
    URL_TEMPLATE = "https://ikbo2123.ru/category/general/homeworks/"
    r = requests.get(URL_TEMPLATE)
    soup = bs(r.text, "html.parser")
    homeworks = soup.find_all('h2', class_='wp-block-post-title')
    verificated_homeworks = []
    for homework in homeworks:
        tempdata = list(int(i) for i in homework.text[-10:].split('.'))
        if tomorrow[2] == tempdata[2] and tomorrow[1] == tempdata[1] and tomorrow[0] == tempdata[0]:
            verificated_homeworks += [[homework.text, homework.a['href']]]
    if len(verificated_homeworks) == 0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, "Ура! Домашки на завта отсутствуют 😊", reply_markup=markup)
    else:
        markupInline = types.InlineKeyboardMarkup()
        buttons = []
        for vhomework in verificated_homeworks:
            btn_In_Temp = types.InlineKeyboardButton(text=vhomework[0], href=vhomework[1])
            markupInline.add(btn_In_Temp)
        bot.send_message(message.from_user.id, "📚 Домашние задания на завтра:", reply_markup=markupInline)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, "Другие ДЗ смотрите на сайте ikbo2123.ru", reply_markup=markup)

def active_homeworks(message):
    tomorrow = list(int(i) for i in pendulum.tomorrow("Europe/Moscow").format('DD.MM.YYYY').split('.'))
    URL_TEMPLATE = "https://ikbo2123.ru/category/general/homeworks/"
    r = requests.get(URL_TEMPLATE)
    soup = bs(r.text, "html.parser")
    homeworks = soup.find_all('h2', class_='wp-block-post-title')
    verificated_homeworks = []
    for homework in homeworks:
        tempdata = list(int(i) for i in homework.text[-10:].split('.'))
        if (tomorrow[2] < tempdata[2]) or (tomorrow[2] == tempdata[2] and tomorrow[1] < tempdata[1]) or (tomorrow[2] == tempdata[2] and tomorrow[1] == tempdata[1] and tomorrow[0] <=tempdata[0]):
            verificated_homeworks += [[homework.text, homework.a['href']]]
    if len(verificated_homeworks) == 0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, "Ура! Домашек на данный момент нет 😊", reply_markup=markup)
    else:
        markupInline = types.InlineKeyboardMarkup()
        buttons = []
        for vhomework in verificated_homeworks:
            btn_In_Temp = types.InlineKeyboardButton(text=vhomework[0], href=vhomework[1])
            markupInline.add(btn_In_Temp)
        bot.send_message(message.from_user.id, "📚 Активные домашние задания:", reply_markup=markupInline)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, "Остальную информацию вы найдёте на сайте ikbo2123.ru", reply_markup=markup)

# -= Обработка запроса =- #

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    match message.text:
        case "📚 Домашние задания":
            select_data_homeworks(message)
        case "📆 На завтра":
            homework_for_tomorrow(message)
        case "📋 Все активные":
            active_homeworks(message)
        case "📝 Темы докладов":
            pass
        case "⬅️ Вернуться в меню":
            start(message)
        case _:
            four_zero_four(message)
