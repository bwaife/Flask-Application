import requests
from flask import Flask
import xmlrpc.client
from newsapi import NewsApiClient
import http.client


app = Flask(__name__)

@app.route('/')
def hello_world():

    return 'Hello, World'
    


@app.route('/justweather')
def get_news():
    # Init
    newsapi = NewsApiClient(api_key='966611677d694731833118dddf7bd7fc')

    # /v2/top-headlines
    all_articles = newsapi.get_everything(q='bitcoin',
                                          sources='bbc-news,the-verge',
                                          domains='bbc.co.uk,techcrunch.com',
                                          from_param='2021-03-11',
                                          to='2021-12-12',
                                          language='en',
                                          sort_by='relevancy',
                                          page=1)
    # Find out what data type we are working with                                           
    print(type(all_articles))

    # output buffer
    output = ''
    # loop over the key and values in the dict
    for k, v in all_articles.items():
        print(k, v)
        output = output + str(v) # add the value onto the buffer

    return output # return buffer with data 


@app.route('/manual')
def manual():
    conn = http.client.HTTPSConnection("http://newsapi.org/v2/everything?q=tesla&from=2021-01-11&sortBy=publishedAt&apiKey=966611677d694731833118dddf7bd7fc")
    conn.request("GET", "/")

@app.route('/rpc')
def call_rpc():
    # calling the RPC server
    with xmlrpc.client.ServerProxy("http://localhost:8001/") as proxy:
        print("3 is even: %s" % str(proxy.is_even(3)))
    
    # printed to the browser
    return 'Called RPC function'
    
    
    
@app.route('/updates')
def justupdates_call():
    f = open('updates.txt', 'r')
    x = f.readlines()
    output = '{'

    print(type(x))
    print(x)

    for item in x:
        #   "line1": "item1",
        output = output + '"line": "'+item + '",'
    f.close()

    # remove the last trailing comma.
    output = output[:-1]

    output = output + '}'

    return output
    
    
    
    