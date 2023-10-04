import telebot
from telebot import types
import pendulum
import requests
from bs4 import BeautifulSoup as bs
import time

# -= Токен бота =- #

bot = telebot.TeleBot('6440852245:AAE6CiE5QkugkNk2VHKlybHezUx2jdfkg-w')

# -= Страницы бота =- #

@bot.message_handler(commands = ['start'])
def start(message):
    global users
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_homeworks = types.KeyboardButton("📚 Домашние задания")
    #btn_controlworks = types.KeyboardButton("✍️ Контрольные работы")
    #btn_topics = types.KeyboardButton("📝 Темы докладов")
    markup.add(btn_homeworks)
    bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}!\nЧто бы ты хотел узнать?\n\nНа данный момент можно посмотреть:\n1) 📚 Домашние задания\n2) ✍️ Контрольные работы", reply_markup=markup)
    if message.from_user.id not in users:
        users += [message.from_user.id]
        print(users)

def four_zero_four(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
    markup.add(btn_back)
    bot.send_message(message.from_user.id, "Упс... Походу я не могу обработать ваш запрос 😔", reply_markup=markup)

def select_data_homeworks(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_homeworksfortomorrow = types.KeyboardButton("📆 На завтра")
    btn_allactivehomeworks = types.KeyboardButton("📋 Все активные")
    btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
    markup.add(btn_homeworksfortomorrow, btn_allactivehomeworks, btn_back)
    bot.send_message(message.from_user.id, "Выберите, какие ДЗ вы хотите увидеть ( 📆 На завтра / 📋 Все активные )", reply_markup=markup)

def homework_for_tomorrow(message):
    update_homeworks_for_tomorrow()
    if len(data['homeworks_for_tomorrow']) == 0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, "Ура! Домашки на завтра отсутствуют 😊", reply_markup=markup)
    else:
        markupInline = types.InlineKeyboardMarkup()
        for vhomework in data['homeworks_for_tomorrow']:
            btn_In_Temp = types.InlineKeyboardButton(text=vhomework[0], url=vhomework[1])
            markupInline.add(btn_In_Temp)
        bot.send_message(message.from_user.id, "📚 Домашние задания на завтра:", reply_markup=markupInline)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, "Другие ДЗ смотрите на сайте ikbo2123.ru", reply_markup=markup)

def active_homeworks(message):
    update_active_homeworks()
    if len(data['active_homeworks']) == 0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, "Ура! Домашек на данный момент нет 😊", reply_markup=markup)
    else:
        markupInline = types.InlineKeyboardMarkup(row_width=len(data['active_homeworks']))
        for vhomework in data['active_homeworks']:
            btn_In_Temp = types.InlineKeyboardButton(text=vhomework[0], url=vhomework[1])
            markupInline.add(btn_In_Temp)
        bot.send_message(message.from_user.id, "📚 Активные домашние задания:", reply_markup=markupInline)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, "Остальную информацию вы найдёте на сайте ikbo2123.ru", reply_markup=markup)

# def controlworks(message):
#     update_controlworks()
#     if len(data['controlworks']) == 0:
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#         btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
#         markup.add(btn_back)
#         bot.send_message(message.from_user.id, "Ура! На данный момент нет запланированных контрольных работ 😊", reply_markup=markup)
#     else:
#         markupInline = types.InlineKeyboardMarkup(row_width=len(data['controlworks']))
#         for controlwork in data['controlworks']:
#             btn_In_Temp = types.InlineKeyboardButton(text=controlwork[0], url=controlwork[1])
#             markupInline.add(btn_In_Temp)
#         bot.send_message(message.from_user.id, "✍️ Запланированные контрольные работы:", reply_markup=markupInline)
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#         btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
#         markup.add(btn_back)
#         bot.send_message(message.from_user.id, "Остальную информацию вы можете найти на сайте ikbo2123.ru", reply_markup=markup)

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
        #case "✍️ Контрольные работы":
            #controlworks(message)
        #case "📝 Темы докладов":
            pass
        case "⬅️ Вернуться в меню":
            start(message)
        case _:
            four_zero_four(message)

# -= Data Update =- #

