import telebot
import threading
import time
from datetime import datetime
import webbrowser as wb
import requests
import socket
import json
import random

print("[LOG] Importing settings and config...")
import settings

# import your token and chat id
import config
print("[LOG] Initializing bot with API token...")
bot = telebot.TeleBot(config.api)
bot.remove_webhook()

chat_ids = {config.chat_id}
print(f"[SYSTEM] Added predefined chat_id {config.chat_id} to notifications list")

def send_server_checker():
    print("Подключние к серверу")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            client_socket.connect((config.host, config.port))
            message = "telegram_bot"
            client_socket.send(message.encode)
            break
        except ConnectionRefusedError:
            print("Не удалось подключится к серверу")

active_timers = {}

print("[LOG] Creating keyboard layout - Page 1")
main_button_1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('📉\nExchange')
button_2 = telebot.types.KeyboardButton('⛅️\nWeather')
button_3 = telebot.types.KeyboardButton('🛠️\nSettings')
button_4 = telebot.types.KeyboardButton('ℹ️\nMy info')
button_page_1 = telebot.types.KeyboardButton('➡️\nPage 2')
button_page_2 = telebot.types.KeyboardButton('⬅️\nPage 4')
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

print("[LOG] Creating timer selection keyboard")
timer_button = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton('1 минута')
button_2 = telebot.types.KeyboardButton('2 минуты')
button_3 = telebot.types.KeyboardButton('3 минуты')
button_4 = telebot.types.KeyboardButton('5 минут')
button_5 = telebot.types.KeyboardButton('10 минут')
button_6 = telebot.types.KeyboardButton('15 минут')
button_7 = telebot.types.KeyboardButton('20 минут')
button_8 = telebot.types.KeyboardButton('25 минут')
button_9 = telebot.types.KeyboardButton('30 минут')
button_10 = telebot.types.KeyboardButton('40 минут')
button_11 = telebot.types.KeyboardButton('1 час')
button_12 = telebot.types.KeyboardButton('2 часа')
button_13 = telebot.types.KeyboardButton('3 часа')
button_14 = telebot.types.KeyboardButton('4 часа')
button_15 = telebot.types.KeyboardButton('5 часов')
button_16 = telebot.types.KeyboardButton('6 часов')
button_17 = telebot.types.KeyboardButton('12 часов')
button_18 = telebot.types.KeyboardButton('24 часа')
button_exit = telebot.types.KeyboardButton('⬅️\nExit')
timer_button.row(button_1, button_2, button_3, button_4, button_5)
timer_button.row(button_6, button_7, button_8, button_9, button_10)
timer_button.row(button_11, button_12, button_13, button_14, button_15)
timer_button.row(button_16, button_17, button_18)
timer_button.row(button_exit)

