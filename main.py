import telebot, constants, requests, json
from telebot import types

bot = telebot.TeleBot(constants.token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привіт! Я Lviv Transport Bot, моя ціль - вказувати час до прибуття громадського транспорту. Просто введи код зупинки і все побачиш." + "\n" + "Все ще є запитання? Натисни /help")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "У Львові кожна зупинка має код і якщо відправити цей код цьому боту, він вкаже час до прибуття громадського транспорту. Приклад, де можна побачити цей код, є на фото")
    bot.send_photo(message.chat.id,
                   photo='https://lh4.googleusercontent.com/__SzhlXT47vOhyJAH2SF61X87Q03Ray5HdLQhKUawiuxf7dKLfNihajpxE_Lc62hIxTHGcogiJd71aKIeVXv=w1366-h657')


@bot.message_handler(commands=['about'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Дані для обробки беруться з сайту https://lad.lviv.ua/. Інформація постійно оновлюється для кожного автобусу трамваю чи тролейбусу і у більшості випадків є досить точною. За будь якими питаннями звертатись - @kahitin")


@bot.message_handler(func=lambda message: True)
def main_func(message):
    try:
        chat_id = message.chat.id
        global a
        a = message.text
        global mssgg
        mssgg = message
        pre_url = a
        url = "https://lad.lviv.ua/api/stops/" + pre_url
        r = requests.get(url)
        json_data = json.loads(r.content)
        stop_code = json_data["name"]
        bus_stop = json_data["code"]
        current_number = len(json_data["timetable"])
        i = 0
        d = {}
        big_data = ""
        if current_number == 0:
            big_data += "В даний момент маршруток немає!" + "\n"
        while i < current_number:
            globals()['bus_numb%s' % i] = json_data["timetable"][i]["route"]
            globals()['time_to%s' % i] = json_data["timetable"][i]["time_left"]
            globals()['info_line%s' % i] = globals()['bus_numb%s' % i] + " через " + globals()['time_to%s' % i]
            if json_data["timetable"][i]["vehicle_type"] == 'tram':
                globals()['info_line%s' % i] = u'\U0001F683' + " " + globals()['info_line%s' % i]
            if json_data["timetable"][i]["vehicle_type"] == 'bus':
                globals()['info_line%s' % i] = u"\U0001F68C" + " " + globals()['info_line%s' % i]
            if json_data["timetable"][i]["vehicle_type"] == 'trol':
                globals()['info_line%s' % i] = u"\U0001F68E" + " " + globals()['info_line%s' % i]
            big_data += globals()['info_line%s' % i] + "\n"
            i += 1
        full_info = str(stop_code) + " ( № " + str(bus_stop) + " )" + "\n" + "\n" + str(big_data)
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Оновити", callback_data="test")
        keyboard.add(callback_button)
        bot.send_message(message.chat.id, full_info, reply_markup=keyboard)
        return full_info
    except:
        bot.send_message(message.chat.id, "Ви ввели щось неправильно, спробуйте знову  \nЯк працює бот - /help")


def info_upd(message):
    chat_id = message.chat.id
    global chat_in
    chat_in = message.chat.id
    global a
    a = message.text
    global mssgg
    mssgg = message
    pre_url = a
    url = "https://lad.lviv.ua/api/stops/" + pre_url
    r = requests.get(url)
    json_data = json.loads(r.content)
    stop_code = json_data["name"]
    bus_stop = json_data["code"]
    current_number = len(json_data["timetable"])
    i = 0
    d = {}
    big_data = ""
    if current_number == 0:
        big_data += "В даний момент маршруток немає!" + "\n"
    while i < current_number:
        globals()['bus_numb%s' % i] = json_data["timetable"][i]["route"]
        globals()['time_to%s' % i] = json_data["timetable"][i]["time_left"]
        globals()['info_line%s' % i] = globals()['bus_numb%s' % i] + " через " + globals()['time_to%s' % i]
        if json_data["timetable"][i]["vehicle_type"] == 'tram':
            globals()['info_line%s' % i] = u'\U0001F683' + " " + globals()['info_line%s' % i]
        if json_data["timetable"][i]["vehicle_type"] == 'bus':
            globals()['info_line%s' % i] = u"\U0001F68C" + " " + globals()['info_line%s' % i]
        if json_data["timetable"][i]["vehicle_type"] == 'trol':
            globals()['info_line%s' % i] = u"\U0001F68E" + " " + globals()['info_line%s' % i]
        big_data += globals()['info_line%s' % i] + "\n"
        i += 1
    full_info = str(stop_code) + " ( № " + str(bus_stop) + " )" + "\n" + "\n" + str(big_data)
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Оновити", callback_data="test")
    keyboard.add(callback_button)
    return full_info


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "test":
            keyboard2 = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="Оновити", callback_data="test2")
            keyboard2.add(callback_button)
            bot.edit_message_text(text=info_upd(mssgg), chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=keyboard2)
        if call.data == "test2":
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="Оновити", callback_data="test")
            keyboard.add(callback_button)
            bot.edit_message_text(text=info_upd(mssgg), chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)



