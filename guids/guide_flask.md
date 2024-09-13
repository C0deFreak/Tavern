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


# Deployment
Install the 'waitress' lib with:

    pip install waitress

For servers make a 'requirements.txt' and input all lib names followed by enter and use:

    pip install -r requirements.txt

Add 'waitress' to 'main.py':

    from scripts import create_app

    app = create_app()

    if __name__ == "__main__":
        from waitress import serve
        serve(app, host='0.0.0.0', port=5000)

Run the server by 'python main.py'