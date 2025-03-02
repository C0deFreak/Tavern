from scripts import create_app
from scripts.libraries import *
from waitress import serve
from scripts.socketio_instance import socketio

app = create_app()
socketio.init_app(app)

if __name__ == "__main__":
    # Pokrećemo aplikaciju putem Waitress servera
    serve(app, host='0.0.0.0', port=5000)
