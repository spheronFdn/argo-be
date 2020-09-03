from flask import Flask, request
from flask_socketio import emit, SocketIO, send
import docker

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None)
client = docker.from_env()


@app.route('/')
def hello_world():
    return 'Hello World!'


def start_build_background(*args):
    print(args)
    github_url = args[0]
    folder_name = args[1]
    if github_url:
        container = client.containers.run('argonew', detach=True, environment={
            "GIT_HUB_URL": github_url,
            "FOLDER_NAME": folder_name
        })

        for log in container.logs(stream=True):
            logstr = str(log, 'utf-8')
            print(logstr)
            socketio.emit('eventLogs', logstr)

    result = container.wait()
    socketio.emit('buildResult', result)


@app.route('/request_build', methods=["POST"])
def request_build():
    data = request.get_json()
    github_url = data['github_url']
    folder_name = data['folder_name']
    socketio.start_background_task(start_build_background, github_url, folder_name)

    return {'result': 'Build Started'}


if __name__ == '__main__':
    socketio.run(app, debug=True)
