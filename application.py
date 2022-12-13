from flask import Flask, jsonify, request

app = Flask(__name__, static_url_path='', static_folder='static')



if __name__ == "__main__":
    app.run(debug=True)