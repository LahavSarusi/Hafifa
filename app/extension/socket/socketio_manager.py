from flask_socketio import SocketIO
from app import flask_app

socketio = SocketIO(
    app=flask_app,
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
)


@socketio.on('connect')
def on_connect():
    print('Client connected')


@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')
