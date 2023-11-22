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
    btn_controlworks = types.KeyboardButton("✍️ Контрольные работы")
    btn_queue = types.KeyboardButton("🗳 Очереди")
    markup.add(btn_homeworks, btn_controlworks, btn_queue)
    bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}!\nЧто бы ты хотел узнать?\n\nНа данный момент можно посмотреть:\n1) 📚 Домашние задания\n2) ✍️ Контрольные работы\n3) 🗳 Очереди", reply_markup=markup)
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
    btn_homeworksfortoday = types.KeyboardButton("⚡️ На сегодня")
    btn_homeworksfortomorrow = types.KeyboardButton("📆 На завтра")
    btn_allactivehomeworks = types.KeyboardButton("📋 Все активные")
    btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
    markup.add(btn_homeworksfortoday, btn_homeworksfortomorrow, btn_allactivehomeworks, btn_back)
    bot.send_message(message.from_user.id, "Выберите, какие ДЗ вы хотите увидеть ( ⚡️ На сегодня / 📆 На завтра / 📋 Все активные )", reply_markup=markup)

def homework_for_today(message):
    update_homeworks_for_today()
    if len(data['homeworks_for_today']) == 0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, "Ура! Домашки на завтра отсутствуют 😊", reply_markup=markup)
    else:
        markupInline = types.InlineKeyboardMarkup()
        for vhomework in data['homeworks_for_today']:
            btn_In_Temp = types.InlineKeyboardButton(text=vhomework[0], url=vhomework[1])
            markupInline.add(btn_In_Temp)
        bot.send_message(message.from_user.id, "⚡️ Домашние задания на сегодня:", reply_markup=markupInline)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, "Другие ДЗ смотрите на сайте ikbo2123.ru", reply_markup=markup)

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

def controlworks(message):
    update_controlworks()
    if len(data['controlworks']) == 0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, "Ура! На данный момент нет запланированных контрольных работ 😊", reply_markup=markup)
    else:
        markupInline = types.InlineKeyboardMarkup(row_width=len(data['controlworks']))
        for controlwork in data['controlworks']:
            btn_In_Temp = types.InlineKeyboardButton(text=controlwork[0], url=controlwork[1])
            markupInline.add(btn_In_Temp)
        bot.send_message(message.from_user.id, "✍️ Запланированные контрольные работы:", reply_markup=markupInline)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, "Остальную информацию вы можете найти на сайте ikbo2123.ru", reply_markup=markup)

# -= Data Update =- #

def update_homeworks_for_today():
    global data
    if time.time() - data['last_timeupdate_for_homeworks_for_today'] >= delta_time or len(data['homeworks_for_today']) == 0:
        data['homeworks_for_today'].clear()
        data['last_timeupdate_for_homeworks_for_today'] = time.time()
        today = list(int(i) for i in pendulum.today("Europe/Moscow").format('DD.MM.YYYY').split('.'))
        today_alternative = list(int(i) for i in pendulum.today("Europe/Moscow").format('DD.MM.YY').split('.'))
        URL_TEMPLATE = "https://ikbo2123.ru/category/general/homeworks/"
        r = requests.get(URL_TEMPLATE)
        soup = bs(r.text, "html.parser")
        homeworks = soup.find_all('h2', class_='wp-block-post-title')
        for homework in homeworks:
            try:
                tempdata = list(int(i) for i in homework.text[-10:].split('.'))
                if today[2] == tempdata[2] and today[1] == tempdata[1] and today[0] == tempdata[0]:
                    data['homeworks_for_today'] += [[homework.text, homework.a['href']]]
            except:
                try:
                    tempdata = list(int(i) for i in homework.text[-8:].split('.'))
                    if tomorrow_alternative[2] == tempdata[2] and tomorrow_alternative[1] == tempdata[1] and \
                            tomorrow_alternative[0] == tempdata[0]:
                        data['homeworks_for_today'] += [[homework.text, homework.a['href']]]
                except:
                    continue

