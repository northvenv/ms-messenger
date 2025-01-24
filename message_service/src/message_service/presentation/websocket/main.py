import socketio
from message_service.presentation.websocket.routes.chat import sio

from message_service.bootstrap.di import setup_containers

def create_socket_app() -> socketio.ASGIApp:
    app = socketio.ASGIApp(sio, socketio_path="/socket.io")
    setup_containers()

    return app
