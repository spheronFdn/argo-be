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
    framework = args[2]
    package_manager = args[3]
    topic = args[4]
    build_command = args[5]
    publish_dir = args[6]
    is_workspace=args[7]
    workspace=args[8]

    image = 'argo'+framework

    if github_url:
        container = client.containers.run(image, detach=True, environment={
            "GIT_HUB_URL": github_url,
            "FOLDER_NAME": folder_name,
            "BUILD_COMMAND": build_command,
            "PUBLISH_DIR": publish_dir,
            "PACKAGE_MANAGER": package_manager,
            "IS_WORKSPACE":is_workspace,
            "WORKSPACE":workspace
        })

        for log in container.logs(stream=True):
            logstr = str(log, 'utf-8')
            print(logstr)
            socketio.emit(topic, logstr)

    result = container.wait()
    print('Build Results', result)
    socketio.emit('buildResult', 'Error - {} and Status Code - {}'.format(
        result['Error'], result['StatusCode']))


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/build_logs')
def build_logs():
    return render_template('logs.html')


@app.route('/request_build/', methods=["POST"])
def request_build():
    data = request.get_json()
    framework = data['framework']
    github_url = data['github_url']
    folder_name = data['folder_name']
    package_manager = data['package_manager']
    topic = data["topic"]
    build_command = data["build_command"]
    publish_dir = data["publish_dir"]
    is_workspace=data["is_workspace"]
    workspace=data["workspace"]
    socketio.start_background_task(start_build_background, github_url,
                                   folder_name, framework, package_manager, topic, build_command, publish_dir,is_workspace,workspace)

    return {'result': 'Build Started'}


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, host=('0.0.0.0'))
