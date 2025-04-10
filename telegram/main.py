import telebot
import threading
import time
from datetime import datetime
import webbrowser as wb
import requests

# Импорт настроек
print("[LOG] Importing settings...")
import settings

print("[LOG] Connecting bot token...")
bot = telebot.TeleBot('7285599484:AAECj2fMmK_B60tUxLDF_wcfFVCs1vfO-vc')
bot.remove_webhook()

chat_ids = set()

# 1 страница
main_button_1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('📉 Exchange')
button_2 = telebot.types.KeyboardButton('⛅️ Weather')
button_3 = telebot.types.KeyboardButton('🛠️ Settings')
button_4 = telebot.types.KeyboardButton('ℹ️ My info')
button_page_1 = telebot.types.KeyboardButton('➡️ 2 страница')
button_page_2 = telebot.types.KeyboardButton('⬅️ 3 страница')
main_button_1.row(button_4, button_1, button_2, button_3)
main_button_1.row(button_page_2, button_page_1)

# 2 страница
main_button_2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('🎹 Music')
button_2 = telebot.types.KeyboardButton('👾 Game')
button_page_1 = telebot.types.KeyboardButton('➡️ 3 страница')
button_page_2 = telebot.types.KeyboardButton('⬅️ 1 страница')
main_button_2.row(button_1, button_2)
main_button_2.row(button_page_2, button_page_1)

# 3 страница
main_button_3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('⏳ Timer')
button_2 = telebot.types.KeyboardButton('🧠 Reminder')
button_3 = telebot.types.KeyboardButton('📆 Schedule')
button_4 = telebot.types.KeyboardButton('📝 Notes')
button_page_1 = telebot.types.KeyboardButton('➡️ 4 страница')
button_page_2 = telebot.types.KeyboardButton('⬅️ 2 страница')
main_button_3.row(button_1)
main_button_3.row(button_page_2, button_page_1)

# 4 страница
main_button_4 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('🏠 Home')
button_2 = telebot.types.KeyboardButton('🌑 Night')
button_3 = telebot.types.KeyboardButton('💤 Sleep')
button_4 = telebot.types.KeyboardButton('🧠 Hmmmm')
button_5 = telebot.types.KeyboardButton('💼 Work')
button_page_1 = telebot.types.KeyboardButton('➡️ 1 страница')
button_page_2 = telebot.types.KeyboardButton('⬅️ 3 страница')
main_button_4.row(button_1, button_2, button_3)
main_button_4.row(button_4, button_5)
main_button_4.row(button_page_2, button_page_1)

music_button = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('🛞 Phonk')
button_2 = telebot.types.KeyboardButton('🌚 Аtmospheric phonk')
button_3 = telebot.types.KeyboardButton('🇧🇷 Brazzilian phonk')
button_4 = telebot.types.KeyboardButton('🎹 Piano')
button_5 = telebot.types.KeyboardButton('🎻 Classic')
button_6 = telebot.types.KeyboardButton('😕 Melancholy')
button_random = telebot.types.KeyboardButton('🎲 Random')
button_exit = telebot.types.KeyboardButton('⬅️ Exit')
music_button.row(button_1, button_2, button_3)
music_button.row(button_4, button_5, button_6)
music_button.row(button_random)
music_button.row(button_exit)

# Настройки
def update_main_button():
    print("[LOG] Updating settings keyboard...")
    setting_button = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if settings.youtube_music:
        button_1 = telebot.types.KeyboardButton('🟢 YouTube')
    else:
        button_1 = telebot.types.KeyboardButton('🔴 YouTube')

    if settings.morning:
        button_2 = telebot.types.KeyboardButton('🟢 Morning')
    else:
        button_2 = telebot.types.KeyboardButton('🔴 Morning')
    
    button_exit = telebot.types.KeyboardButton('⬅️ Exit')
    setting_button.row(button_1, button_2)
    setting_button.row(button_exit)
    return setting_button

setting_button = update_main_button()


@bot.message_handler(regexp='1 страница')
def page(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "1 страница", reply_markup=main_button_1)

