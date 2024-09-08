# Svelte Frontend

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


# Connecting to the backend from Svelte

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


# Learning resources

    svelte: https://svelte.dev/ the tutorial is pretty neat, it's super easy to pick up.

    flask: read the doc https://flask.palletsprojects.com/en/3.0.x/server/ , can't help you there I use django exclusively, and beside the most basic of things idk how to do anything with flask, but if it's just serving stuff then you're set :)


# Alternatives

You can (and at some point should) switch to sveltekit

    npm create svelte@latest myapp
    cd myapp
    npm install
    npm run dev