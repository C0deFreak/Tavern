from scripts import create_app
from scripts.libraries import *
from scripts.socketio_instance import socketio

app = create_app()
socketio.init_app(app)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
