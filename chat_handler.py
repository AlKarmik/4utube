# chat_handler.py
import time

def check_chat(youtube, live_chat_id, commands, command_queue, last_processed_timestamp):
    """
    Перевіряє чат і додає нові команди у чергу.
    """
    request = youtube.liveChatMessages().list(
        liveChatId=live_chat_id,
        part="snippet,authorDetails"
    )
    response = request.execute()

    for item in response["items"]:
        message = item["snippet"]["displayMessage"].strip()
        timestamp = item["snippet"]["publishedAt"]
        username = item["authorDetails"].get("displayName", "Unknown")

        # Пропуск вже оброблених команд
        if last_processed_timestamp and timestamp <= last_processed_timestamp:
            continue

        # Перевірка повного співпадіння команди
        for cmd, video_path in commands.items():
            if message == cmd:
                if any(cmd == existing_cmd['command'] and timestamp == existing_cmd['timestamp'] for existing_cmd in command_queue):
                    continue  # Уникнення дублювання команд
                
                command_queue.append({
                    'command': cmd,
                    'video_path': video_path,
                    'timestamp': timestamp,
                    'username': username
                })
                print(f"Команда '{cmd}' виявлена! Додано в чергу з шляхом: {video_path}, міткою часу: {timestamp}, від {username}")

    # Оновлення останньої обробленої мітки часу
    if response["items"]:
        last_processed_timestamp = response["items"][-1]["snippet"]["publishedAt"]

    return last_processed_timestamp
