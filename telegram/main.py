import telebot
import threading
import time
from datetime import datetime
import webbrowser as wb
import requests

# Импорт настроек
print("[LOG] Importing settings...", end="")
import settings
print(" Done!")

print("[LOG] Connecting bot token...", end="")
bot = telebot.TeleBot('7285599484:AAECj2fMmK_B60tUxLDF_wcfFVCs1vfO-vc')
bot.remove_webhook()
print(" Done!")

chat_ids = set()

main_button = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('📉 Exchange')
button_2 = telebot.types.KeyboardButton('⛅️ Weather')
button_3 = telebot.types.KeyboardButton('🛠️ Settings')
main_button.row(button_1, button_2, button_3)

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
    
    setting_button.row(button_1, button_2)
    return setting_button

setting_button = update_main_button()

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