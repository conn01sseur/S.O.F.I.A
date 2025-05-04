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
bot = telebot.TeleBot('7945094960:AAHl3Gmz0XBeyRNpzBZLxGDT7H8-4oGuVn4')
bot.remove_webhook()

chat_ids = set()

host = "localhost"
port = 7780

connected_clients = []
socket_lock = threading.Lock()

def socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"[SOCKET] Server is listening on {host}:{port}")
    
    while True:
        try:
            conn, addr = server.accept()
            print(f"[SOCKET] Connection established from {addr}")
            
            with socket_lock:
                connected_clients.append(conn)

            client_thread = threading.Thread(
                target=handle_client_connection,
                args=(conn, addr),
                daemon=True
            )
            client_thread.start()
            
        except Exception as e:
            print(f"[SOCKET ERROR] Server accept error: {e}")
            break

def handle_client_connection(conn, addr):
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
                
            print(f"[SOCKET] Received from {addr}: {data}")
            
            try:
                message_data = json.loads(data)
                chat_id = message_data.get('chat_id')
                text = message_data.get('text')
                
                if chat_id and text:
                    bot.send_message(chat_id, f"🔌 From {addr[0]}: {text}")
                    print(f"[SOCKET] Forwarded message to chat {chat_id}")
                    
                conn.send("Message received by server".encode('utf-8'))
                
            except json.JSONDecodeError:
                print("[SOCKET] Received invalid JSON data")
                conn.send("Invalid JSON format".encode('utf-8'))
                
    except Exception as e:
        print(f"[SOCKET ERROR] Client {addr} connection error: {e}")
    finally:
        with socket_lock:
            if conn in connected_clients:
                connected_clients.remove(conn)
        conn.close()
        print(f"[SOCKET] Connection closed with {addr}")

def send_to_all_clients(message):
    with socket_lock:
        if not connected_clients:
            return False, "No devices connected"
            
        success = 0
        failed = 0
        responses = []
        
        for client in connected_clients.copy():
            try:
                client.sendall(message.encode('utf-8'))
                print(f"[SOCKET] Sent message to {client.getpeername()}")
                success += 1

                response = client.recv(1024).decode('utf-8')
                responses.append(response)
                
            except Exception as e:
                print(f"[SOCKET ERROR] Failed to send to client: {e}")
                failed += 1
                # Remove disconnected client
                connected_clients.remove(client)
                
        return True, f"Sent to {success} device(s), failed: {failed}. Responses: {responses}"

# Start socket server thread
socket_thread = threading.Thread(target=socket_server, daemon=True)
socket_thread.start()

print("[LOG] Creating keyboard layout - Page 1")
main_button_1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('📉\nExchange')
button_2 = telebot.types.KeyboardButton('⛅️\nWeather')
button_3 = telebot.types.KeyboardButton('🛠️\nSettings')
button_4 = telebot.types.KeyboardButton('ℹ️\nMy info')
button_page_1 = telebot.types.KeyboardButton('➡️\nPage 2')
button_page_2 = telebot.types.KeyboardButton('⬅️\nPage 3')
main_button_1.row(button_4, button_1, button_2, button_3)
main_button_1.row(button_page_2, button_page_1)

print("[LOG] Creating keyboard layout - Page 2")
main_button_2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('🎹\nMusic')
button_2 = telebot.types.KeyboardButton('👾\nGame')
button_3 = telebot.types.KeyboardButton('🕹️\nControl')
button_page_1 = telebot.types.KeyboardButton('➡️\nPage 3')
button_page_2 = telebot.types.KeyboardButton('⬅️\nPage 1')
main_button_2.row(button_1, button_2, button_3)
main_button_2.row(button_page_2, button_page_1)

print("[LOG] Creating keyboard layout - Page 3")
main_button_3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('⏳\nTimer')
button_2 = telebot.types.KeyboardButton('🧠\nReminder')
button_3 = telebot.types.KeyboardButton('📆\nSchedule')
button_4 = telebot.types.KeyboardButton('📝\nNotes')
button_page_1 = telebot.types.KeyboardButton('➡️\nPage 4')
button_page_2 = telebot.types.KeyboardButton('⬅️\nPage 2')
main_button_3.row(button_1, button_2, button_3, button_4)
main_button_3.row(button_page_2, button_page_1)

