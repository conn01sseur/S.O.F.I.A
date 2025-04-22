import telebot
import threading
import time
from datetime import datetime
import webbrowser as wb
import requests
import socket
import json

print("[LOG] Importing settings...")
import settings

print("[LOG] Initializing bot with API token...")
bot = telebot.TeleBot('7285599484:AAECj2fMmK_B60tUxLDF_wcfFVCs1vfO-vc')
bot.remove_webhook()

chat_ids = set()

host = "localhost"
port = 3333

def socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[SOCKET] Server is listening on {host}:{port}")
    
    while True:
        conn, addr = server.accept()
        print(f"[SOCKET] Connection established from {addr}")
        
        try:
            data = conn.recv(1024).decode('utf-8')
            if data:
                print(f"[SOCKET] Received data: {data}")
                
                try:
                    message_data = json.loads(data)
                    chat_id = message_data.get('chat_id')
                    text = message_data.get('text')
                    
                    if chat_id and text:
                        bot.send_message(chat_id, f"🔌 From server: {text}")
                        print(f"[SOCKET] Forwarded message to chat {chat_id}")
                except json.JSONDecodeError:
                    print("[SOCKET] Received invalid JSON data")
                
                conn.send("Message received by server".encode('utf-8'))
        except Exception as e:
            print(f"[SOCKET ERROR] {e}")
        finally:
            conn.close()

# Запускаем сервер в отдельном потоке
socket_thread = threading.Thread(target=socket_server, daemon=True)
socket_thread.start()

print("[LOG] Creating keyboard layout - Page 1")
main_button_1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('📉 Exchange')
button_2 = telebot.types.KeyboardButton('⛅️ Weather')
button_3 = telebot.types.KeyboardButton('🛠️ Settings')
button_4 = telebot.types.KeyboardButton('ℹ️ My info')
button_page_1 = telebot.types.KeyboardButton('➡️ Page 2')
button_page_2 = telebot.types.KeyboardButton('⬅️ Page 3')
main_button_1.row(button_4, button_1, button_2, button_3)
main_button_1.row(button_page_2, button_page_1)

print("[LOG] Creating keyboard layout - Page 2")
main_button_2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('🎹 Music')
button_2 = telebot.types.KeyboardButton('👾 Game')
button_3 = telebot.types.KeyboardButton('🕹️ Control')
button_page_1 = telebot.types.KeyboardButton('➡️ Page 3')
button_page_2 = telebot.types.KeyboardButton('⬅️ Page 1')
main_button_2.row(button_1, button_2, button_3)
main_button_2.row(button_page_2, button_page_1)

print("[LOG] Creating keyboard layout - Page 3")
main_button_3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('⏳ Timer')
button_2 = telebot.types.KeyboardButton('🧠 Reminder')
button_3 = telebot.types.KeyboardButton('📆 Schedule')
button_4 = telebot.types.KeyboardButton('📝 Notes')
button_page_1 = telebot.types.KeyboardButton('➡️ Page 4')
button_page_2 = telebot.types.KeyboardButton('⬅️ Page 2')
main_button_3.row(button_1, button_2, button_3, button_4)
main_button_3.row(button_page_2, button_page_1)

print("[LOG] Creating keyboard layout - Page 4")
main_button_4 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('🏠 Home')
button_2 = telebot.types.KeyboardButton('🚫 No message')
button_3 = telebot.types.KeyboardButton('💤 Sleep')
button_4 = telebot.types.KeyboardButton('🧠 Hmmmm')
button_5 = telebot.types.KeyboardButton('💼 Work')
button_6 = telebot.types.KeyboardButton('☀️ Morning')
button_7 = telebot.types.KeyboardButton('🌑 Night')
button_page_1 = telebot.types.KeyboardButton('➡️ Page 1')
button_page_2 = telebot.types.KeyboardButton('⬅️ Page 3')
main_button_4.row(button_1, button_2, button_3)
main_button_4.row(button_4, button_5)
main_button_4.row(button_6, button_7)
main_button_4.row(button_page_2, button_page_1)

