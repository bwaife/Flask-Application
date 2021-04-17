

import requests

r = requests.get('http://newsapi.org/v2/everything?q=tesla&from=2021-01-11&sortBy=publishedAt&apiKey=966611677d694731833118dddf7bd7fc')

print(r.status_code)

print(r.text)