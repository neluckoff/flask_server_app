from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, send
from server import Server

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
server = Server()


@socketio.on('message')
def message_handler(message):
    command = server.command(message).replace('\r', '')
    result = command.split('\n')
    send(f'~/# {message}')
    for row in result:
        send(row, broadcast=True)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    server.start()
    socketio.run(app, host='localhost', allow_unsafe_werkzeug=True)
