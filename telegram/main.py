import telebot
import threading
import time
from datetime import datetime
import webbrowser as wb
import importlib

# Импорт настроек
print("[LOG] Импорт ваши настроек...", end="")
import settings
print(" Done!")

print("[LOG] Подключение токена...", end="")
bot = telebot.TeleBot('7285599484:AAECj2fMmK_B60tUxLDF_wcfFVCs1vfO-vc')
print(" Done!")

chat_ids = set()

def update_main_button():
    Main_Button_1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if settings.youtube_music:
        button_1 = telebot.types.KeyboardButton('🟢 YouTube')
    else:
        button_1 = telebot.types.KeyboardButton('🔴 YouTube')

    if settings.morning:
        button_2 = telebot.types.KeyboardButton('🟢 Morning')
    else:
        button_2 = telebot.types.KeyboardButton('🔴 Morning')
    
    Main_Button_1.row(button_1, button_2)
    return Main_Button_1

Main_Button_1 = update_main_button()

def save_settings():
    with open('settings.py', 'w') as f:
        f.write(f'youtube_music = {settings.youtube_music}\n')
        f.write(f'morning = {settings.morning}\n')

@bot.message_handler(regexp='/start')
def start(command):
    bot.delete_message(command.chat.id, command.id)
    # bot.send_message(command.chat.id, 'Привет, я С.О.Ф.И.Я', reply_markup=Main_Button_1)
    chat_ids.add(command.chat.id)

@bot.message_handler(regexp='Youtube')
def youtube(command):
    bot.delete_message(command.chat.id, command.id)
    settings.youtube_music = not settings.youtube_music
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, 'Настройки YouTube обновлены', reply_markup=updated_markup)
    chat_ids.add(command.chat.id)

@bot.message_handler(regexp='Morning')
def morning(command):
    bot.delete_message(command.chat.id, command.id)
    settings.morning = not settings.morning
    save_settings()
    updated_markup = update_main_button()
    bot.send_message(command.chat.id, 'Настройки Morning обновлены', reply_markup=updated_markup)
    chat_ids.add(command.chat.id)

def send_messages():
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        if current_time == "05:25":
            print("[LOG] time == 05:25")
            if settings.morning == True:
                for chat_id in chat_ids:
                    bot.send_message(chat_id, "Доброе утро!")
                    if settings.youtube_music == True:
                        wb.open("https://music.youtube.com/watch?v=dzqucn29zM4&list=PLJN6x0_6gGDQifOqtq1oIkj8U8XRCue6h")
                    else:
                        pass

            time.sleep(60)

        elif current_time == "19:54":
            for chat_id in chat_ids:
                bot.send_message(chat_id, "Добрый день!")
            time.sleep(60)

        time.sleep(1)

threading.Thread(target=send_messages, daemon=True).start()

bot.polling()