def update_homeworks_for_tomorrow():
    global data
    if time.time() - data['last_timeupdate_for_homeworks_for_tomorrow'] >= delta_time or len(data['homeworks_for_tomorrow']) == 0:
        data['homeworks_for_tomorrow'].clear()
        data['last_timeupdate_for_homeworks_for_tomorrow'] = time.time()
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
    if time.time() - data['last_timeupdate_for_active_homeworks'] >= delta_time or len(data['active_homeworks']) == 0:
        data['active_homeworks'].clear()
        data['last_timeupdate_for_active_homeworks'] = time.time()
        tomorrow = list(int(i) for i in pendulum.tomorrow("Europe/Moscow").format('DD.MM.YYYY').split('.'))
        tomorrow_alternative = list(int(i) for i in pendulum.tomorrow("Europe/Moscow").format('DD.MM.YY').split('.'))
        URL_TEMPLATE = "https://ikbo2123.ru/category/general/homeworks/"
        r = requests.get(URL_TEMPLATE)
        soup = bs(r.text, "html.parser")
        homeworks = soup.find_all('h2', class_='wp-block-post-title')
        for homework in homeworks:
            try:
                tempdata = list(int(i) for i in homework.text[-10:].split('.'))
                if (tomorrow[2] < tempdata[2]) or (tomorrow[2] == tempdata[2] and tomorrow[1] < tempdata[1]) or (tomorrow[2] == tempdata[2] and tomorrow[1] == tempdata[1] and tomorrow[0] <= tempdata[0]):
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
    if time.time() - data['last_timeupdate_for_controlworks'] >= delta_time or len(data['controlworks']) == 0:
        data['controlworks'].clear()
        data['last_timeupdate_for_controlworks'] = time.time()
        today = list(int(i) for i in pendulum.today("Europe/Moscow").format('DD.MM.YYYY').split('.'))
        today_alternative = list(int(i) for i in pendulum.today("Europe/Moscow").format('DD.MM.YY').split('.'))
        URL_TEMPLATE = "https://ikbo2123.ru/category/general/controlworks/"
        r = requests.get(URL_TEMPLATE)
        soup = bs(r.text, "html.parser")
        controlworks = soup.find_all('h2', class_='wp-block-post-title')
        for controlwork in controlworks:
            try:
                tempurl = controlwork.a['href']
                tempr = requests.get(tempurl)
                tempsoup = bs(tempr.text, "html.parser")
                temp_s = str(tempsoup.find_all('div', class_='entry-content wp-block-post-content is-layout-constrained wp-block-post-content-is-layout-constrained'))
                temp_s = temp_s[temp_s.index('Дата проведения:')+16:temp_s.index('</p>')]
                tempdata = ''
                numsDetected = False
                for i in temp_s:
                    if i != ' ':
                        numsDetected = True
                        tempdata += i
                    elif numsDetected == True: break
                tempdata = list(int(i) for i in tempdata.split('.'))
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

# -= Очереди =-

def queue_general_owners(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_take = types.KeyboardButton("📨 Занять очередь")
    btn_leave = types.KeyboardButton("🚪 Выйти из очереди")
    btn_create = types.KeyboardButton("🪄 Создать очередь")
    btn_manage = types.KeyboardButton("🎚 Управлять очередью")
    btn_delete = types.KeyboardButton("🗑 Удалить очередь")
    btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
    markup.add(btn_take, btn_leave, btn_create, btn_manage, btn_delete, btn_back)
    temp_list = ''
    for queue in data['queues'].keys():
        temp_list += f'- {queue}\n'
    if len(temp_list) == 0: temp_list = 'Нет активных очередей!\n'
    bot.send_message(message.from_user.id, f"🗳 Очереди (для админов)\n\nАктивные очереди:\n{temp_list}\nВыберите, что хотите сделать?\n\nДействия:\n1) 📨 Занять очередь\n2) 🚪 Выйти из очереди\n3) 🪄 Создать очередь\n4) 🎚 Управлять очередью\n5) 🗑 Удалить очередь\n", reply_markup=markup)

def queue_general(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_take = types.KeyboardButton("📨 Занять очередь")
    btn_leave = types.KeyboardButton("🚪 Выйти из очереди")
    btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
    markup.add(btn_take, btn_leave, btn_back)
    temp_list = ''
    for queue in data['queues'].keys():
        temp_list += f'- {queue}\n'
    if len(temp_list) == 0: temp_list = 'Нет активных очередей!\n'
    bot.send_message(message.from_user.id, f"🗳 Очереди\n\nАктивные очереди:\n{temp_list}\nВыберите, что хотите сделать?\n\nДействия:\n1) 📨 Занять очередь\n2) 🚪 Выйти из очереди\n", reply_markup=markup)

# -= Создание очередей =-
def queue_create_owners(message):
    global create_room
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    create_room += [message.from_user.id]
    btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
    markup.add(btn_back)
    bot.send_message(message.from_user.id, f"Введите название очереди: \n", reply_markup=markup)

def queue_finalcreate_owners(message):
    global data, create_room
    create_room.pop(create_room.index(message.from_user.id))
    if str(message.text) not in data['queues'].keys():
        data['queues'][str(message.text)] = [[], -1, 0]
        print(data['queues'])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, f"Очередь \"{message.text}\" была успешно создана!\n", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, f"К сожалению, очередь с таким же названием уже существует!\n", reply_markup=markup)

# -= Удаление очередей =-

def queue_delete_owners(message):
    global delete_room
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for queue in data['queues'].keys():
        markup.add(types.KeyboardButton(queue))
    btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
    markup.add(btn_back)
    delete_room += [message.from_user.id]
    bot.send_message(message.from_user.id, f"Выберите, какую из очередей нужно удалить: \n", reply_markup=markup)

def queue_finaldelete_owners(message):
    global data, delete_room
    delete_room.pop(delete_room.index(message.from_user.id))
    if str(message.text) in data['queues'].keys():
        queue_notification_delete_for_all(str(message.text))
        data['queues'].pop(str(message.text))
        print(data['queues'])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, f"Очередь \"{message.text}\" была успешно удалена!\n", reply_markup=markup)
    else:
        queue_failfind(message)

