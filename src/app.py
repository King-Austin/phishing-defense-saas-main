from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the AI-powered Phishing Defense Platform"

if __name__ == '__main__':
    app.run(debug=True)
