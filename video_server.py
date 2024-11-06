# Розширений video_server.py
from flask import Flask, jsonify, send_from_directory, render_template, request
import os
import logging

app = Flask(__name__)

# Зменшення рівня логування в Flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

is_video_playing = False  # Змінна для відстеження стану відтворення відео
command_queue = []

@app.route('/')
def home():
    return render_template('index.html')  # Основна панель управління

@app.route('/commands')
def commands_page():
    return render_template('commands.html')  # Сторінка управління командами

@app.route('/alerts')
def alerts_page():
    return render_template('alerts.html')  # Сторінка для управління алертами

@app.route('/video')
def video():
    global is_video_playing
    if is_video_playing:
        return jsonify({"videoPath": "", "timestamp": ""})

    if command_queue:
        is_video_playing = True
        command_data = command_queue.pop(0)  # Витягуємо першу команду з черги
        video_path = command_data['video_path']
        timestamp = command_data['timestamp']
        username = command_data['username']
        
        return jsonify({"videoPath": f"/videos/{os.path.basename(video_path)}", "timestamp": timestamp})
    else:
        return jsonify({"videoPath": "", "timestamp": ""})

@app.route('/video-ended', methods=['POST'])
def video_ended():
    global is_video_playing
    is_video_playing = False
    return '', 204  # Повертає статус 204 (No Content)

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(os.getcwd(), filename)

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Повертає порожню відповідь без вмісту для усунення помилки

def run_server():
    app.run(host="0.0.0.0", port=5000)

# Створіть відповідні файли шаблонів (HTML) у папці `templates`: index.html, commands.html, alerts.html.