print("[LOG] Creating keyboard layout - Page 4")
main_button_4 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('🏠\nHome')
button_2 = telebot.types.KeyboardButton('🚫\nNo message')
button_3 = telebot.types.KeyboardButton('💤\nSleep')
button_4 = telebot.types.KeyboardButton('🧠 \nmmmm')
button_5 = telebot.types.KeyboardButton('💼\nWork')
button_6 = telebot.types.KeyboardButton('☀️\nMorning')
button_7 = telebot.types.KeyboardButton('🌑\nNight')
button_page_1 = telebot.types.KeyboardButton('➡️\nPage 1')
button_page_2 = telebot.types.KeyboardButton('⬅️\nPage 3')
main_button_4.row(button_1, button_2, button_3)
main_button_4.row(button_4, button_5)
main_button_4.row(button_6, button_7)
main_button_4.row(button_page_2, button_page_1)

print("[LOG] Creating music selection keyboard")
music_button = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_phonk_1 = telebot.types.KeyboardButton('🛞\nPhonk')
button_phonk_2 = telebot.types.KeyboardButton('🌚\nАtmospheric phonk')
button_phonk_3 = telebot.types.KeyboardButton('🇧🇷\nBrazzilian phonk')
button_classic_1 = telebot.types.KeyboardButton('🎹\nPiano')
button_classic_2 = telebot.types.KeyboardButton('🎻\nClassic')
button_classic_3 = telebot.types.KeyboardButton('😕\nMelancholy')
button_author_1 = telebot.types.KeyboardButton('🙂\nMac_demarco')
button_author_2 = telebot.types.KeyboardButton('xz')
button_rock_1 = telebot.types.KeyboardButton('🎸\nMute Rock')
button_rock_2 = telebot.types.KeyboardButton('🤘\nRock')
button_rock_3 = telebot.types.KeyboardButton('🫥\nDead Rock')
button_random = telebot.types.KeyboardButton('🎲\nRandom')
button_exit = telebot.types.KeyboardButton('⬅️\nExit')
music_button.row(button_phonk_1, button_phonk_2, button_phonk_3)
music_button.row(button_classic_1, button_classic_2, button_classic_3)
music_button.row(button_author_1, button_author_2)
music_button.row(button_rock_1, button_rock_2, button_rock_3)
music_button.row(button_random)
music_button.row(button_exit)

print("[LOG] Creating game control selection keyboard")
game_control = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('🎯\nSelect game')
button_2 = telebot.types.KeyboardButton('🌀\nOptimization')
button_3 = telebot.types.KeyboardButton('🛸\nLauncher')
button_exit = telebot.types.KeyboardButton('⬅️\nExit')
game_control.row(button_1, button_2, button_3)
game_control.row(button_exit)

print("[LOG] Creating control selection keyboard")
control_button = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('⏮️\nPrevious')
button_2 = telebot.types.KeyboardButton('⏯️\nPlay / Stop')
button_3 = telebot.types.KeyboardButton('⏭️\nNext')
button_4 = telebot.types.KeyboardButton('🔉\n- Volume')
button_5 = telebot.types.KeyboardButton('🔊\n+ Volume')
button_6 = telebot.types.KeyboardButton('🔇\nMute')
button_exit = telebot.types.KeyboardButton('⬅️\nExit')
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
    chat_ids.add(command.chat.id)
    print(f"[USER ACTION] User {command.chat.id} navigated to Page 1")
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "Page 1", reply_markup=main_button_1)

@bot.message_handler(regexp='Page 2')
def page(command):
    chat_ids.add(command.chat.id)
    print(f"[USER ACTION] User {command.chat.id} navigated to Page 2")
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "Page 2", reply_markup=main_button_2)

@bot.message_handler(regexp='Page 3')
def page(command):
    chat_ids.add(command.chat.id)
    print(f"[USER ACTION] User {command.chat.id} navigated to Page 3")
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "Page 3", reply_markup=main_button_3)