print("[LOG] Creating music selection keyboard")
music_button = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_phonk_1 = telebot.types.KeyboardButton('🛞 Phonk')
button_phonk_2 = telebot.types.KeyboardButton('🌚 Аtmospheric phonk')
button_phonk_3 = telebot.types.KeyboardButton('🇧🇷 Brazzilian phonk')
button_classic_1 = telebot.types.KeyboardButton('🎹 Piano')
button_classic_2 = telebot.types.KeyboardButton('🎻 Classic')
button_classic_3 = telebot.types.KeyboardButton('😕 Melancholy')
button_author_1 = telebot.types.KeyboardButton('🙂 Mac_demarco')
button_author_2 = telebot.types.KeyboardButton('xz')
button_rock_1 = telebot.types.KeyboardButton('🎸 Mute Rock')
button_rock_2 = telebot.types.KeyboardButton('🤘 Rock')
button_rock_3 = telebot.types.KeyboardButton('🫥 Dead Rock')
button_random = telebot.types.KeyboardButton('🎲 Random')
button_exit = telebot.types.KeyboardButton('⬅️ Exit')
music_button.row(button_phonk_1, button_phonk_2, button_phonk_3)
music_button.row(button_classic_1, button_classic_2, button_classic_3)
music_button.row(button_author_1, button_author_2)
music_button.row(button_rock_1, button_rock_2, button_rock_3)
music_button.row(button_random)
music_button.row(button_exit)

print("[LOG] Creating game control selection keyboard")
game_control = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('🎯 Select game')
button_2 = telebot.types.KeyboardButton('🌀 Optimization')
button_3 = telebot.types.KeyboardButton('🛸 Launcher')
button_exit = telebot.types.KeyboardButton('⬅️ Exit')
game_control.row(button_1, button_2, button_3)
game_control.row(button_exit)

print("[LOG] Creating control selection keyboard")
control_button = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('⏮️ Previous')
button_2 = telebot.types.KeyboardButton('⏯️ Play / Stop')
button_3 = telebot.types.KeyboardButton('⏭️ Next')
button_4 = telebot.types.KeyboardButton('🔉 - Volume')
button_5 = telebot.types.KeyboardButton('🔊 + Volume')
button_6 = telebot.types.KeyboardButton('🔇 Mute')
button_exit = telebot.types.KeyboardButton('⬅️ Exit')
control_button.row(button_1, button_2, button_3)
control_button.row(button_4, button_5, button_6)
control_button.row(button_exit)

def update_main_button():
    print("[LOG] Updating settings keyboard based on current configuration")
    setting_button = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if settings.youtube_music:
        button_1 = telebot.types.KeyboardButton('🟢 YouTube')
        print("[LOG] YouTube music setting is currently ENABLED")
    else:
        button_1 = telebot.types.KeyboardButton('🔴 YouTube')
        print("[LOG] YouTube music setting is currently DISABLED")

    if settings.morning:
        button_2 = telebot.types.KeyboardButton('🟢 Morning')
        print("[LOG] Morning notifications setting is currently ENABLED")
    else:
        button_2 = telebot.types.KeyboardButton('🔴 Morning')
        print("[LOG] Morning notifications setting is currently DISABLED")

    if settings.music_in_the_evening:
        button_3 = telebot.types.KeyboardButton('🟢 Music in the evening')
        print("[LOG] Music notifications setting is currently ENABLED")
    else:
        button_3 = telebot.types.KeyboardButton('🔴 Music in the evening')
        print("[LOG] Music notifications setting is currently DISABLED")
    
    button_exit = telebot.types.KeyboardButton('⬅️ Exit')
    setting_button.row(button_1, button_2)
    setting_button.row(button_3)
    setting_button.row(button_exit)
    return setting_button

setting_button = update_main_button()

@bot.message_handler(regexp='Page 1')
def page(command):
    print(f"[USER ACTION] User {command.chat.id} navigated to Page 1")
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "Page 1", reply_markup=main_button_1)

@bot.message_handler(regexp='Page 2')
def page(command):
    print(f"[USER ACTION] User {command.chat.id} navigated to Page 2")
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "Page 2", reply_markup=main_button_2)

@bot.message_handler(regexp='Page 3')
def page(command):
    print(f"[USER ACTION] User {command.chat.id} navigated to Page 3")
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "Page 3", reply_markup=main_button_3)

@bot.message_handler(regexp='Page 4')
def page(command):
    print(f"[USER ACTION] User {command.chat.id} navigated to Page 4")
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "Page 4", reply_markup=main_button_4)

