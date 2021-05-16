from flask import Flask, request, render_template
from flask_socketio import emit, SocketIO, send
import docker
import json
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None)
client = docker.from_env()
api_cli = docker.APIClient()


def calc_buildtime_in_microseconds(container_state):
    def erase_microseconds(time):
        return time.split('.')[0]

    format = "%Y-%m-%dT%H:%M:%S"
    start_time = container_state['StartedAt']
    end_time = container_state['FinishedAt']   

    start = erase_microseconds(start_time)
    end = erase_microseconds(end_time)

    start_datetime = datetime.strptime(start, format)
    end_datetime = datetime.strptime(end, format)

    return int((end_datetime - start_datetime).total_seconds() * 1000)


def _checkForImage(imagename):
    try:
        client.images.get(imagename)
        return True
    except docker.errors.ImageNotFound:
        return False
    except:
        return None


def start_build_background(*args):
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
    imageExists = _checkForImage(image)

    if imageExists == False:
        socketio.emit(f'build-error-{topic}', json.dumps({
            'statusCode': 1,
            'msg': f'Image {image} does not exists',
        }))
    elif imageExists == None:
        socketio.emit(f'build-error-{topic}', json.dumps({
            'statusCode': 1,
            'msg': 'Internal API error',
        }))
    else:
        # Why did we check if github url exists?
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
            socketio.emit(topic, logstr)

        result = container.wait()
        build_time = calc_buildtime_in_microseconds(api_cli.inspect_container(container.id)['State'])
        container.remove()

        if result['StatusCode']:
            socketio.emit(f'build-error-{topic}', json.dumps({
                'statusCode': 1,
                'msg': result['Error'],
            }))
        else:
            socketio.emit(f'build-success-{topic}', json.dumps({
                'statusCode': 0,
                'msg': 'Build success',
                'buildTime': build_time,
            }))


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