@bot.message_handler(regexp='Page 4')
def page(command):
    chat_ids.add(command.chat.id)
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
        f.write(f'music_in_the_evening = {settings.music_in_the_evening}\n')
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
        wb.open("https://music.youtube.com/playlist?list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
    except Exception as e:
        print(f"[ERROR] Failed to open music playlist: {str(e)}")

# Page 1
@bot.message_handler(regexp="My info")
def info(command):
    try:
        bot.delete_message(command.chat.id, command.id)
        user_info = f"👤 Your Info:\n" \
                   f"ID: {command.chat.id}\n" \
                   f"First Name: {command.chat.first_name}\n" \
                   f"Last Name: {command.chat.last_name}\n" \
                   f"Username: @{command.chat.username}"
        bot.send_message(command.chat.id, user_info)
    except Exception as e:
        print(f"[ERROR] Failed to get user info: {str(e)}")

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
        
        weather_info = (
            f"⛅️ Weather in {city}:\n"
            f"🌡 Temperature: {data['main']['temp']}°C\n"
            f"💧 Humidity: {data['main']['humidity']}%\n"
            f"🌬 Wind: {data['wind']['speed']} m/s\n"
            f"☁️ Conditions: {data['weather'][0]['description']}"
        )
        
        bot.send_message(command.chat.id, weather_info)
        print(f"[API RESPONSE] Successfully retrieved weather data")
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

# Music
@bot.message_handler(regexp='Phonk')
def music_phonk(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        print(f"[USER ACTION] User {command.chat.id} selected Phonk music")
        wb.open("https://music.youtube.com/playlist?list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
        bot.send_message(command.chat.id, "🎵 Playing Phonk music")
    except Exception as e:
        print(f"[ERROR] Failed to open Phonk playlist: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to open Phonk playlist")

@bot.message_handler(regexp='Аtmospheric phonk')
def music_atmospheric_phonk(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        print(f"[USER ACTION] User {command.chat.id} selected Atmospheric Phonk")
        wb.open("https://music.youtube.com/playlist?list=PLJN6x0_6gGDSVjQwB1bVqZ4k3ZJwYQ9jK")
        bot.send_message(command.chat.id, "🌚 Playing Atmospheric Phonk")
    except Exception as e:
        print(f"[ERROR] Failed to open Atmospheric Phonk playlist: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to open Atmospheric Phonk playlist")

@bot.message_handler(regexp='Brazzilian phonk')
def music_brazilian_phonk(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        print(f"[USER ACTION] User {command.chat.id} selected Brazilian Phonk")
        wb.open("https://music.youtube.com/playlist?list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
        bot.send_message(command.chat.id, "🇧🇷 Playing Brazilian Phonk")
    except Exception as e:
        print(f"[ERROR] Failed to open Brazilian Phonk playlist: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to open Brazilian Phonk playlist")

@bot.message_handler(regexp='Piano')
def music_piano(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        print(f"[USER ACTION] User {command.chat.id} selected Piano music")
        wb.open("https://music.youtube.com/playlist?list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
        bot.send_message(command.chat.id, "🎹 Playing Piano music")
    except Exception as e:
        print(f"[ERROR] Failed to open Piano playlist: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to open Piano playlist")

@bot.message_handler(regexp='Classic')
def music_classic(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        print(f"[USER ACTION] User {command.chat.id} selected Classic music")
        wb.open("https://music.youtube.com/playlist?list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
        bot.send_message(command.chat.id, "🎻 Playing Classical music")
    except Exception as e:
        print(f"[ERROR] Failed to open Classic playlist: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to open Classic playlist")

@bot.message_handler(regexp='Melancholy')
def music_melancholy(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        print(f"[USER ACTION] User {command.chat.id} selected Melancholy music")
        wb.open("https://music.youtube.com/playlist?list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
        bot.send_message(command.chat.id, "😕 Playing Melancholy music")
    except Exception as e:
        print(f"[ERROR] Failed to open Melancholy playlist: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to open Melancholy playlist")

@bot.message_handler(regexp='Mac_demarco')
def music_mac_demarco(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        print(f"[USER ACTION] User {command.chat.id} selected Mac DeMarco")
        wb.open("https://music.youtube.com/playlist?list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
        bot.send_message(command.chat.id, "🙂 Playing Mac DeMarco")
    except Exception as e:
        print(f"[ERROR] Failed to open Mac DeMarco playlist: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to open Mac DeMarco playlist")

@bot.message_handler(regexp='xz')
def music_xz(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        print(f"[USER ACTION] User {command.chat.id} selected xz music")
        wb.open("https://music.youtube.com/playlist?list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
        bot.send_message(command.chat.id, "🎵 Playing xz selection")
    except Exception as e:
        print(f"[ERROR] Failed to open xz playlist: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to open xz playlist")

@bot.message_handler(regexp='Mute Rock')
def music_mute_rock(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        print(f"[USER ACTION] User {command.chat.id} selected Mute Rock")
        wb.open("https://music.youtube.com/playlist?list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
        bot.send_message(command.chat.id, "🎸 Playing Mute Rock")
    except Exception as e:
        print(f"[ERROR] Failed to open Mute Rock playlist: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to open Mute Rock playlist")

@bot.message_handler(regexp='Rock')
def music_rock(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        print(f"[USER ACTION] User {command.chat.id} selected Rock")
        wb.open("https://music.youtube.com/playlist?list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
        bot.send_message(command.chat.id, "🤘 Playing Rock music")
    except Exception as e:
        print(f"[ERROR] Failed to open Rock playlist: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to open Rock playlist")

@bot.message_handler(regexp='Dead Rock')
def music_dead_rock(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        print(f"[USER ACTION] User {command.chat.id} selected Dead Rock")
        wb.open("https://music.youtube.com/playlist?list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
        bot.send_message(command.chat.id, "🫥 Playing Dead Rock")
    except Exception as e:
        print(f"[ERROR] Failed to open Dead Rock playlist: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to open Dead Rock playlist")

@bot.message_handler(regexp='Random')
def music_random(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        print(f"[USER ACTION] User {command.chat.id} selected Random music")
        # You can implement random selection logic here
        wb.open("https://music.youtube.com/playlist?list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
        bot.send_message(command.chat.id, "🎲 Playing Random selection")
    except Exception as e:
        print(f"[ERROR] Failed to open Random playlist: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to open Random playlist")

@bot.message_handler(regexp="Game")
def game(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "🎮 Game control panel", reply_markup=game_control)

@bot.message_handler(regexp='Control')
def control(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "Control panel", reply_markup=control_button)

# Page 3
@bot.message_handler(regexp="Timer")
def timer(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "⏳ Timer functionality will be implemented soon")

@bot.message_handler(regexp="Reminder")
def reminder(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "🧠 Reminder functionality will be implemented soon")

@bot.message_handler(regexp="Schedule")
def schedule(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "📆 Schedule functionality will be implemented soon")

@bot.message_handler(regexp="Notes")
def notes(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "📝 Notes functionality will be implemented soon")

# Page 4 commands
@bot.message_handler(regexp="Home")
def home(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        print(f"[USER ACTION] User {command.chat.id} sent Home command")
        result, message = send_to_all_clients("home")
        if result:
            bot.send_message(command.chat.id, f"🏠 Home command sent successfully\n{message}")
        else:
            bot.send_message(command.chat.id, f"⚠️ {message}")
    except Exception as e:
        print(f"[ERROR] Failed to send home command: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to send command to devices")

@bot.message_handler(regexp="Night")
def night(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        result, message = send_to_all_clients("night")
        if result:
            bot.send_message(command.chat.id, f"🌑 Night command sent successfully\n{message}")
        else:
            bot.send_message(command.chat.id, f"⚠️ {message}")
    except Exception as e:
        print(f"[ERROR] Night command failed: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to send night command")

@bot.message_handler(regexp="Sleep")
def sleep(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        result, message = send_to_all_clients("sleep")
        if result:
            bot.send_message(command.chat.id, f"💤 Sleep command sent successfully\n{message}")
        else:
            bot.send_message(command.chat.id, f"⚠️ {message}")
    except Exception as e:
        print(f"[ERROR] Sleep command failed: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to send sleep command")

@bot.message_handler(regexp="Hmmmm")
def hmmmm(command):
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "🤔 Hmmmm... Interesting thought!")

@bot.message_handler(regexp="Work")
def work(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        result, message = send_to_all_clients("work")
        if result:
            bot.send_message(command.chat.id, f"💼 Work command sent successfully\n{message}")
        else:
            bot.send_message(command.chat.id, f"⚠️ {message}")
    except Exception as e:
        print(f"[ERROR] Work command failed: {str(e)}")
        bot.send_message(command.chat.id, "🛑 Failed to send work command")

# Control button
@bot.message_handler(regexp="Previous")
def previous(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        result, message = send_to_all_clients("media_previous")
        if result:
            bot.send_message(command.chat.id, f"⏮️ Previous track command sent\n{message}")
    except Exception as e:
        print(f"[ERROR] Previous command failed: {str(e)}")

@bot.message_handler(regexp="Next")
def next_button(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        result, message = send_to_all_clients("media_next")
        if result:
            bot.send_message(command.chat.id, f"⏭️ Next track command sent\n{message}")
    except Exception as e:
        print(f"[ERROR] Next command failed: {str(e)}")

@bot.message_handler(regexp="Play / stop")
def play_stop(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        result, message = send_to_all_clients("media_play_pause")
        if result:
            bot.send_message(command.chat.id, f"⏯️ Play/Pause command sent\n{message}")
    except Exception as e:
        print(f"[ERROR] Play/Stop command failed: {str(e)}")

@bot.message_handler(regexp="Mute")
def mute(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        result, message = send_to_all_clients("volume_mute")
        if result:
            bot.send_message(command.chat.id, f"🔇 Mute command sent\n{message}")
    except Exception as e:
        print(f"[ERROR] Mute command failed: {str(e)}")

@bot.message_handler(regexp="\+ Volume")
def volume_up(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        result, message = send_to_all_clients("volume_up")
        if result:
            bot.send_message(command.chat.id, f"🔊 Volume increased\n{message}")
    except Exception as e:
        print(f"[ERROR] Volume up command failed: {str(e)}")

@bot.message_handler(regexp="\- Volume")
def volume_down(command):
    bot.delete_message(command.chat.id, command.id)
    try:
        result, message = send_to_all_clients("volume_down")
        if result:
            bot.send_message(command.chat.id, f"🔉 Volume decreased\n{message}")
    except Exception as e:
        print(f"[ERROR] Volume down command failed: {str(e)}")

def send_messages():
    print("[BACKGROUND TASK] Starting scheduled messages service")
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        if current_time == "05:30":
            print("[SCHEDULED TASK] Morning message time triggered (05:30)")
            if settings.morning:
                print(f"[SCHEDULED TASK] Sending morning messages to {len(chat_ids)} active users")
                for chat_id in chat_ids:
                    try:
                        bot.send_message(chat_id, "Доброе утро!")
                        print(f"[SCHEDULED MESSAGE] Sent morning message to {chat_id}")
                        if settings.youtube_music:
                            print("[ACTION] Opening morning YouTube music playlist")
                            wb.open("https://music.youtube.com/watch?v=dzqucn29zM4&list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
                    except Exception as e:
                        print(f"[ERROR] Failed to send morning message to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "06:20":
            print("[SCHEDULED TASK] Bus reminder time triggered (06:20)")
            print(f"[SCHEDULED TASK] Sending bus reminders to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "Пора на автобус. 🚌 🏃‍♂️")
                    bot.send_message(chat_id, "Удачной поездки!")
                    print(f"[SCHEDULED MESSAGE] Sent bus reminder to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send bus reminder to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "13:00":
            print("[SCHEDULED TASK] Lunch time reminder (13:00)")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "🍽 Обед")
                    print(f"[SCHEDULED MESSAGE] Sent lunch reminder to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send lunch reminder to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "20:00":
            print("[SCHEDULED TASK] Evening message time triggered (20:00)")
            print(f"[SCHEDULED TASK] Sending evening messages to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "Пора поесть легкий ужин и ПИСАТЬ ОТЧЕТ")
                    bot.send_message(chat_id, "Пельмени или что-то иное?")
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
                    print(f"[SCHEDULED MESSAGE] Sent evening message to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send evening message to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "21:30":
            print("[SCHEDULED TASK] Evening message time triggered (21:30)")
            print(f"[SCHEDULED TASK] Sending evening messages to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "Пора принять теплый душ/ванна")
                    print(f"[SCHEDULED MESSAGE] Sent evening message to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send evening message to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "22:21":
            print("[SCHEDULED TASK] Evening message time triggered (22:21)")
            print(f"[SCHEDULED TASK] Sending evening messages to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "Отложи все гаджеты, лучше послушай музыку.")
                    print(f"[SCHEDULED MESSAGE] Sent evening message to {chat_id}")
                    if settings.music_in_the_evening:
                        print("[ACTION] Opening evening YouTube music playlist")
                        wb.open("https://www.youtube.com/watch?v=E0FQOxhAQRo")
                except Exception as e:
                    print(f"[ERROR] Failed to send evening message to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "23:00":
            print("[SCHEDULED TASK] Evening message time triggered (23:00)")
            print(f"[SCHEDULED TASK] Sending evening messages to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "Пора спать! Хороших снов 😴")
                    print(f"[SCHEDULED MESSAGE] Sent good night message to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send good night message to {chat_id}: {str(e)}")
            time.sleep(60)

        time.sleep(1)

print("[SYSTEM] Starting background thread for scheduled messages")
threading.Thread(target=send_messages, daemon=True).start()

print("[SYSTEM] Starting bot...")
while True:
    try:
        print("[SYSTEM] Starting bot polling...")
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"[ERROR] Bot crashed: {e}")
        print("[SYSTEM] Restarting bot in 5 seconds...")
        time.sleep(5)