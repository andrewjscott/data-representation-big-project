import requests
import dbconfig as cfg


# Set API key
api_key = cfg.api_keys['newsapikey']

# Set request parameters
params = {
    "apiKey": api_key,
    "sources": 'bbc-news',

    "q": "technology",
    "sortBy": "publishedAt",
}

# Make request to News API
response = requests.get("https://newsapi.org/v2/everything", params=params)

# Print response
print(response.json())
