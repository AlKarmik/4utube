# utils.py
import os

def get_last_logged_timestamp(log_file="queue_log.txt"):
    """
    Повертає останню мітку часу з журналу, якщо вона існує.
    """
    if not os.path.exists(log_file):
        return None
    with open(log_file, "r") as log:
        last_line = log.readlines()[-1]
        timestamp = last_line.split(", ")[0]
        return timestamp

def is_command_logged(timestamp, log_file="queue_log.txt"):
    """
    Перевіряє, чи була команда з певною міткою часу вже виконана.
    """
    if not os.path.exists(log_file):
        return False
    with open(log_file, "r") as log:
        for line in log:
            if line.startswith(timestamp):
                return True
    return False

def load_commands(filename="command.txt"):
    """
    Завантажує команди з текстового файлу у форматі ключ=значення.
    """
    commands = {}
    with open(filename, "r") as file:
        for line in file:
            if "=" in line:
                cmd, path = line.strip().split("=", 1)
                commands[cmd.strip()] = path.strip()
    return commands

# Використання цих функцій дозволяє іншим модулям отримувати доступ до міток часу, перевіряти виконання команд та завантажувати команди з файлу.
