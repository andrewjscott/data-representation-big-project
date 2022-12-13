# Import required modules
from flask import Flask, request
import mysql.connector

# Create Flask app and configure database
app = Flask(__name__, static_url_path='', static_folder='static')
config = {
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'database': 'newsapp',
}
cnx = mysql.connector.connect(**config)

# Define NewsSource model
class NewsSource:
    def __init__(self, name, url):
        self.name = name
        self.url = url

# Create endpoint for creating a new news source
@app.route('/api/news-sources', methods=['POST'])
def create_news_source():
    # Get data from request body
    data = request.get_json()
    name = data['name']
    url = data['url']

    # Create new NewsSource instance
    news_source = NewsSource(name=name, url=url)

    # Add news source to database
    cursor = cnx.cursor()
    query = f"INSERT INTO news_sources (name, url) VALUES ('{name}', '{url}')"
    cursor.execute(query)
    cnx.commit()

    # Return success message
    return flask.jsonify({'message': 'News source created successfully'})
