
import datetime
from datetime import datetime
from datetime import date
import pymongo
from pymongo import MongoClient
import telebot
from telebot import types




MURL = "mongodb://mongo:27017"
connection = MongoClient(MURL) 

db = connection['MeasuringTools']

collection_exist_check = db.list_collection_names()        
if "measuring_tools" not in collection_exist_check:
    db.create_collection("measuring_tools")

bot = telebot.TeleBot('5774981582:AAGMtlDQVJA4EqoZf29blS-T65xJwLHlWUk')

@bot.message_handler(commands=['help', 'start'])




def start_main_menu(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('1: Внести средство измерения', '2: Редактировать/Удалить', '3: Вывести все СИ', '4: Вывести один тип СИ', '5: Вывести истекающие/Просроченые')

    mes = """Что необходимо сделать? Выберите вариант:

    1: Внести срество измерения

    2: Редактировать/Удалить срество измерения

    3: Вывести все срества измерения

    4: Вывести срества измерения конкретного типа
    
    5: Вывести просроченные срества измерения или с истекающим сроком поверки(менее 30 дней)"""
    bot.send_message(message.from_user.id, mes, reply_markup=markup)
    bot.register_next_step_handler(message, main_menu)
    
def main_menu(message):

    if message.text == "1: Внести средство измерения":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('1: Из списка', '2: Вручную')

        mes = """Внести СИ из списка или вручную?

    1: Из списка

    2: Вручную"""


        bot.send_message(message.from_user.id, mes, reply_markup=markup)
        bot.register_next_step_handler(message, list_or_hand_insert)
        
    elif message.text == "2: Редактировать/Удалить":
        bot.send_message(message.from_user.id, "Введите название средства измерения")
        bot.register_next_step_handler(message, change_del_type)

    elif message.text == "3: Вывести все СИ": # вывод всех сразу здесь
        res = db.measuring_tools.find()
        if res is None:
            bot.send_message(message.from_user.id,"Ни одного средства измерения в базе не найдено")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('/start')
            bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
            return
        else:
            for i in res:
                date = i["verification_date"]
                ver_delta = date - datetime.now()

                if ver_delta.days <= 0:
                    bot.send_message(message.from_user.id, str(i["type"]) + "   Зав.№: " + str(i["id_num"])  +'\n' + "Дата сл.поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "Просрочено: " + str(ver_delta.days) + " дней")
                else:
                    bot.send_message(message.from_user.id, str(i["type"]) + "   Зав.№: " + str(i["id_num"])  +'\n' + "Дата сл.поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "Количество дней до поверки: " + str(ver_delta.days))
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('/start')
            bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
            return
    
    elif message.text == "4: Вывести один тип СИ":
        bot.send_message(message.from_user.id, "Средство измерения какого типа следует вывести?")
        bot.register_next_step_handler(message, output_one)

    elif message.text == "5: Вывести истекающие/Просроченые":

        res = db.measuring_tools.find()
        check = False

        if res is None:
            bot.send_message(message.from_user.id,"Ни одного средства измерения в базе не найдено")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('/start')
            bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
            return
        else:
            for i in res:
                date = i["verification_date"]
                ver_delta = date - datetime.now()

                if ver_delta.days <= 0:
                    check = True
                    bot.send_message(message.from_user.id, str(i["type"]) + "   Зав.№: " + str(i["id_num"])  +'\n' + "Дата сл.поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "Просрочено: " + str(ver_delta.days) + " дней")
                elif ver_delta.days <= 30:
                    check = True
                    bot.send_message(message.from_user.id, str(i["type"]) + "   Зав.№: " + str(i["id_num"])  +'\n' + "Дата сл.поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "Количество дней до поверки: " + str(ver_delta.days))
            if check == True:
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.add('/start')
                bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)

        if check == False:
            bot.send_message(message.from_user.id, "Просроченных средств измерения или средств измерения со сроком поверки, истекающим менее, чем через 30 дней - не найдено")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('/start')
            bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
            return
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        bot.send_message(message.from_user.id, "Некорректное значение", reply_markup=markup)
        bot.send_message(message.from_user.id, "Перейти в главное меню?")
        return

# Функция внести средство измерения        
def list_or_hand_insert(message):

    if message.text == "1: Из списка":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('1: Мерник', '2: Метрошток', '3: Секундомер', '4: Весы')
        mes = """Какое средство измерения внести в базу? Выберите и введите вариант:

    1: Мерник

    2: Метрошток

    3: Секундомер

    4: Весы"""

        bot.send_message(message.from_user.id, mes, reply_markup=markup)
        bot.register_next_step_handler(message, list_insert_option)

    elif message.text == "2: Вручную":
        bot.send_message(message.from_user.id, "Внесите название средства измерения")
        bot.register_next_step_handler(message, extra_insert_option_type)

    else:
        bot.send_message(message.from_user.id, "Некорректное значение")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
        return
    

# Группа функций добавления СИ по списку
def list_insert_option(message):
    if message.text == "1: Мерник":
        bot.send_message(message.from_user.id, "Введите уникальный заводской номер Мерника:")
        bot.register_next_step_handler(message, mernik_num)
    elif message.text == "2: Метрошток":
        bot.send_message(message.from_user.id, "Введите уникальный заводской номер Метроштока:")
        bot.register_next_step_handler(message, mtrshk_num)
    elif message.text == "3: Секундомер":
        bot.send_message(message.from_user.id, "Введите уникальный заводской номер Секундомера:")
        bot.register_next_step_handler(message, sekndmr_num)
    elif message.text == "4: Весы":
        bot.send_message(message.from_user.id, "Введите уникальный заводской номер Весов:")
        bot.register_next_step_handler(message, ves_num)
    else:
        bot.send_message(message.from_user.id, "Некорректное значение")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
        return

def mernik_num(message):
    global num
    num = message.text
    if db.measuring_tools.find_one({"type":"Мерник", "id_num":num}) is None:
        bot.send_message(message.from_user.id, "Введите дату следующей поверки")
        bot.register_next_step_handler(message, mernik_date)
    else:
        bot.send_message(message.from_user.id, "Средство измерения данного типа с таким номером уже существует")
        return
def mernik_date(message):
    mounthes = {"январь":1, "января":1, "янв":1, "февраль":2, "февраля":2, "фев":2, "март":3, "марта":3, "мар":3, "апрель":4, "апреля":4, "апр":4, "май":5, "мая":5, "июнь":6, "июня":6, "июль":7, "июля":7, "август":8, "августа":8, "авг":8, "сентябрь":9, "сентября":9, "сент":9, "сен":9, "октября":10, "октябрь":10, "окт":10, "ноября":11, "ноябрь":11, "нояб":11, "декабрь":12, "декабря":12, "дек":12}

    
    date_list = []
    
    date = message.text
    
    if date.count(" ") >= 2:
        for i in date.split(" "):
            date_list.append(i)
    elif date.count(".") >= 2:
        for i in date.split("."):
            date_list.append(i)
    elif date.count("-") >= 2:
        for i in date.split("-"):
            date_list.append(i)
    elif date.count("/") >= 2:
        for i in date.split("/"):
            date_list.append(i)
    else:
        bot.send_message(message.from_user.id, "Некорректный ввод")
        bot.register_next_step_handler(message, mernik_date)
        return


    if date_list[1].lower() in mounthes:
        date_list[1] = mounthes[date_list[1].lower()]

    for i in range(len(date_list)):
        date_list[i] = int(date_list[i])


    if date_list[0] < 1 or date_list[0] > 31:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректное число")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, mernik_date)
        return
    elif date_list[1] < 1 or date_list[1] > 12:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректный месяц")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, mernik_date)
        return
    elif date_list[2] < 0:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректный год")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, mernik_date)
        return
    elif date_list[2] < 99:
        date_list[2] = 2000 + date_list[2]

    ready_date = ('-'.join([str(i) for i in date_list]))
    date = datetime.strptime(ready_date, '%d-%m-%Y')
    
    db.measuring_tools.insert_one({"id_num":num, "type":"Мерник", "verification_date":date})
    bot.send_message(message.from_user.id, "===============================" +'\n' + "Мерник" + "   Зав.№: " + str(num) + "            Внесено" +'\n' + "Дата поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "===============================")
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('/start')
    bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
    return          
def mtrshk_num(message):
    global num
    num = message.text
    if db.measuring_tools.find_one({"type":"Метрошток", "id_num":num}) is None:
        bot.send_message(message.from_user.id, "Введите дату следующей поверки")
        bot.register_next_step_handler(message, mtrshk_date)
    else:
        bot.send_message(message.from_user.id, "Средство измерения данного типа с таким номером уже существует")
        return
def mtrshk_date(message):
    mounthes = {"январь":1, "января":1, "янв":1, "февраль":2, "февраля":2, "фев":2, "март":3, "марта":3, "мар":3, "апрель":4, "апреля":4, "апр":4, "май":5, "мая":5, "июнь":6, "июня":6, "июль":7, "июля":7, "август":8, "августа":8, "авг":8, "сентябрь":9, "сентября":9, "сент":9, "сен":9, "октября":10, "октябрь":10, "окт":10, "ноября":11, "ноябрь":11, "нояб":11, "декабрь":12, "декабря":12, "дек":12}

    
    date_list = []
    
    date = message.text
    
    if date.count(" ") >= 2:
        for i in date.split(" "):
            date_list.append(i)
    elif date.count(".") >= 2:
        for i in date.split("."):
            date_list.append(i)
    elif date.count("-") >= 2:
        for i in date.split("-"):
            date_list.append(i)
    elif date.count("/") >= 2:
        for i in date.split("/"):
            date_list.append(i)
    else:
        bot.send_message(message.from_user.id, "Некорректный ввод")
        bot.register_next_step_handler(message, mtrshk_date)
        return


    if date_list[1].lower() in mounthes:
        date_list[1] = mounthes[date_list[1].lower()]

    for i in range(len(date_list)):
        date_list[i] = int(date_list[i])


    if date_list[0] < 1 or date_list[0] > 31:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректное число")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, mtrshk_date)
        return
    elif date_list[1] < 1 or date_list[1] > 12:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректный месяц")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, mtrshk_date)
        return
    elif date_list[2] < 0:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректный год")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, mtrshk_date)
        return
    elif date_list[2] < 99:
        date_list[2] = 2000 + date_list[2]

    ready_date = ('-'.join([str(i) for i in date_list]))
    date = datetime.strptime(ready_date, '%d-%m-%Y')
    
    db.measuring_tools.insert_one({"id_num":num, "type":"Метрошток", "verification_date":date})
    bot.send_message(message.from_user.id, "===============================" +'\n' + "Метрошток" + "   Зав.№: " + str(num) + "          Внесено" +'\n' + "Дата поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "===============================")
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('/start')
    bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
    return
def sekndmr_num(message):
    global num
    num = message.text
    if db.measuring_tools.find_one({"type":"Секундомер", "id_num":num}) is None:
        bot.send_message(message.from_user.id, "Введите дату следующей поверки")
        bot.register_next_step_handler(message, sekndmr_date)
    else:
        bot.send_message(message.from_user.id, "Средство измерения данного типа с таким номером уже существует")
        return
def sekndmr_date(message):
    mounthes = {"январь":1, "января":1, "янв":1, "февраль":2, "февраля":2, "фев":2, "март":3, "марта":3, "мар":3, "апрель":4, "апреля":4, "апр":4, "май":5, "мая":5, "июнь":6, "июня":6, "июль":7, "июля":7, "август":8, "августа":8, "авг":8, "сентябрь":9, "сентября":9, "сент":9, "сен":9, "октября":10, "октябрь":10, "окт":10, "ноября":11, "ноябрь":11, "нояб":11, "декабрь":12, "декабря":12, "дек":12}

    
    date_list = []
    
    date = message.text
    
    if date.count(" ") >= 2:
        for i in date.split(" "):
            date_list.append(i)
    elif date.count(".") >= 2:
        for i in date.split("."):
            date_list.append(i)
    elif date.count("-") >= 2:
        for i in date.split("-"):
            date_list.append(i)
    elif date.count("/") >= 2:
        for i in date.split("/"):
            date_list.append(i)
    else:
        bot.send_message(message.from_user.id, "Некорректный ввод")
        bot.register_next_step_handler(message, sekndmr_date)
        return


    if date_list[1].lower() in mounthes:
        date_list[1] = mounthes[date_list[1].lower()]

    for i in range(len(date_list)):
        date_list[i] = int(date_list[i])


    if date_list[0] < 1 or date_list[0] > 31:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректное число")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, sekndmr_date)
        return
    elif date_list[1] < 1 or date_list[1] > 12:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректный месяц")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, sekndmr_date)
        return
    elif date_list[2] < 0:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректный год")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, sekndmr_date)
        return
    elif date_list[2] < 99:
        date_list[2] = 2000 + date_list[2]

    ready_date = ('-'.join([str(i) for i in date_list]))
    date = datetime.strptime(ready_date, '%d-%m-%Y')
    
    db.measuring_tools.insert_one({"id_num":num, "type":"Секундомер", "verification_date":date})
    bot.send_message(message.from_user.id, "===============================" +'\n' + "Секундомер" + "   Зав.№: " + str(num) + "      Внесено" +'\n' + "Дата поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "===============================")
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('/start')
    bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
    return                      
def ves_num(message):
    global num
    num = message.text
    if db.measuring_tools.find_one({"type":"Весы", "id_num":num}) is None:
        bot.send_message(message.from_user.id, "Введите дату следующей поверки")
        bot.register_next_step_handler(message, ves_date)
    else:
        bot.send_message(message.from_user.id, "Средство измерения данного типа с таким номером уже существует")
        return
def ves_date(message):
    mounthes = {"январь":1, "января":1, "янв":1, "февраль":2, "февраля":2, "фев":2, "март":3, "марта":3, "мар":3, "апрель":4, "апреля":4, "апр":4, "май":5, "мая":5, "июнь":6, "июня":6, "июль":7, "июля":7, "август":8, "августа":8, "авг":8, "сентябрь":9, "сентября":9, "сент":9, "сен":9, "октября":10, "октябрь":10, "окт":10, "ноября":11, "ноябрь":11, "нояб":11, "декабрь":12, "декабря":12, "дек":12}

    
    date_list = []
    
    date = message.text
    
    if date.count(" ") >= 2:
        for i in date.split(" "):
            date_list.append(i)
    elif date.count(".") >= 2:
        for i in date.split("."):
            date_list.append(i)
    elif date.count("-") >= 2:
        for i in date.split("-"):
            date_list.append(i)
    elif date.count("/") >= 2:
        for i in date.split("/"):
            date_list.append(i)
    else:
        bot.send_message(message.from_user.id, "Некорректный ввод")
        bot.register_next_step_handler(message, ves_date)
        return


    if date_list[1].lower() in mounthes:
        date_list[1] = mounthes[date_list[1].lower()]

    for i in range(len(date_list)):
        date_list[i] = int(date_list[i])


    if date_list[0] < 1 or date_list[0] > 31:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректное число")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, ves_date)
        return
    elif date_list[1] < 1 or date_list[1] > 12:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректный месяц")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, ves_date)
        return
    elif date_list[2] < 0:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректный год")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, ves_date)
        return
    elif date_list[2] < 99:
        date_list[2] = 2000 + date_list[2]

    ready_date = ('-'.join([str(i) for i in date_list]))
    date = datetime.strptime(ready_date, '%d-%m-%Y')
    
    db.measuring_tools.insert_one({"id_num":num, "type":"Весы", "verification_date":date})
    bot.send_message(message.from_user.id, "===============================" +'\n' + "Весы" + "   Зав.№: " + str(num) + "              Внесено" +'\n' + "Дата поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "===============================")
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('/start')
    bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
    return
         
#Группа функций добавления СИ вручную - пользователь сам вносит название
def extra_insert_option_type(message):
    global type
    type = message.text
    bot.send_message(message.from_user.id, "Введите уникальный заводской номер средства измерения")
    bot.register_next_step_handler(message, extra_insert_option_num)
def extra_insert_option_num(message):  #  
    global num
    num = message.text
    if db.measuring_tools.find_one({"type":type, "id_num":num}) is None:
        bot.send_message(message.from_user.id, "Введите дату следующей поверки")
        bot.register_next_step_handler(message, extra_insert_option_date)
    else:
        bot.send_message(message.from_user.id, "Средство измерения данного типа с таким номером уже существует")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
        return              
def extra_insert_option_date(message):
    mounthes = {"январь":1, "января":1, "янв":1, "февраль":2, "февраля":2, "фев":2, "март":3, "марта":3, "мар":3, "апрель":4, "апреля":4, "апр":4, "май":5, "мая":5, "июнь":6, "июня":6, "июль":7, "июля":7, "август":8, "августа":8, "авг":8, "сентябрь":9, "сентября":9, "сент":9, "сен":9, "октября":10, "октябрь":10, "окт":10, "ноября":11, "ноябрь":11, "нояб":11, "декабрь":12, "декабря":12, "дек":12}

    
    date_list = []
    
    date = message.text
    
    if date.count(" ") >= 2:
        for i in date.split(" "):
            date_list.append(i)
    elif date.count(".") >= 2:
        for i in date.split("."):
            date_list.append(i)
    elif date.count("-") >= 2:
        for i in date.split("-"):
            date_list.append(i)
    elif date.count("/") >= 2:
        for i in date.split("/"):
            date_list.append(i)
    else:
        bot.send_message(message.from_user.id, "Некорректный ввод")
        bot.register_next_step_handler(message, extra_insert_option_date)
        return


    if date_list[1].lower() in mounthes:
        date_list[1] = mounthes[date_list[1].lower()]

    for i in range(len(date_list)):
        date_list[i] = int(date_list[i])


    if date_list[0] < 1 or date_list[0] > 31:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректное число")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, extra_insert_option_date)
        return
    elif date_list[1] < 1 or date_list[1] > 12:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректный месяц")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, extra_insert_option_date)
        return
    elif date_list[2] < 0:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректный год")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, extra_insert_option_date)
        return
    elif date_list[2] < 99:
        date_list[2] = 2000 + date_list[2]

    ready_date = ('-'.join([str(i) for i in date_list]))
    date = datetime.strptime(ready_date, '%d-%m-%Y')
    
    db.measuring_tools.insert_one({"id_num":num, "type":type, "verification_date":date})
    bot.send_message(message.from_user.id, "===============================" +'\n' + str(type) + "   Зав.№: " + str(num) + "           Внесено" +'\n' + "Дата поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "===============================")
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('/start')
    bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
    return
     
# Внести/Удалить - тип
def change_del_type(message):
    global type
    type = message.text
    bot.send_message(message.from_user.id, "Введите уникальный заводской номер средства измерения")
    bot.register_next_step_handler(message, change_del_num)
# Внести/Удалить - номер
def change_del_num(message):  #  
    global num
    num = message.text
    if db.measuring_tools.find_one({"type":type, "id_num":num}) is None:        
        bot.send_message(message.from_user.id, "Средства измерения с такими параметрами не найдено")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
        return  
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('1: Внести дату поверки', '2: Удалить')
        res = db.measuring_tools.find_one({"type":type, "id_num":num})
        date = res["verification_date"]
        bot.send_message(message.from_user.id, "===============================" +'\n' + str(type) + "   Зав.№: " + str(num)  +'\n' + "Дата следующей поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "===============================")
        mes = """Удалить СИ из базы или внести новую дату поверки?

    1: Внести дату поверки

    2: Удалить"""
        bot.send_message(message.from_user.id, mes, reply_markup=markup)
        bot.register_next_step_handler(message, change_del_choise)
# Внести/Удалить - выбор
def change_del_choise(message):
    if message.text == "1: Внести дату поверки":
        bot.send_message(message.from_user.id, "Внесите новую дату поверки")
        bot.register_next_step_handler(message, change_del_date)
    elif message.text == "2: Удалить":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('1: Подтвердить', '2: Отменить')
        mes = """Удалить ?

    1: Подтвердить

    2: Отменить"""
        bot.send_message(message.from_user.id, mes, reply_markup=markup)
        bot.register_next_step_handler(message, change_del_delete)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        bot.send_message(message.from_user.id, "Некорректное значение", reply_markup=markup)
        bot.send_message(message.from_user.id, "Перейти в главное меню?")
        return
# Внести новую дату
def change_del_date(message):
    mounthes = {"январь":1, "января":1, "янв":1, "февраль":2, "февраля":2, "фев":2, "март":3, "марта":3, "мар":3, "апрель":4, "апреля":4, "апр":4, "май":5, "мая":5, "июнь":6, "июня":6, "июль":7, "июля":7, "август":8, "августа":8, "авг":8, "сентябрь":9, "сентября":9, "сент":9, "сен":9, "октября":10, "октябрь":10, "окт":10, "ноября":11, "ноябрь":11, "нояб":11, "декабрь":12, "декабря":12, "дек":12}

    
    date_list = []
    
    date = message.text
    
    if date.count(" ") >= 2:
        for i in date.split(" "):
            date_list.append(i)
    elif date.count(".") >= 2:
        for i in date.split("."):
            date_list.append(i)
    elif date.count("-") >= 2:
        for i in date.split("-"):
            date_list.append(i)
    elif date.count("/") >= 2:
        for i in date.split("/"):
            date_list.append(i)
    else:
        bot.send_message(message.from_user.id, "Некорректный ввод")
        bot.register_next_step_handler(message, change_del_date)
        return


    if date_list[1].lower() in mounthes:
        date_list[1] = mounthes[date_list[1].lower()]

    for i in range(len(date_list)):
        date_list[i] = int(date_list[i])


    if date_list[0] < 1 or date_list[0] > 31:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректное число")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, change_del_date)
        return
    elif date_list[1] < 1 or date_list[1] > 12:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректный месяц")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, change_del_date)
        return
    elif date_list[2] < 0:
        bot.send_message(message.from_user.id, "Некорректный ввод: некорректный год")
        bot.send_message(message.from_user.id, "Введите дату повторно:")
        bot.register_next_step_handler(message, change_del_date)
        return
    elif date_list[2] < 99:
        date_list[2] = 2000 + date_list[2]

    ready_date = ('-'.join([str(i) for i in date_list]))
    date = datetime.strptime(ready_date, '%d-%m-%Y')
    
    db.measuring_tools.update_one({"type":type, "id_num":num},{"$set":{"verification_date":date}})
    bot.send_message(message.from_user.id, "===============================" +'\n' + str(type) + "   Зав.№: " + str(num) + "           Обновлено" +'\n' + "Новая дата поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "===============================")
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('/start')
    bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
    return
# Удалить
def change_del_delete(message):
    if message.text == "1: Подтвердить":
        res = db.measuring_tools.find_one({"type":type, "id_num":num})
        date = res["verification_date"]
        db.measuring_tools.delete_one({"type":type, "id_num":num})
        bot.send_message(message.from_user.id, "===============================" +'\n' + str(type) + "   Зав.№: " + str(num) + "           УДАЛЕНО" +'\n' + "Дата поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "===============================")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        bot.send_message(message.from_user.id, "Отменено", reply_markup=markup)
        date = None
        return


# Функцкия вывода СИ конкретного типа
def output_one(message):
    choise_type = message.text

    res = db.measuring_tools.find({"type":choise_type})
    if res is None:
        bot.send_message(message.from_user.id, "Ни одного средства измерения в базе не найдено")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
        return
    else:
        for i in res:
            date = i["verification_date"]
            ver_delta = date - datetime.now()

            if ver_delta.days <= 0:
                bot.send_message(message.from_user.id, str(i["type"]) + "   Зав.№: " + str(i["id_num"])  +'\n' + "Дата сл.поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "Просрочено: " + str(ver_delta.days) + " дней")
            else:
                bot.send_message(message.from_user.id, str(i["type"]) + "   Зав.№: " + str(i["id_num"])  +'\n' + "Дата сл.поверки: " + str(date.strftime('%d-%m-%Y')) +'\n' + "Количество дней до поверки: " + str(ver_delta.days))
        
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('/start')
    bot.send_message(message.from_user.id, "Перейти в главное меню?", reply_markup=markup)
    return


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling()