def update_main_button():
    print("[LOG] Updating settings keyboard based on current configuration")
    setting_button = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    if settings.youtube_music:
        button_1 = telebot.types.KeyboardButton('🟢 YouTube All Time')
        print("[LOG] YouTube music setting is currently ENABLED")
    else:
        button_1 = telebot.types.KeyboardButton('🔴 YouTube All Time')
        print("[LOG] YouTube music setting is currently DISABLED")

    if settings.morning:
        button_2 = telebot.types.KeyboardButton('🟢 Morning Script')
        print("[LOG] Morning notifications setting is currently ENABLED")
    else:
        button_2 = telebot.types.KeyboardButton('🔴 Morning Script')
        print("[LOG] Morning notifications setting is currently DISABLED")

    if settings.music_in_the_evening:
        button_3 = telebot.types.KeyboardButton('🟢 Music in the evening')
        print("[LOG] Music notifications setting is currently ENABLED")
    else:
        button_3 = telebot.types.KeyboardButton('🔴 Music in the evening')
        print("[LOG] Music notifications setting is currently DISABLED")
    
    if settings.rmlt:
        button_4 = telebot.types.KeyboardButton('🟢 Random my lunch time')
        print("[LOG] RMLT notifications setting is currently ENABLED")
    else:
        button_4 = telebot.types.KeyboardButton('🔴 Random my lunch time')
        print("[LOG] RMLT notifications setting is currently DISABLED")

    if settings.yim:
        button_5 = telebot.types.KeyboardButton('🟢 YouTube in morning')
        print("[LOG] YouTube in morning notifications setting is currently ENABLED")
    else:
        button_5 = telebot.types.KeyboardButton('🔴 YouTube in morning')
        print("[LOG] YouTube in morning notifications setting is currently DISABLED")

    if settings.ventilation_reminders:
        button_6 = telebot.types.KeyboardButton('🟢 Ventilation reminder')
        print("[LOG] Ventilation reminders setting is currently ENABLED")
    else:
        button_6 = telebot.types.KeyboardButton('🔴 Ventilation reminder')
        print("[LOG] Ventilation reminders setting is currently DISABLED")

    if settings.omega3_reminders:
        button_7 = telebot.types.KeyboardButton('🟢 Omega-3 reminders')
        print("[LOG] Omega-3 reminders setting is currently ENABLED")
    else:
        button_7 = telebot.types.KeyboardButton('🔴 Omega-3 reminders')
        print("[LOG] Omega-3 reminders setting is currently DISABLED")

    if settings.vitamin_d3_reminders:
        button_8 = telebot.types.KeyboardButton('🟢 Vitamin D3 reminders')
        print("[LOG] Vitamin D3 reminders setting is currently ENABLED")
    else:
        button_8 = telebot.types.KeyboardButton('🔴 Vitamin D3 reminders')
        print("[LOG] Vitamin D3 reminders setting is currently DISABLED")
    
    if settings.time_reminder:
        button_9 = telebot.types.KeyboardButton('🟢 Time_reminder_nada')
        print("[LOG] Time reminders setting is currently ENABLED")
    else:
        button_9 = telebot.types.KeyboardButton('🔴 Time_reminder_nada')
        print("[LOG] Time reminders setting is currently DISABLED")

    button_exit = telebot.types.KeyboardButton('⬅️ Exit')
    
    setting_button.row(button_1, button_2)
    setting_button.row(button_3, button_4)
    setting_button.row(button_5, button_6)
    setting_button.row(button_7, button_8)
    setting_button.row(button_9)
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
        f.write(f'rmlt = {settings.rmlt}\n')
        f.write(f'yim = {settings.yim}\n')
        f.write(f'ventilation_reminders = {settings.ventilation_reminders}\n')
        f.write(f'omega3_reminders = {settings.omega3_reminders}\n')
        f.write(f'vitamin_d3_reminders = {settings.vitamin_d3_reminders}\n')
        f.write(f'time_reminder = {settings.time_reminder}\n')
    print("[LOG] Settings successfully saved to file")

@bot.message_handler(regexp='/start')
def start(command):
    print(f"[USER ACTION] New session started by user {command.chat.id}")
    bot.send_message(command.chat.id, 'Hello, I am S.O.F.I.A', reply_markup=main_button_1)
    chat_ids.add(command.chat.id)
    print(f"[LOG] Added user {command.chat.id} to active sessions list")

@bot.message_handler(regexp='Youtube All Time')
def youtube(command):
    print(f"[USER ACTION] User {command.chat.id} toggled YouTube setting")
    bot.delete_message(command.chat.id, command.id)
    settings.youtube_music = not settings.youtube_music
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, '⚙️ YouTube settings updated', reply_markup=updated_markup)
    print(f"[LOG] YouTube setting changed to: {settings.youtube_music}")

@bot.message_handler(regexp='Morning Script')
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

@bot.message_handler(regexp='Random my lunch time')
def RMLT(command):
    bot.delete_message(command.chat.id, command.id)
    settings.rmlt = not settings.rmlt
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, '⚙️ RMLT in the evening settings updated', reply_markup=updated_markup)
    print(f"[LOG] RMLT in the evening setting changed to: {settings.rmlt}")

