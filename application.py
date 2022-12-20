from flask import Flask, jsonify, request, abort
import requests
import dbconfig as cfg
from flask import render_template
from newsDAO import newsDAO
from datetime import datetime


app = Flask(__name__, static_url_path='', static_folder='static')

def get_articles(source, keyword):
    api_key = cfg.api_keys['newsapikey']
    base_url = "https://newsapi.org/v2/everything" 
    params = {
        "sources": source,
        "q": keyword,
        "apiKey": api_key
    }
    response = requests.get(base_url, params=params) 
    if response.status_code == 200:
        articles = response.json()["articles"]
        for article in articles:
            title = article["title"]
            author = article["author"]
            description = article["description"]
            url = article["url"]
            date_published = article["publishedAt"]
            source = article["source"]["name"]       
        return articles      
    else:
        print(f"Request failed with status code {response.status_code}")

@app.route('/sourcesjson')
def get_all_source():
    results = newsDAO.get_all_source()
    return jsonify(results)

@app.route('/articlesjson')
def get_all_articles():
    results = newsDAO.get_all_articles()
    return jsonify(results)

# return the articles to display using the template.html file, add to articles mysql table
@app.route("/articles")
def articles():
    # Uses the id of the source table to get the information to get articles from NewsAPI
    source_info = newsDAO.get_id_source(1)
    source = source_info["source"]
    keyword = source_info["keyword"]   
    articles = get_articles(source, keyword)
    for article in articles:
        title = article["title"]
        author = article["author"]
        description = article["description"]
        # The description can be longer than the MySQL limit so in case it's too long this shortens it
        description = description[:255]
        date = article["publishedAt"]
        # Need to format the date to make it MySQL friendly
        # Parse the date string using the datetime module
        date_parse = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        # Convert the date to a string in the format 'YYYY-MM-DD HH:mm:ss'
        date_published = date_parse.strftime('%Y-%m-%d %H:%M:%S')
        url = article["url"]
        source = article["source"]["name"]
        values = (title, author, description, date_published, url, source)
        new_id = newsDAO.create_article(values)
    # Use render template to display articles - https://www.geeksforgeeks.org/flask-rendering-templates/
    return render_template("articles.html", articles=articles)

# Add the sources to the sources mysql table 
@app.route('/sources', methods=['POST'])
def update_sources():
    source = request.form['source']
    keyword = request.form['keyword']  
    values = (source, keyword)
    new_id = newsDAO.create_source(values)
    source['id'] = new_id
    return jsonify(source)

# Delete source from sources mysql table
@app.route('/sources/<int:id>' , methods=['DELETE'])
def delete(id):
    newsDAO.delete_source(id)
    return jsonify({"done":True})


if __name__ == "__main__":
    app.run(debug=True)