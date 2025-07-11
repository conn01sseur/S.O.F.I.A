try:
    from config import *
    print("[+] Config.py file loaded successfully")
except ImportError:
    print("[-] Config file not found or not installed")

try:
    import socket
    print("[+] Socket library is installed")
except ImportError:
    print("[-] Socket not installed (this is unusual, it's a built-in library)")

try:
    import sys
    print("[+] Sys library is installed")
except ImportError:
    print("[-] Sys not installed (this is very unusual, it's a core Python library)")

try:
    import os
    print("[+] Os library is installed")
except ImportError:
    print("[-] Os not installed (this is very unusual, it's a core Python library)")

try:
    import telebot
    print("[+] Telebot library is installed")
except ImportError:
    print("[-] Telebot not installed")

bunner = f'''
⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦
⣿⣿⣿⣿⣿⣿⣿⣿⣯⡉⠙⠻⢿⣿⣿⣿⣿⣿⢿⣦
⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⡆⠀⠀⢻⣿⣿⣿⣿⡆⠈⢳⡄
⣿⣿⣿⣿⣿⠈⢿⣿⣿⣿⣷⠖⠀⠀⣿⣿⣿⣿⣿⣄⠀⣿⡄
⣿⣿⣿⣿⣿⣇⠀⢄⡙⠋⠻⡄⠀⣼⣿⣿⣿⣩⠟⠟⠀⣼⣿⡄
⣿⣿⣿⣿⣿⣿⣷⣦⣭⣤⣤⣴⣿⣿⣿⣿⣿⣿⣿⣦⣴⣿⣿⣷⠀
⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⢿⣿⣿⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⢰⣶⣄
⣉⣛⣛⣛⣥⣶⣾⣿⣿⣿⣷⡝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⠟⠀
⢻⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠈⠁
⠀⠹⣿⣿⡿⠿⠛⣋⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿

    version: {version_sofia}'''

print(bunner)