@bot.message_handler(regexp='YouTube in morning')
def yim(command):
    bot.delete_message(command.chat.id, command.id)
    settings.yim = not settings.yim
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, '⚙️ yim in the evening settings updated', reply_markup=updated_markup)
    print(f"[LOG] yim in the evening setting changed to: {settings.yim}")

@bot.message_handler(regexp='Omega-3 reminders')
def omega3_reminders(command):
    print(f"[USER ACTION] User {command.chat.id} toggled Omega-3 reminders setting")
    bot.delete_message(command.chat.id, command.id)
    settings.omega3_reminders = not settings.omega3_reminders
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, '⚙️ Omega-3 reminders settings updated', reply_markup=updated_markup)
    print(f"[LOG] Omega-3 reminders setting changed to: {settings.omega3_reminders}")

@bot.message_handler(regexp='Vitamin D3 reminders')
def vitamin_d3_reminders(command):
    print(f"[USER ACTION] User {command.chat.id} toggled Vitamin D3 reminders setting")
    bot.delete_message(command.chat.id, command.id)
    settings.vitamin_d3_reminders = not settings.vitamin_d3_reminders
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, '⚙️ Vitamin D3 reminders settings updated', reply_markup=updated_markup)
    print(f"[LOG] Vitamin D3 reminders setting changed to: {settings.vitamin_d3_reminders}")

@bot.message_handler(regexp='Ventilation reminder')
def ventilation_reminder(command):
    print(f"[USER ACTION] User {command.chat.id} toggled Ventilation reminder setting")
    bot.delete_message(command.chat.id, command.id)
    settings.ventilation_reminders = not settings.ventilation_reminders
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, '⚙️ Ventilation reminders settings updated', reply_markup=updated_markup)
    print(f"[LOG] Ventilation reminders setting changed to: {settings.ventilation_reminders}")

@bot.message_handler(regexp='Time_reminder_nada')
def timereminder(command):
    print(f"[USER ACTION] User {command.chat.id} toggled Time reminder setting")
    bot.delete_message(command.chat.id, command.id)
    settings.time_reminder = not settings.time_reminder
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, '⚙️ Time reminders settings updated', reply_markup=updated_markup)
    print(f"[LOG] Time reminder reminders setting changed to: {settings.time_reminder}")

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
        user_info = (
            f"👤 Ваша информация:\n"
            f"🆔 ID: {command.chat.id}\n"
            f"👤 Имя: {command.chat.first_name}\n"
            f"👥 Фамилия: {command.chat.last_name}\n"
            f"📛 Логин: @{command.chat.username}\n"
            f"📅 Дата регистрации: {datetime.fromtimestamp(command.date).strftime('%Y-%m-%d %H:%M:%S')}"
        )
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
        bot.send_message(command.chat.id, f"💵 Курс валют:\n💲 1 USD = {data['rates']['RUB']} RUB\n💶 1 EUR = {data['rates']['RUB']/data['rates']['EUR']:.2f} RUB")
        print(f"[API RESPONSE] Current exchange rate: 1 USD = {data['rates']['RUB']} RUB")
    except Exception as e:
        print(f"[API ERROR] Exchange rate API request failed: {str(e)}")
        bot.reply_to(command, "❌ Не удалось получить курс валют")

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
            f"🌤 Погода в {city}:\n"
            f"🌡 Температура: {data['main']['temp']}°C (ощущается как {data['main']['feels_like']}°C)\n"
            f"💧 Влажность: {data['main']['humidity']}%\n"
            f"🌬 Ветер: {data['wind']['speed']} м/с\n"
            f"☁️ {data['weather'][0]['description'].capitalize()}\n"
            f"🧭 Давление: {data['main']['pressure']} hPa"
        )
        
        bot.send_message(command.chat.id, weather_info)
        print(f"[API RESPONSE] Successfully retrieved weather data")
    except Exception as e:
        print(f"[API ERROR] Weather API request failed: {str(e)}")
        bot.send_message(command.chat.id, "❌ Не удалось получить данные о погоде")

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
def timer_menu(command):
    print(f"[USER ACTION] User {command.chat.id} opened Timer menu")
    bot.delete_message(command.chat.id, command.id)
    bot.send_message(command.chat.id, "⏳ Выберите время для таймера:", reply_markup=timer_button)

