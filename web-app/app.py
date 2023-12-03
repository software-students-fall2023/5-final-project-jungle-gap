from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Personal Finance Tracker!"})

if __name__ == '__main__':
    app.run(debug=True)
