import time
import threading
from datetime import datetime
import googleapiclient.discovery
import googleapiclient.errors
import sys
import pickle

# Ініціалізація сервісу YouTube

def initialize_youtube_service(credentials):
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# Отримання liveChatId для стріму

def get_live_chat_id(youtube):
    try:
        request = youtube.liveBroadcasts().list(
            part="snippet",
            broadcastStatus="active",
            broadcastType="all"
        )
        response = request.execute()
        if "items" in response and len(response["items"]) > 0:
            live_chat_id = response["items"][0]["snippet"]["liveChatId"]
            print(f"Отримано liveChatId: {live_chat_id}")
            return live_chat_id
        else:
            print("Активний стрім не знайдено.")
            return None
    except googleapiclient.errors.HttpError as e:
        print("Помилка отримання liveChatId:", e)
        return None

# Функція для відправлення повідомлення в чат

def send_message_to_chat(youtube, live_chat_id, message):
    try:
        request = youtube.liveChatMessages().insert(
            part="snippet",
            body={
                "snippet": {
                    "liveChatId": live_chat_id,
                    "type": "textMessageEvent",
                    "textMessageDetails": {
                        "messageText": message
                    }
                }
            }
        )
        response = request.execute()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Повідомлення відправлено: {message}")
        print("Відповідь API:", response)
    except googleapiclient.errors.HttpError as e:
        print("Помилка відправлення повідомлення:", e)

# Функція для відправлення повідомлень з файлу

def send_alerts(youtube, live_chat_id):
    try:
        with open("alert.txt", "r", encoding="utf-8") as file:
            alerts = file.readlines()

        if not alerts:
            print("Файл alert.txt порожній. Додайте повідомлення для відправки.")
            return

        while True:
            for alert in alerts:
                alert = alert.strip()
                if alert:
                    print(f"Відправка повідомлення: {alert}")
                    send_message_to_chat(youtube, live_chat_id, alert)
                    time.sleep(150)  # Затримка для тестування (15 секунд)
    except FileNotFoundError:
        print("Файл alert.txt не знайдено. Створіть файл і додайте повідомлення.")

# Запускаємо відправку повідомлень у фоновому режимі

def start_alerts_thread(credentials):
    youtube = initialize_youtube_service(credentials)
    live_chat_id = get_live_chat_id(youtube)
    if not live_chat_id:
        print("Не вдалося отримати liveChatId.")
        return

    alert_thread = threading.Thread(target=send_alerts, args=(youtube, live_chat_id))
    alert_thread.daemon = True  # Потік завершиться при завершенні програми
    alert_thread.start()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--load-credentials":
        try:
            with open("credentials.pkl", "rb") as cred_file:
                credentials = pickle.load(cred_file)
            start_alerts_thread(credentials)
            while True:
                time.sleep(1)  # Основний цикл, щоб скрипт не завершувався
        except FileNotFoundError:
            print("Файл credentials.pkl не знайдено. Запустіть авторизацію спочатку.")
    else:
        print("Цей скрипт потрібно запускати з обліковими даними з основного скрипту.")