def timer_callback(chat_id, duration, message_id):
    try:
        print(f"[TIMER] Timer completed for user {chat_id} after {duration}")
        bot.send_message(chat_id, f"⏰ Таймер на {duration} завершен! 🔔")
        
        try:
            bot.delete_message(chat_id, message_id)
        except Exception as e:
            print(f"[TIMER WARNING] Could not delete timer selection message: {e}")
        
        bot.send_message(chat_id, "🔄 Возврат в главное меню", reply_markup=main_button_1)
        
        if chat_id in active_timers:
            del active_timers[chat_id]
            
    except Exception as e:
        print(f"[TIMER ERROR] Error in timer callback for user {chat_id}: {e}")

@bot.message_handler(func=lambda message: any(time in message.text for time in [
    '1 минута', '2 минуты', '3 минуты', '5 минут', '10 минут', 
    '15 минут', '20 минут', '25 минут', '30 минут', '40 минут',
    '1 час', '2 часа', '3 часа', '4 часа', '5 часов', '6 часов',
    '12 часов', '24 часа'
]))

def set_timer(command):
    try:
        chat_id = command.chat.id
        duration_text = command.text
        print(f"[USER ACTION] User {chat_id} set timer for {duration_text}")

        bot.delete_message(chat_id, command.id)

        msg = bot.send_message(chat_id, f"⏳ Таймер установлен на {duration_text}\nОтправьте 'Отмена' для отмены")

        if 'минут' in duration_text:
            seconds = int(duration_text.split()[0]) * 60
        elif 'час' in duration_text:
            hours = 1 if duration_text == '1 час' else int(duration_text.split()[0])
            seconds = hours * 3600
        else:
            raise ValueError("Unknown time format")
            
        print(f"[TIMER] Parsed {duration_text} to {seconds} seconds")

        if chat_id in active_timers:
            print(f"[TIMER] Cancelling previous timer for user {chat_id}")
            active_timers[chat_id].cancel()
            
        timer_thread = threading.Timer(seconds, timer_callback, args=[chat_id, duration_text, msg.message_id])
        timer_thread.start()
        
        active_timers[chat_id] = timer_thread
        print(f"[TIMER] New timer started for user {chat_id} ({duration_text})")
        
    except Exception as e:
        print(f"[TIMER ERROR] Failed to set timer: {e}")
        bot.send_message(chat_id, "🛑 Не удалось установить таймер")

@bot.message_handler(regexp="Отмена")
def cancel_timer(command):
    try:
        chat_id = command.chat.id
        print(f"[USER ACTION] User {chat_id} requested timer cancellation")
        
        if chat_id in active_timers:
            active_timers[chat_id].cancel()
            del active_timers[chat_id]
            print(f"[TIMER] Timer cancelled for user {chat_id}")
            bot.send_message(chat_id, "Таймер отменен")
        else:
            print(f"[TIMER WARNING] No active timer found for user {chat_id}")
            bot.send_message(chat_id, "Нет активных таймеров для отмены")
            
        bot.send_message(chat_id, "Page 1", reply_markup=main_button_1)
        
    except Exception as e:
        print(f"[TIMER ERROR] Failed to cancel timer: {e}")
        bot.send_message(chat_id, "🛑 Не удалось отменить таймер")
    

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

# Page 4
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
        
