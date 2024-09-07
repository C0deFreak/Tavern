Setup
Svelte Frontend

    npm init vite      # choose Svelte, JS and name your app "frontend" 
    cd frontend        # replace with the app name you chose
    npm install        # install dependencies

And then you want to automatically build when there's a change in your frontend, you do that with:

    npm run build --watch

(optional if --watch doesn't work properly) In your package.json add in scripts "autobuild": "vite build --watch"

    {
    "name": "frontend",
    "private": true,
    "version": "0.0.0",
    "type": "module",
    "scripts": {
        "dev": "vite",
        "build": "vite build",
        "preview": "vite preview",
        "autobuild": "vite build --watch"
    },
    "devDependencies": {
        "@sveltejs/vite-plugin-svelte": "^3.0.0",
        "svelte": "^4.2.3",
        "vite": "^5.0.0"
    }
    }

And then run instead:

    npm run autobuild

Flask Backend

(optional) Setup a virtual environment

    # Create a virtual environment
    python -m venv .venv

    # activate it
    .venv\Scripts\activate

    # deactivate it with
    # .venv\Scripts\deactivate

Install Flask

    pip install Flask flask_login flask_cors flask_sqlalchemy sqlalchemy

Connecting both
Flask Backend

Make a backend.py

    # Taken from https://github.com/cabreraalex/svelte-flask-example/blob/master/server.py
    # And tweaked/updated for this post

    from flask import Flask, send_from_directory
    import random
    app = Flask(__name__)

    # << CHANGE THIS TO WHATEVER YOUR FRONTEND APP IS CALLED >>
    FRONTEND_APP = 'frontend'

    # Path for our main Svelte page
    @app.route("/")
    def base():
        return send_from_directory(f'{FRONTEND_APP}/dist', 'index.html')

    # Path for all the static files (compiled JS/CSS, etc.)
    @app.route("/<path:path>")
    def home(path):
        return send_from_directory(f'{FRONTEND_APP}/dist', path)


    @app.route("/hello")
    def hello():
        return f"{random.randint(1, 100)} Hello World!"


    if __name__ == "__main__":
        app.run(debug=True)

Now the backend will effectively serve the frontend

    # Run this to run your backend
    flask run --app backend --debug

Connecting to the backend from Svelte

In src/App.svelte delete w/e you got there by default and put:


    <script>
    let message = "Click the button below to get the message from Flask!"
    let host = 'http://localhost:5000'
    function getMessage() {
        fetch(host + '/index')
            .then(response => response.text())
            .then(data => {
                message = data
            })
    }

    </script>


    <h2>{message}</h2>

    <button on:click={getMessage}>Get Message</button>

Basically all you need is to fetch from /hello from here and tadaaa done.
Learning resources

    svelte: https://svelte.dev/ the tutorial is pretty neat, it's super easy to pick up.

    flask: read the doc https://flask.palletsprojects.com/en/3.0.x/server/ , can't help you there I use django exclusively, and beside the most basic of things idk how to do anything with flask, but if it's just serving stuff then you're set :)

Alternatives

You can (and at some point should) switch to sveltekit

    npm create svelte@latest myapp
    cd myapp
    npm install
    npm run dev


To push to github:
    git add --all
    git commit -m "message"
    git push

If you get errors you may need to do:
    git fetch
    git rebase
