# Virtual enviroment

(optional) Setup a virtual environment

    # Create a virtual environment
    python -m venv .venv

    # activate it
    .venv\Scripts\activate

    # deactivate it with
    # .venv\Scripts\deactivate


# Install Flask and other libraries

    pip install Flask flask_login flask_cors flask_sqlalchemy sqlalchemy


# Flask Backend

Make a backend.py

    from flask import Flask, send_from_directory
    import random
    app = Flask(__name__)

    @app.route("/hello")
    def hello():
        return f"{random.randint(1, 100)} Hello World!"


    if __name__ == "__main__":
        app.run(debug=True)

Now the backend will effectively serve the frontend

    # Run this to run your backend
    flask run --app backend --debug