@bot.message_handler(regexp='Exit')
def page(command):
    print(f"[USER ACTION] User {command.chat.id} exited current menu")
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "Page 1", reply_markup=main_button_1)

def save_settings():
    print("[LOG] Saving current settings to configuration file...")
    with open('settings.py', 'w') as f:
        f.write(f'youtube_music = {settings.youtube_music}\n')
        f.write(f'morning = {settings.morning}\n')
    print("[LOG] Settings successfully saved to file")

@bot.message_handler(regexp='/start')
def start(command):
    print(f"[USER ACTION] New session started by user {command.chat.id}")
    bot.send_message(command.chat.id, 'Hello, I am S.O.F.I.A', reply_markup=main_button_1)
    chat_ids.add(command.chat.id)
    print(f"[LOG] Added user {command.chat.id} to active sessions list")

@bot.message_handler(regexp='Youtube')
def youtube(command):
    print(f"[USER ACTION] User {command.chat.id} toggled YouTube setting")
    bot.delete_message(command.chat.id, command.id)
    settings.youtube_music = not settings.youtube_music
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, '⚙️ YouTube settings updated', reply_markup=updated_markup)
    print(f"[LOG] YouTube setting changed to: {settings.youtube_music}")

@bot.message_handler(regexp='Morning')
def morning(command):
    print(f"[USER ACTION] User {command.chat.id} toggled Morning setting")
    bot.delete_message(command.chat.id, command.id)
    settings.morning = not settings.morning
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, '⚙️ Morning settings updated', reply_markup=updated_markup)
    print(f"[LOG] Morning setting changed to: {settings.morning}")

@bot.message_handler(regexp='Music in the evening')
def music_in_the_evening(command):
    bot.delete_message(command.chat.id, command.id)
    settings.music_in_the_evening = not settings.music_in_the_evening
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, '⚙️ Music in the evening settings updated', reply_markup=updated_markup)
    print(f"[LOG] Music in the evening setting changed to: {settings.music_in_the_evening}")

@bot.message_handler(regexp="Phonk")
def music(command):
    print(f"[USER ACTION] User {command.chat.id} selected Phonk music")
    try:
        print("[ACTION] Opening Phonk playlist in browser")
        
    except Exception as e:
        print(f"[ERROR] Failed to open music playlist: {str(e)}")

# Page 1
@bot.message_handler(regexp="My info")
def info(command):
    pass

@bot.message_handler(regexp="Exchange")
def exchange(command):
    print(f"[USER ACTION] User {command.chat.id} requested exchange rates")
    try:
        print("[API REQUEST] Fetching USD to RUB exchange rate")
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()
        bot.delete_message(command.chat.id, command.id)
        bot.send_message(command.chat.id, f"💸 1 USD = {data['rates']['RUB']} RUB")
        print(f"[API RESPONSE] Current exchange rate: 1 USD = {data['rates']['RUB']} RUB")
    except Exception as e:
        print(f"[API ERROR] Exchange rate API request failed: {str(e)}")
        bot.reply_to(command, "🛑 Failed to retrieve exchange rates")

@bot.message_handler(regexp="Weather")
def weather(command):
    print(f"[USER ACTION] User {command.chat.id} requested weather information")
    try:
        city = "Yakutsk"
        print(f"[API REQUEST] Fetching weather data for {city}")
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=942343b4877c75d7775a5cda76fd1bc6&units=metric")
        data = response.json()
        bot.delete_message(command.chat.id, command.id)
        bot.send_message(command.chat.id, f"⛅️ Weather in {city}: {data['main']['temp']}°C")
        print(f"[API RESPONSE] Successfully retrieved weather data: {data['main']['temp']}°C")
    except Exception as e:
        print(f"[API ERROR] Weather API request failed: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to retrieve weather data")

@bot.message_handler(regexp='Settings')
def page(command):
    print(f"[USER ACTION] User {command.chat.id} opened Settings")
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "Settings", reply_markup=setting_button)

# Page 2
@bot.message_handler(regexp='Music')
def page_music(command):
    print(f"[USER ACTION] User {command.chat.id} opened Music selection")
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "🔵🔴 Select music genre", reply_markup=music_button)

@bot.message_handler(regexp="Game")
def game(command):
    pass

@bot.message_handler(regexp='Control')
def control(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "Control panel", reply_markup=control_button)