# -= Не удалось найти очередь =-
def queue_failfind(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
    markup.add(btn_back)
    bot.send_message(message.from_user.id, f"Не удалось найти очередь c таким названием!\n", reply_markup=markup)

# -= Занять очередь =-
def queue_take(message):
    global take_room
    take_room += [message.from_user.id]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for queue in data['queues'].keys():
        if int(message.from_user.id) not in list(data['queues'][queue][0][i][0] for i in range(len(data['queues'][queue][0]))):
            markup.add(types.KeyboardButton(queue))
    btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
    markup.add(btn_back)
    bot.send_message(message.from_user.id, f"Выберите, в какую очередь вас закинуть:\n", reply_markup=markup)

def queue_finaltake(message):
    global data, take_room
    take_room.pop(take_room.index(message.from_user.id))
    if str(message.text) in data['queues'].keys():
        if message.from_user.id in list(data['queues'][str(message.text)][0][i][0] for i in range(len(data['queues'][str(message.text)][0]))): #data['queues'][str(message.text)][0].pop(i for i in range(len(data['queues'][str(message.text)][0])) if data['queues'][str(message.text)][0][i][0] == message.from_user.id)
            for i in range(len(data['queues'][str(message.text)][0])):
                print(i, len(data['queues'][str(message.text)][0]))
                if data['queues'][str(message.text)][0][i][0] == message.from_user.id: queue_delete_and_adjustment(str(message.text), data['queues'][str(message.text)][0][i]); break
        data['queues'][str(message.text)][0] += [[int(message.from_user.id), message.from_user.first_name]]
        print(data['queues'])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
        markup.add(btn_back)
        bot.send_message(message.from_user.id, f"Вы были закинуты в очередь \"{message.text}\"!\n\n🥁 Ваш номер в очереди: {data['queues'][message.text][0].index([message.from_user.id, message.from_user.first_name])+1}", reply_markup=markup)
    else:
        queue_failfind(message)

# -= Выйти из очереди =-

def queue_leave(message):
    global leave_room
    leave_room += [message.from_user.id]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for queue in data['queues'].keys():
        if int(message.from_user.id) in list(data['queues'][queue][0][i][0] for i in range(len(data['queues'][queue][0]))):
            markup.add(types.KeyboardButton(queue))
    btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
    markup.add(btn_back)
    bot.send_message(message.from_user.id, f"Выберите, из какой очереди вас необходимо убрать:\n", reply_markup=markup)

def queue_finalleave(message):
    global data, leave_room
    leave_room.pop(leave_room.index(message.from_user.id))
    if str(message.text) in data['queues'].keys():
        if int(message.from_user.id) in list(data['queues'][str(message.text)][0][i][0] for i in range(len(data['queues'][str(message.text)][0]))):
            for i in range(len(data['queues'][str(message.text)][0])):
                if data['queues'][str(message.text)][0][i][0] == message.from_user.id: queue_delete_and_adjustment(str(message.text), data['queues'][str(message.text)][0][i]); break
            print(data['queues'])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
            markup.add(btn_back)
            bot.send_message(message.from_user.id, f"Вы были удалены из очереди \"{message.text}\"!\n", reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
            markup.add(btn_back)
            bot.send_message(message.from_user.id, f"Нам не удалось вас убрать из очереди, так как вы не состоите в \"{message.text}\"!\n", reply_markup=markup)
    else:
        queue_failfind(message)

# -= Управление очередями =-
def queue_select_owners(message):
    global select_manage_room
    select_manage_room += [message.from_user.id]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for queue in data['queues'].keys():
        markup.add(types.KeyboardButton(queue))
    btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
    markup.add(btn_back)
    bot.send_message(message.from_user.id, f"Выберите, какой очередью вы собиратетесь управлять:\n", reply_markup=markup)

def queue_finalselect_owners(message):
    global data, select_manage_room
    select_manage_room.pop(select_manage_room.index(message.from_user.id))
    if str(message.text) in data['queues'].keys():
        if data['queues'][str(message.text)][1] == -1:
            data['queues'][str(message.text)][1] = message.from_user.id
            print(data['queues'])
            queue_manage_owners(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
            markup.add(btn_back)
            bot.send_message(message.from_user.id,f"К сожалению, очередью \"{message.text}\" уже кто-то управляет!\n",reply_markup=markup)
    else:
        queue_failfind(message)

def queue_manage_owners(message):
    global select_remove_person
    if message.from_user.id not in owners: four_zero_four(message)
    if message.from_user.id in select_remove_person: select_remove_person.pop(select_remove_person.index(message.from_user.id))
    else:
        name_queue = ''
        for queue in data['queues'].keys():
            if data['queues'][queue][1] == int(message.from_user.id):
                name_queue = queue; break
        if len(name_queue) == 0: queue_failfind(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn_next = types.KeyboardButton("👉 Вызвать следующего человека")
            btn_remove_person = types.KeyboardButton("❌ Удалить человека из очереди")
            btn_update_info = types.KeyboardButton("ℹ️ Обновить информацию")
            btn_reset = types.KeyboardButton("🔄 Начать заново")
            btn_back = types.KeyboardButton("⬅️ Вернуться в меню")
            markup.add(btn_next, btn_remove_person, btn_update_info, btn_reset, btn_back)
            temp_string_list = ''
            for person in data['queues'][name_queue][0]:
                temp_string_list += f"{data['queues'][name_queue][0].index(person)+1}) {person[1]} {'🟢' if data['queues'][name_queue][0].index(person)+1 < data['queues'][name_queue][2] else '🟡' if data['queues'][name_queue][0].index(person)+1 == data['queues'][name_queue][2] else '🔴'}\n"
            bot.send_message(message.from_user.id, f"📋 Очередь \"{name_queue}\"\n\nСейчас отвечает: {data['queues'][name_queue][0][data['queues'][name_queue][2]-1][1] if data['queues'][name_queue][2] > 0 else '---'}\n\nПрогресс очереди: {data['queues'][name_queue][2]} / {len(data['queues'][name_queue][0])}\n\nОчередь:\n{temp_string_list}\nВы можете:\n1) 👉 Вызвать следующего человека\n2) ❌ Удалить человека из очереди\n3) ℹ️ Обновить информацию\n", reply_markup=markup)

def queue_processing_request(message):
    name_queue = ''
    for queue in data['queues'].keys():
        if message.from_user.id == data['queues'][queue][1]:
            name_queue = queue
            break
    if len(name_queue) > 0:
        if data['queues'][name_queue][2] < len(data['queues'][name_queue][0]):
            data['queues'][name_queue][2] += 1
            queue_notification_now(data['queues'][name_queue][0][data['queues'][name_queue][2] - 1], name_queue)
            if data['queues'][name_queue][2] != len(data['queues'][name_queue][0]): queue_notification_next(data['queues'][name_queue][0][data['queues'][name_queue][2]], name_queue)
            queue_notification_all(name_queue)
        queue_manage_owners(message)
    else:
        four_zero_four(message)

def queue_notification_now(userFromQueue, name_queue):
    bot.send_message(userFromQueue[0], f"🚨 {userFromQueue[1]}, пришла ваша очередь!!!\n\nВы получили данное уведомление, так как вы записаны в очереди \"{name_queue}\". Просим вас отреагировать на это сообщение оперативно и не задерживать всю очередь!")


def queue_notification_next(userFromQueue, name_queue):
    bot.send_message(userFromQueue[0], f"‼️ {userFromQueue[1]}, вы будете следующим!!!\n\nВы получили данное уведомление, так как вы записаны в очереди \"{name_queue}\". Просим вас отреагировать на это сообщение оперативно и не задерживать всю очередь!")

def queue_notification_all(name_queue):
    if data['queues'][name_queue][2] + 2 > len(data['queues'][name_queue][0]): return 0
    for i in range(data['queues'][name_queue][2] + 1, len(data['queues'][name_queue][0])):
        if data['queues'][name_queue][0][i][0] != data['queues'][name_queue][1] : bot.send_message(data['queues'][name_queue][0][i][0], f"{data['queues'][name_queue][0][i][1]}, свежая информация об очереди \"{name_queue}\"\n\nВаш номер: {i+1}\n\nПрогресс очереди: {data['queues'][name_queue][2]} / {len(data['queues'][name_queue][0])}\n\nОсталось: {i - data['queues'][name_queue][2] + 1}\n\nПросим вас обращать внимания на наши уведомления!")

def queue_notification_remove(ex_queue_man, name_queue):
    bot.send_message(ex_queue_man[0], f"🚫 {ex_queue_man[1]}, вас убрали из очереди!\n\nВы получили данное уведомление, так как вы БЫЛИ записаны в очереди \"{name_queue}\".")

def queue_notification_delete_for_all(name_queue):
    for person in data['queues'][name_queue][0]:
        bot.send_message(person[0], f"🗑 {person[1]}, очередь \"{name_queue}\" была распущена!\n\nВы получили данное уведомление, так как вы БЫЛИ записаны в очереди \"{name_queue}\".")

def queue_delete_and_adjustment(name_queue, userFromQueue):
    global data
    temp_queue = data['queues'][name_queue]
    if temp_queue[0].index(userFromQueue) + 1 > temp_queue[2]:
        temp_queue[0].pop(temp_queue[0].index(userFromQueue))
    else:
        temp_queue[2] -= 1
        temp_queue[0].pop(temp_queue[0].index(userFromQueue))
    data['queues'][name_queue] = temp_queue

def queue_reset_owners(name_queue, message):
    global data
    if name_queue in data['queues'].keys():
        data['queues'][name_queue][2] = 0
    queue_manage_owners(message)

# -= Удаление человека из очереди со стороны контроллёра =-

def queue_select_remove_person(name_queue, message):
    global select_remove_person
    select_remove_person += [message.from_user.id]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for person in data['queues'][name_queue][0]:
        if data['queues'][name_queue][0].index(person) + 1 > data['queues'][name_queue][2]: markup.add(types.KeyboardButton(person[1]))
    markup.add(types.KeyboardButton("⬅️ Вернуться к управлению"))
    bot.send_message(message.from_user.id, f"Выберите, какого человека стоит удалить из очереди:\n", reply_markup=markup)

def queue_final_Remove_person(message):
    global select_remove_person
    if message.from_user.id not in select_remove_person: four_zero_four(message); return 0
    select_remove_person.pop(select_remove_person.index(message.from_user.id))
    name_queue = ''
    for queue in data['queues'].keys():
        if message.from_user.id == data['queues'][queue][1]:
            name_queue = queue
            break
    if len(name_queue) == 0:
        four_zero_four(message); return 0
    temp_user = []
    for i in range(len(data['queues'][name_queue][0])):
        if data['queues'][name_queue][0][i][1] == str(message.text): temp_user = data['queues'][name_queue][0][i]; break
    if len(temp_user) == 0: four_zero_four(message); return 0
    queue_delete_and_adjustment(name_queue, temp_user)
    queue_notification_remove(temp_user, name_queue)
    queue_manage_owners(message)

# -= Обработка запроса =- #

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    match message.text:
        case "📚 Домашние задания":
            select_data_homeworks(message)
        case "⚡️ На сегодня":
            homework_for_today(message)
        case "📆 На завтра":
            homework_for_tomorrow(message)
        case "📋 Все активные":
            active_homeworks(message)
        case "✍️ Контрольные работы":
            controlworks(message)
        case "🗳 Очереди":
            if message.from_user.id in owners:
                queue_general_owners(message)
            else: queue_general(message)
        case "⬅️ Вернуться в меню":
            if message.from_user.id in create_room: create_room.pop(create_room.index(message.from_user.id))
            if message.from_user.id in delete_room: delete_room.pop(delete_room.index(message.from_user.id))
            if message.from_user.id in take_room: take_room.pop(take_room.index(message.from_user.id))
            if message.from_user.id in leave_room: leave_room.pop(leave_room.index(message.from_user.id))
            for queue in data['queues'].keys():
                if data['queues'][queue][1] == message.from_user.id: data['queues'][queue][1] = -1; break
            start(message)
        case "🪄 Создать очередь":
            if message.from_user.id in owners:
                queue_create_owners(message)
            else:
                four_zero_four(message)
        case "🗑 Удалить очередь":
            if message.from_user.id in owners:
                queue_delete_owners(message)
            else:
                four_zero_four(message)
        case "📨 Занять очередь":
            queue_take(message)
        case "🚪 Выйти из очереди":
            queue_leave(message)
        case "🎚 Управлять очередью":
            if message.from_user.id in owners:
                queue_select_owners(message)
            else:
                four_zero_four(message)
        case "👉 Вызвать следующего человека":
            if message.from_user.id in owners: queue_processing_request(message)
            else: four_zero_four(message)
        case "ℹ️ Обновить информацию":
            if message.from_user.id not in owners: four_zero_four(message)
            else:
                name_queue = ''
                for queue in data['queues'].keys():
                    if message.from_user.id == data['queues'][queue][1]:
                        name_queue = queue
                        break
                if len(name_queue) == 0: four_zero_four(message)
                else:
                    queue_manage_owners(message)
        case "🔄 Начать заново":
            if message.from_user.id not in owners:
                four_zero_four(message)
            else:
                name_queue = ''
                for queue in data['queues'].keys():
                    if message.from_user.id == data['queues'][queue][1]:
                        name_queue = queue
                        break
                if len(name_queue) == 0:
                    four_zero_four(message)
                else:
                    queue_reset_owners(name_queue, message)
        case "❌ Удалить человека из очереди":
            if message.from_user.id not in owners:
                four_zero_four(message)
            else:
                name_queue = ''
                for queue in data['queues'].keys():
                    if message.from_user.id == data['queues'][queue][1]:
                        name_queue = queue
                        break
                if len(name_queue) == 0:
                    four_zero_four(message)
                else:
                    queue_select_remove_person(name_queue, message)
        case "⬅️ Вернуться к управлению":
            if message.from_user.id not in owners:
                four_zero_four(message)
            else:
                queue_manage_owners(message)
        case _:
            if message.from_user.id in create_room:
                queue_finalcreate_owners(message)
            elif message.from_user.id in delete_room:
                queue_finaldelete_owners(message)
            elif message.from_user.id in take_room:
                queue_finaltake(message)
            elif message.from_user.id in leave_room:
                queue_finalleave(message)
            elif message.from_user.id in select_manage_room:
                queue_finalselect_owners(message)
            elif message.from_user.id in select_remove_person:
                queue_final_Remove_person(message)
            else:
                four_zero_four(message)


# -= Start bot  =- #
users = []
startbot = True
owners = [980673249, 678949997]
create_room = []
delete_room = []
take_room = []
leave_room = []
select_manage_room = []
select_remove_person = []
delta_time = 600
data = {
    'homeworks_for_today': [],
    'homeworks_for_tomorrow': [],
    'active_homeworks': [],
    'controlworks': [],
    'last_timeupdate_for_homeworks_for_today': 0,
    'last_timeupdate_for_homeworks_for_tomorrow': 0,
    'last_timeupdate_for_active_homeworks': 0,
    'last_timeupdate_for_controlworks': 0,
    'queues': {},
}
bot.polling(non_stop=True)
