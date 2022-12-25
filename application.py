"""
An application in Flask that makes allows the user to enter a news source and keyword(s).
The user can then view a summary of the articles.
The sources/keywords provided by the user are stored in a mysql table.
Details about the articles returned are stored in a second mysql table.

Author: Andrew Scott
"""
from flask import Flask, jsonify, request, abort
import requests
import dbconfig as cfg
from flask import render_template
from newsDAO import newsDAO
from datetime import datetime
import mysql.connector

app = Flask(__name__, static_url_path='', static_folder='static')

# Use the source id and keyword provided to fetch news articles using NewsAPI
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

# Return all the entries in the sources database table in JSON format
@app.route('/sourcesjson')
def get_all_source():
    results = newsDAO.get_all_source()
    return jsonify(results)

# Return all the entries in the sources articles table in JSON format
@app.route('/articlesjson')
def get_all_articles():
    results = newsDAO.get_all_articles()
    return jsonify(results)

# Render the articles returned by NewsAPI with the all_articles.html template
@app.route('/articles')
def view_all_articles():
    articles = newsDAO.get_all_articles()
    return render_template("all_articles.html", articles=articles)

# return the articles to display using the template.html file, add to articles mysql table
@app.route("/articles/<int:id>")
def articles(id):
    # Get the id associated with the row the user wishes to see the results for
    #id = request.args.get('id')
    # Uses the id of the source table to get the information to get articles from NewsAPI
    source_info = newsDAO.get_id_source(id)
    source = source_info["source"]
    keyword = source_info["keyword"]   
    articles = get_articles(source, keyword)
    for article in articles:
        title = article["title"]
        title = title[:255]
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
def add_sources():
    source = request.form['source']
    keyword = request.form['keyword']  
    values = (source, keyword)
    id = newsDAO.create_source(values)
    return jsonify(source)

# Delete source from sources mysql table
@app.route('/sources/<int:id>' , methods=['DELETE'])
def delete(id):
    newsDAO.delete_source(id)
    return jsonify({"done":True})

# Update source from sources mysql table
@app.route('/sources/<int:id>', methods=['PUT'])
def update_source(id):
    source = request.form['source']
    keyword = request.form['keyword']
    values = (source, keyword, id)
    newsDAO.update_source(values)
    return jsonify({"done":True})



if __name__ == "__main__":
    newsDAO.create_database()
    newsDAO.create_source_table()
    newsDAO.create_article_table()
    newsDAO.first_source()
    print("testing")
    app.run(debug=True)