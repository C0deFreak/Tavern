from scripts import create_app

app = create_app()

if __name__ == "__main__":
    from waitress import serve
    app.run(host='0.0.0.0', port=5000, debug=True)
