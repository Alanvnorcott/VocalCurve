# app.py
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from threading import Thread
from queue import Queue
import time

app = Flask(__name__)

recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Global variables for continuous listening
audio_queue = Queue()
stop_listening = False

def listener_thread():
    global stop_listening
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        while not stop_listening:
            try:
                audio = recognizer.listen(source, phrase_time_limit=3)
                audio_queue.put(audio)
            except sr.WaitTimeoutError:
                pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_listening', methods=['POST'])
def start_listening():
    global stop_listening
    stop_listening = False
    Thread(target=listener_thread).start()
    return jsonify({'success': True, 'message': 'Listening started'})

@app.route('/stop_listening', methods=['POST'])
def stop_listening():
    global stop_listening
    stop_listening = True
    return jsonify({'success': True, 'message': 'Listening stopped'})

@app.route('/recognize', methods=['POST'])
def recognize():
    target_word = request.form.get('target_word', '').lower()

    if audio_queue.empty():
        return jsonify({'success': False, 'error': 'No audio available'})

    audio = audio_queue.get()

    try:
        transcription = recognizer.recognize_google(audio)
        words = transcription.lower().split()
        word_count = words.count(target_word)

        return jsonify({
            'success': True,
            'transcription': transcription,
            'word_count': word_count,
        })
    except sr.RequestError:
        return jsonify({'success': False, 'error': 'API unavailable'})
    except sr.UnknownValueError:
        return jsonify({'success': False, 'error': 'Unable to recognize speech'})

if __name__ == '__main__':
    app.run(debug=True, threaded=True)