# Page 3
@bot.message_handler(regexp="Timer")
def timer(command):
    pass

@bot.message_handler(regexp="Reminder")
def reminder(command):
    pass

@bot.message_handler(regexp="Schedule")
def schedule(command):
    pass

@bot.message_handler(regexp="Notes")
def notes(command):
    pass

# Page 4
@bot.message_handler(regexp="Home")
def home(command):
    pass

@bot.message_handler(regexp="Night")
def night(command):
    pass

@bot.message_handler(regexp="Sleep")
def sleep(command):
    pass

@bot.message_handler(regexp="Hmmmm")
def hmmmm(command):
    pass

@bot.message_handler(regexp="Work")
def work(command):
    pass

# Control button
@bot.message_handler(regexp="Previous")
def previous(command):
    bot.delete_message(command.chat.id, command.id)

@bot.message_handler(regexp="Next")
def next_button(command):
    bot.delete_message(command.chat.id, command.id)

@bot.message_handler(regexp="Play / stop")
def play_stop(command):
    bot.delete_message(command.chat.id, command.id)

@bot.message_handler(regexp="Mute")
def mute(command):
    bot.delete_message(command.chat.id, command.id)

def send_messages():
    print("[BACKGROUND TASK] Starting scheduled messages service")
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        if current_time == "05:25":
            print("[SCHEDULED TASK] Morning message time triggered (05:25)")
            if settings.morning:
                print(f"[SCHEDULED TASK] Sending morning messages to {len(chat_ids)} active users")
                for chat_id in chat_ids:
                    try:
                        bot.send_message(chat_id, "Good morning!")
                        print(f"[SCHEDULED MESSAGE] Sent morning message to {chat_id}")
                        if settings.youtube_music:
                            print("[ACTION] Opening morning YouTube music playlist")
                            wb.open("https://music.youtube.com/watch?v=dzqucn29zM4&list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
                    except Exception as e:
                        print(f"[ERROR] Failed to send morning message to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "20:00":
            print("[SCHEDULED TASK] Evening message time triggered (20:00)")
            print(f"[SCHEDULED TASK] Sending evening messages to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "Легкий ужин")
                    print(f"[SCHEDULED MESSAGE] Sent evening message to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send evening message to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "21:00":
            print("[SCHEDULED TASK] Evening message time triggered (21:00)")
            print(f"[SCHEDULED TASK] Sending evening messages to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "Ночной режим.")
                    bot.send_message(chat_id, "Выключи яркий свет")
                    bot.send_message(chat_id, "Включи желтый оттенок для гаджетов")
                    print(f"[SCHEDULED MESSAGE] Sent evening message to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send evening message to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "21:30":
            print("[SCHEDULED TASK] Evening message time triggered (21:30)")
            print(f"[SCHEDULED TASK] Sending evening messages to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "Пора принять теплый душ/ванна(расслабляет мышцы)")
                    print(f"[SCHEDULED MESSAGE] Sent evening message to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send evening message to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "22:00":
            print("[SCHEDULED TASK] Evening message time triggered (22:00)")
            print(f"[SCHEDULED TASK] Sending evening messages to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "Отложи все гаджеты, лучше послушай музыку.")
                    print(f"[SCHEDULED MESSAGE] Sent evening message to {chat_id}")
                    if settings.music_in_the_morning:
                        wb.open("https://open.spotify.com/track/1Np8jXEGfnWuqAeahhyoaD?si=f40fb754ebe64b2b")
                except Exception as e:
                    print(f"[ERROR] Failed to send evening message to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "23:00":
            print("[SCHEDULED TASK] Evening message time triggered (23:00)")
            print(f"[SCHEDULED TASK] Sending evening messages to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "Отложи все гаджеты, лучше послушай музыку.")
                    print(f"[SCHEDULED MESSAGE] Sent evening message to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send evening message to {chat_id}: {str(e)}")
            time.sleep(60)

        time.sleep(1)

print("[SYSTEM] Starting background thread for scheduled messages")
threading.Thread(target=send_messages, daemon=True).start()

while True:
    try:
        print("[SYSTEM] Starting bot polling...")
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"[ERROR] Bot crashed: {e}")
        print("[SYSTEM] Restarting bot in 5 seconds...")
        time.sleep(5)