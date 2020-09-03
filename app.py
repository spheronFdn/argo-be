from flask import Flask, request as req
from flask_socketio import emit, SocketIO, send
import docker

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
client = docker.from_env()

@app.route('/')
def hello_world():
    return 'Hello World!'


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, debug=True)
