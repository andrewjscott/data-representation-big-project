from flask import Flask, jsonify, request
import requests
import dbconfig as cfg
from flask import render_template
from newsDAO import newsDAO


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

# Accessing different elements of the returned articles
# https://www.geeksforgeeks.org/python-get-values-of-particular-key-in-list-of-dictionaries/
x = get_articles("bbc-news", "stretch")
urls = [ sub['url'] for sub in x ]
titles = [ sub['title'] for sub in x ]
date = [ sub['publishedAt'] for sub in x ] 


# return the articles to display using the template.html file
@app.route("/articles")
def articles():
    source = "bbc-news"
    keyword = "stretch"   
    articles = get_articles(source, keyword)
    return render_template("template.html", articles=articles)

# Add the sources to the sources mysql table 
@app.route('/sources', methods=['POST'])
def update():
    if not request.json:
        abort(400)
    # other checking 
    source = {
        "source": request.json['source'],
        "keyword": request.json['keyword'],
    }
    values =(source['source'], source['keyword'])
    new_id = newsDAO.create_source(values)
    source['id'] = new_id
    return jsonify(source)


if __name__ == "__main__":
    app.run(debug=True)