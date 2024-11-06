# main.py
import subprocess  # Імпорт для запуску зовнішніх процесів
import threading
import os
import webbrowser
import time
from video_server import run_server
from chat_handler import check_chat
from utils import get_last_logged_timestamp, load_commands
from auth import authorize_youtube

# Глобальні змінні
command_queue = []
alert_process = None

def main():
    global alert_process

    # Авторизація та створення YouTube сервісу
    scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]
    youtube = authorize_youtube(scopes)

    # Отримання останньої обробленої мітки часу
    last_processed_timestamp = get_last_logged_timestamp()

    # Отримання liveChatId для стріму
    live_chat_id = youtube.liveBroadcasts().list(
        part="snippet",
        broadcastStatus="active",
        broadcastType="all"
    ).execute().get("items", [{}])[0].get("snippet", {}).get("liveChatId")

    if not live_chat_id:
        print("Не вдалось знайти liveChatId.")
        return

    try:
        while True:
            # Динамічне завантаження команд під час роботи
            commands = load_commands()
            check_chat(youtube, live_chat_id, commands, command_queue, last_processed_timestamp)
            time.sleep(5)
    except KeyboardInterrupt:
        print("Зупинка основного скрипта.")
    finally:
        if alert_process:
            alert_process.terminate()
            alert_process.wait()
            print("Скрипт alert.py завершено.")

if __name__ == "__main__":
    # Запуск сервера у фоновому потоці
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000")
    main()
