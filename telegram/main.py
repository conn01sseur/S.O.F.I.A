# Settings and config import from file config.py

print("[LOG] Importing settings and config...")
from config import *


# Imports 

import telebot
import socket
import random
import threading
import time

# Global

bot = telebot.TeleBot(api)
print("[LOG] Initializing bot with API token...")
bot.remove_webhook()
print(f"[SYSTEM] Added predefined chat_id {chat_id} to notifications list")


# Server function

def check_server_connection():
    pass


def telegram_bot():
    pass


# Starting bot

while True:
    try:
        check_server_connection()
        print("[SYSTEM] Starting bot polling...")
        bot.polling(none_stop = True, interval = 0, timeout = 20)
    except Exception as e:
        print(f"[ERROR] Bot crashed: {e}")
        print("[SYSTEM] Restarting bot in 3 seconds...")
        time.sleep(3)