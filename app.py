from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread
import os

app = Flask(__name__)
socketio = SocketIO(app)

users = {}

def handle_connect(sid):
    users[sid] = Thread(target=user_thread, args=(sid,))
    users[sid].start()

def user_thread(sid):
    while True:
        socketio.sleep(0)  # Permite que outros eventos sejam tratados
        socketio.on_event('message', handle_message, namespace='/', room=sid)

@socketio.on('connect')
def handle_connect_event():
    emit('connected', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect_event():
    emit('disconnected', {'data': 'Disconnected'})

@socketio.on('message')
def handle_message(message):
    emit('broadcast', message, broadcast=True, include_self=False)

@app.route('/')
def index():
    return render_template('client.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.getenv("PORT")), allow_unsafe_werkzeug=True)
