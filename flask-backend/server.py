from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/members")
def members():
    return jsonify({"members": ["Luka", "Baga", "Simun"]})

if __name__ == "__main__":
    app.run(debug=True, port=2371)