@bot.message_handler(regexp='2 страница')
def page(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "2 страница", reply_markup=main_button_2)

@bot.message_handler(regexp='3 страница')
def page(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "3 страница", reply_markup=main_button_3)

@bot.message_handler(regexp='4 страница')
def page(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "4 страница", reply_markup=main_button_4)

@bot.message_handler(regexp='Settings')
def page(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "Настройки", reply_markup=setting_button)

@bot.message_handler(regexp='Exit')
def page(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "1 страница", reply_markup=main_button_1)

@bot.message_handler(regexp='Music')
def page_music(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "🔵🔴 Выбери жанр музыки", reply_markup=music_button)



def save_settings():
    print("[LOG] Saving settings to file...")
    with open('settings.py', 'w') as f:
        f.write(f'youtube_music = {settings.youtube_music}\n')
        f.write(f'morning = {settings.morning}\n')

@bot.message_handler(regexp='/start')
def start(command):
    print(f"[LOG] /start command from user {command.chat.id}")
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, 'Привет, я С.О.Ф.И.Я', reply_markup=main_button)
    chat_ids.add(command.chat.id)

@bot.message_handler(regexp='Youtube')
def youtube(command):
    print(f"[LOG] YouTube toggle from user {command.chat.id}")
    bot.delete_message(command.chat.id, command.id)
    settings.youtube_music = not settings.youtube_music
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, '⚙️ Настройки YouTube обновлены', reply_markup=updated_markup)
    chat_ids.add(command.chat.id)

@bot.message_handler(regexp='Morning')
def morning(command):
    print(f"[LOG] Morning toggle from user {command.chat.id}")
    bot.delete_message(command.chat.id, command.id)
    settings.morning = not settings.morning
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, '⚙️ Настройки Morning обновлены', reply_markup=updated_markup)
    chat_ids.add(command.chat.id)

@bot.message_handler(regexp="Weather")
def weather(command):
    print(f"[LOG] Weather request from user {command.chat.id}")
    try:
        city = "Якутск"
        print(f"[LOG] Fetching weather for {city}")
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=942343b4877c75d7775a5cda76fd1bc6&units=metric")
        data = response.json()
        bot.delete_message(command.chat.id, command.id)
        bot.send_message(command.chat.id, f"⛅️ Погода в {city}: {data['main']['temp']}°C")
    except Exception as e:
        print(f"[ERROR] Weather API error: {e}")
        bot.send_message(command.chat.id, "🛑 Не удалось получить данные о погоде")

@bot.message_handler(regexp="Exchange")
def exchange(command):
    print(f"[LOG] Exchange rate request from user {command.chat.id}")
    try:
        print("[LOG] Fetching USD to RUB exchange rate")
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()
        bot.delete_message(command.chat.id, command.id)
        bot.send_message(command.chat.id, f"💸 1 USD = {data['rates']['RUB']} RUB")
    except Exception as e:
        print(f"[ERROR] Exchange API error: {e}")
        bot.reply_to(command, "🛑 Не удалось получить курс валют")


def send_messages():
    print("[LOG] Starting scheduled messages service")
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        if current_time == "05:25":
            print("[LOG] Morning message time triggered (05:25)")
            if settings.morning:
                print(f"[LOG] Sending morning messages to {len(chat_ids)} users")
                for chat_id in chat_ids:
                    bot.send_message(chat_id, "Доброе утро!")
                    if settings.youtube_music:
                        print("[LOG] Opening YouTube music")
                        wb.open("https://music.youtube.com/watch?v=dzqucn29zM4&list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
            time.sleep(60)

        elif current_time == "19:54":
            print("[LOG] Evening message time triggered (19:54)")
            print(f"[LOG] Sending evening messages to {len(chat_ids)} users")
            for chat_id in chat_ids:
                bot.send_message(chat_id, "Добрый день!")
            time.sleep(60)

        time.sleep(1)

print("[LOG] Starting background thread for scheduled messages")
threading.Thread(target=send_messages, daemon=True).start()

print("[LOG] Starting bot polling")
bot.polling()