def update_homeworks_for_tomorrow():
    global data
    data['homeworks_for_tomorrow'].clear()
    tomorrow = list(int(i) for i in pendulum.tomorrow("Europe/Moscow").format('DD.MM.YYYY').split('.'))
    tomorrow_alternative = list(int(i) for i in pendulum.tomorrow("Europe/Moscow").format('DD.MM.YY').split('.'))
    URL_TEMPLATE = "https://ikbo2123.ru/category/general/homeworks/"
    r = requests.get(URL_TEMPLATE)
    soup = bs(r.text, "html.parser")
    homeworks = soup.find_all('h2', class_='wp-block-post-title')
    for homework in homeworks:
        try:
            tempdata = list(int(i) for i in homework.text[-10:].split('.'))
            if tomorrow[2] == tempdata[2] and tomorrow[1] == tempdata[1] and tomorrow[0] == tempdata[0]:
                data['homeworks_for_tomorrow'] += [[homework.text, homework.a['href']]]
        except:
            try:
                tempdata = list(int(i) for i in homework.text[-8:].split('.'))
                if tomorrow_alternative[2] == tempdata[2] and tomorrow_alternative[1] == tempdata[1] and \
                        tomorrow_alternative[0] == tempdata[0]:
                    data['homeworks_for_tomorrow'] += [[homework.text, homework.a['href']]]
            except:
                continue

def update_active_homeworks():
    global data
    data['active_homeworks'].clear()
    tomorrow = list(int(i) for i in pendulum.tomorrow("Europe/Moscow").format('DD.MM.YYYY').split('.'))
    tomorrow_alternative = list(int(i) for i in pendulum.tomorrow("Europe/Moscow").format('DD.MM.YY').split('.'))
    URL_TEMPLATE = "https://ikbo2123.ru/category/general/homeworks/"
    r = requests.get(URL_TEMPLATE)
    soup = bs(r.text, "html.parser")
    homeworks = soup.find_all('h2', class_='wp-block-post-title')
    for homework in homeworks:
        try:
            tempdata = list(int(i) for i in homework.text[-10:].split('.'))
            if (tomorrow[2] < tempdata[2]) or (tomorrow[2] == tempdata[2] and tomorrow[1] < tempdata[1]) or (
                    tomorrow[2] == tempdata[2] and tomorrow[1] == tempdata[1] and tomorrow[0] <= tempdata[0]):
                data['active_homeworks'] += [[homework.text, homework.a['href']]]
        except:
            try:
                tempdata = list(int(i) for i in homework.text[-8:].split('.'))
                if (tomorrow_alternative[2] < tempdata[2]) or (
                        tomorrow_alternative[2] == tempdata[2] and tomorrow_alternative[1] < tempdata[1]) or (
                        tomorrow_alternative[2] == tempdata[2] and tomorrow_alternative[1] == tempdata[1] and
                        tomorrow_alternative[0] <= tempdata[0]):
                    data['active_homeworks'] += [[homework.text, homework.a['href']]]
            except:
                continue

def update_controlworks():
    global data
    data['controlworks'].clear()
    today = list(int(i) for i in pendulum.today("Europe/Moscow").format('DD.MM.YYYY').split('.'))
    today_alternative = list(int(i) for i in pendulum.today("Europe/Moscow").format('DD.MM.YY').split('.'))
    URL_TEMPLATE = "https://ikbo2123.ru/category/general/controlworks/"
    r = requests.get(URL_TEMPLATE)
    soup = bs(r.text, "html.parser")
    controlworks = soup.find_all('h2', class_='wp-block-post-title')
    for controlwork in controlworks:
        try:
            tempdata = list(int(i) for i in controlwork.text[-10:].split('.'))
            if (today[2] < tempdata[2]) or (today[2] == tempdata[2] and today[1] < tempdata[1]) or (
                    today[2] == tempdata[2] and today[1] == tempdata[1] and today[0] <= tempdata[0]):
                data['controlworks'] += [[controlwork.text, controlwork.a['href']]]
        except:
            try:
                tempdata = list(int(i) for i in controlwork.text[-8:].split('.'))
                if (today_alternative[2] < tempdata[2]) or (
                        today_alternative[2] == tempdata[2] and today_alternative[1] < tempdata[1]) or (
                        today_alternative[2] == tempdata[2] and today_alternative[1] == tempdata[1] and
                        today_alternative[0] <= tempdata[0]):
                    data['controlworks'] += [[controlwork.text, controlwork.a['href']]]
            except:
                continue

# -= Start bot  =- #
users = []
startbot = True
data = {
    'homeworks_for_tomorrow': [],
    'active_homeworks': [],
    'controlworks': [],
    'lasttimeupdate': time.time(),
}
bot.polling(non_stop=True)