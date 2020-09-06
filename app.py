from flask import Flask, request, render_template
from flask_socketio import emit, SocketIO, send
import docker

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None)
client = docker.from_env()

def start_build_background(*args):
    print(args)
    github_url = args[0]
    folder_name = args[1]
    package_manager = args[2]

    if package_manager == 'npm':
        image = 'argonpm'
    elif package_manager == 'yarn':
        image = 'argoyarn'
    else:
        image = 'argonpm'

    if github_url:
        container = client.containers.run(image, detach=True, environment={
            "GIT_HUB_URL": github_url,
            "FOLDER_NAME": folder_name
        })

        for log in container.logs(stream=True):
            logstr = str(log, 'utf-8')
            print(logstr)
            socketio.emit('eventLogs', logstr)

    result = container.wait()
    print('Build Results', result)
    socketio.emit('buildResult', 'Error - {} and Status Code - {}'.format(result['Error'], result['StatusCode']))


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/build_logs')
def build_logs():
    return render_template('logs.html')


@app.route('/request_build', methods=["POST"])
def request_build():
    data = request.get_json()
    github_url = data['github_url']
    folder_name = data['folder_name']
    package_manager = data['package_manager']
    socketio.start_background_task(start_build_background, github_url, folder_name, package_manager)

    return {'result': 'Build Started'}


if __name__ == '__main__':
    socketio.run(app, debug=True)
