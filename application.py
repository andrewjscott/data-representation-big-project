from flask import Flask, jsonify, request
import dbconfig as cfg


app = Flask(__name__, static_url_path='', static_folder='static')

# Init news API
newsapi = NewsApiClient(api_key=cfg.mysql['apikey'])



if __name__ == "__main__":
    app.run(debug=True)