def send_messages():
    print("[BACKGROUND TASK] Starting scheduled messages service")
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        if current_time == "05:30":
            print("[SCHEDULED TASK] Morning message time triggered (05:30)")
            try:
                print("[API REQUEST] Fetching USD to RUB exchange rate")
                response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
                data = response.json()
                exchange_rate = f"💵 Курс валют:\n💲 1 USD = {data['rates']['RUB']} RUB\n💶 1 EUR = {data['rates']['RUB']/data['rates']['EUR']:.2f} RUB"
                print(f"[API RESPONSE] Current exchange rate: 1 USD = {data['rates']['RUB']} RUB")
            except Exception as e:
                print(f"[API ERROR] Exchange rate API request failed: {str(e)}")
                exchange_rate = "❌ Не удалось получить курс валют"

            try:
                city = "Yakutsk"
                print(f"[API REQUEST] Fetching weather data for {city}")
                response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=942343b4877c75d7775a5cda76fd1bc6&units=metric")
                data = response.json()
                
                weather_info = (
                    f"🌤 Погода в {city}:\n"
                    f"🌡 Температура: {data['main']['temp']}°C (ощущается как {data['main']['feels_like']}°C)\n"
                    f"💧 Влажность: {data['main']['humidity']}%\n"
                    f"🌬 Ветер: {data['wind']['speed']} м/с\n"
                    f"☁️ {data['weather'][0]['description'].capitalize()}\n"
                    f"🧭 Давление: {data['main']['pressure']} hPa"
                )
                print(f"[API RESPONSE] Successfully retrieved weather data")
            except Exception as e:
                print(f"[API ERROR] Weather API request failed: {str(e)}")
                weather_info = "❌ Не удалось получить данные о погоде"

            morning_message = (
                "🌄 Доброе утро!\n\n"
                f"{exchange_rate}\n\n"
                f"{weather_info}\n\n"
                "☀️ Хорошего дня!"
            )
            
            if settings.morning:
                print(f"[SCHEDULED TASK] Sending morning messages to {len(chat_ids)} active users")
                for chat_id in chat_ids:
                    try:
                        bot.send_message(chat_id, morning_message)
                        print(f"[SCHEDULED MESSAGE] Sent morning message to {chat_id}")
                        if settings.morning_youtube_music:
                            print("[ACTION] Opening morning YouTube music playlist")
                            wb.open("https://music.youtube.com/watch?v=dzqucn29zM4&list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
                    except Exception as e:
                        print(f"[ERROR] Failed to send morning message to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "05:45" and (settings.omega3_reminders or settings.vitamin_d3_reminders):
            print("[SCHEDULED TASK] Morning supplements reminder (08:00)")
            for chat_id in chat_ids:
                try:
                    message = "💊 Утренний прием добавок:\n\n"
                    if settings.omega3_reminders:
                        message += "🔹 Омега-3: 2 капсулы\n"
                    if settings.vitamin_d3_reminders:
                        message += "🔹 Витамин D3: 1 таблетка\n"
                    message += "\nЗапейте водой во время завтрака"
                    
                    bot.send_message(chat_id, message)
                    print(f"[SCHEDULED MESSAGE] Sent morning supplements reminder to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send supplements reminder to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "06:00" and settings.time_reminder:
            print("[SCHEDULED TASK] Time reminder (06:00)")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "Время уже 6:00")
                    print(f"[SCHEDULED MESSAGE] Sent time reminder to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send time reminder to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "06:15":
            print("[SCHEDULED TASK] Bus reminder time triggered (06:15)")
            print(f"[SCHEDULED TASK] Sending bus reminders to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "🚌 Через 5 минут выходить на автобус")
                    print(f"[SCHEDULED MESSAGE] Sent bus reminder to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send bus reminder to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "15:30" and settings.omega3_reminders:
            print("[SCHEDULED TASK] Afternoon Omega-3 reminder (12:00)")
            for chat_id in chat_ids:
                try:
                    bot.send_message(
                        chat_id,
                        "💊 Дневной прием Омега-3:\n\n"
                        "🔹 Омега-3: 2 капсулы\n\n"
                        "Примите во время обеда"
                    )
                    print(f"[SCHEDULED MESSAGE] Sent afternoon Omega-3 reminder to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send Omega-3 reminder to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "18:00" and settings.ventilation_reminders:
            print("[SCHEDULED TASK] Ventilation reminder time triggered (18:00)")
            print(f"[SCHEDULED TASK] Sending ventilation reminders to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(
                        chat_id,
                        "💨 Вечернее проветривание\n\n"
                        "🔹 10 минут интенсивного проветривания перед сном\n"
                        "🔹 Особенно важно в спальне\n"
                        "🔹 Свежий воздух улучшает качество сна"
                    )
                    print(f"[SCHEDULED MESSAGE] Sent ventilation reminder to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send ventilation reminder to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "12:30":
            print("[SCHEDULED TASK] Lunch time reminder (12:30)")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "🍽 Что будем есть?\n🎲 Рандомный выбор...")
                    print(f"[SCHEDULED MESSAGE] Sent lunch reminder to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send lunch reminder to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "15:25":
            print("[SCHEDULED TASK] Lunch time reminder (15:25)")
            print(f"[SCHEDULED TASK] Sending lunch reminders to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "🍽 Скоро обеденное время")
                    print(f"[SCHEDULED MESSAGE] Sent lunch reminder to {chat_id}")
                    
                    if settings.rmlt:
                        print("[SCHEDULED TASK] Random meal selection enabled")
                        bot.send_message(chat_id, "🍴 Что будем кушать?")
                        bot.send_message(chat_id, "🎰 Крутим барабан...")
                        time.sleep(5)
                        eda = ['🥟 Пельмени', '🍳 Яйца', '🍲 Борщ', '🍜 Харчо', '🥣 Куриный суп']
                        selected_meal = random.choice(eda)
                        bot.send_message(chat_id, selected_meal)
                        print(f"[SCHEDULED MESSAGE] Sent random meal selection: {selected_meal} to {chat_id}")
                    else:
                        print(f"[SCHEDULED MESSAGE] Random meal selection disabled for {chat_id}")
                        
                except Exception as e:
                    print(f"[ERROR] Failed to process lunch reminder for {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "15:30":
            print("[SCHEDULED TASK] Lunch time reminder (15:30)")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "🍽 Обеденное время")
                except Exception as e:
                    print(f"[ERROR] Failed to send lunch reminder to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "20:00":
            print("[SCHEDULED TASK] Evening message time triggered (20:00)")
            print(f"[SCHEDULED TASK] Sending evening messages to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "🍽 Время легкого ужина и 📝 написания отчета\n🥟 Пельмени или что-то другое?")
                    print(f"[SCHEDULED MESSAGE] Sent evening message to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send evening message to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "21:55":
            print("[SCHEDULED TASK] Night mode reminder (21:55)")
            print(f"[SCHEDULED TASK] Sending night mode reminders to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "🌙 Через 5 минут включится ночной режим")
                    print(f"[SCHEDULED MESSAGE] Sent night mode reminder to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send night mode reminder to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "22:00":
            print("[SCHEDULED TASK] Night mode time triggered (22:00)")
            print(f"[SCHEDULED TASK] Sending night mode messages to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "🌙 Ночной режим активирован\n💡 Пожалуйста, выключи яркий свет")
                    print(f"[SCHEDULED MESSAGE] Sent night mode message to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send night mode message to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "22:25":
            print("[SCHEDULED TASK] Shower reminder (22:25)")
            print(f"[SCHEDULED TASK] Sending shower reminders to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "🚿 Через 5 минут время душа")
                    print(f"[SCHEDULED MESSAGE] Sent shower reminder to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send shower reminder to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "22:30":
            print("[SCHEDULED TASK] Shower time triggered (22:30)")
            print(f"[SCHEDULED TASK] Sending shower messages to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "🚿 Пора принять теплый душ или ванну")
                    print(f"[SCHEDULED MESSAGE] Sent shower message to {chat_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send shower message to {chat_id}: {str(e)}")
            time.sleep(60)

        elif current_time == "23:00":
            print("[SCHEDULED TASK] Good night message time triggered (23:00)")
            print(f"[SCHEDULED TASK] Sending good night messages to {len(chat_ids)} active users")
            for chat_id in chat_ids:
                try:
                    bot.send_message(chat_id, "😴 Пора спать! Хороших снов 🌙\n🌃 Приятных сновидений!")
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
        send_server_checker()
        print("[SYSTEM] Starting bot polling...")
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"[ERROR] Bot crashed: {e}")
        print("[SYSTEM] Restarting bot in 3 seconds...")
        time.sleep(3)