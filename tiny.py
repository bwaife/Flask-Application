import logging
import xmlrpc.client
from datetime import datetime
from flask import Flask, request
from newsapi import NewsApiClient
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import hprose


app = Flask(__name__)


@app.route('/')
def hello_world():
    date = datetime.now()
    log = open('calls.log', 'a')
    log_val = '' + str(date) + '-' + request.path + '\n'
    log.write(log_val)
    #logging.basicConfig(filename='users.log', encoding='utf-8', level=logging.DEBUG)

    return 'Hello, World'


@app.route('/insertStudent')
def insertstudent():
    date = datetime.now()
    l = open('calls.log', 'a')
    user = open("users.log", 'a')
    log_val = '' + str(date) + '-' + request.path + '\n'
    l.write(log_val)
    studentfirst = request.args.get('studentfirst')
    studentlast = request.args.get('studentlast')
    studentnumber = request.args.get('studentnumber')
    name = date.strftime("%H:%M:%S") + studentfirst + " " + studentlast + " " + studentnumber + '\n'
    user.write(name)
    # logging.info('/insertStudent' + studentid + '-' + studentname + '-' + studentdob)
    return 'Insert student'


@app.route('/students')
def student():
    date = datetime.now()
    l = open('calls.log', 'a')
    log_val = '' + str(date) + '-' + request.path + '\n'
    l.write(log_val)
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="http://localhost:4000/graphql")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)
    studentName = request.args.get('studentname')
    # Provide a GraphQL query
    query = gql(
        """
        query getStudent($studentname: String)
       { 
       studentQueryByName(studentname: $studentname) {
      studentid
      studentname
      studentdob
    }

    }
    """
    )

    values = {"studentname" : studentName}

    # Execute the query on the transport
    result = client.execute(query, values)
    print(result)
    return result


@app.route('/justweather')
def get_news():
    date = datetime.now()
    log = open('calls.log', 'a')
    log_val = '' + str(date) + '-' + request.path + '\n'
    log.write(log_val)
    # Init
    newsapi = NewsApiClient(api_key='966611677d694731833118dddf7bd7fc')

    # /v2/top-headlines
    all_articles = newsapi.get_everything(q='bitcoin',
                                          sources='bbc-news,the-verge',
                                          domains='bbc.co.uk,techcrunch.com',
                                          from_param='2021-01-11',
                                          to='2021-12-12',
                                          language='en',
                                          sort_by='relevancy',
                                          page=2)
    # Find out what data type we are working with
    print(type(all_articles))

    # output buffer
    output = ''
    # loop over the key and values in the dict
    for k, v in all_articles.items():
        print(k, v)
        output = output + str(v)  # add the value onto the buffer

    return output  # return buffer with data

@app.route('/updates')
def justupdates_call():
    date = datetime.now()
    l = open('calls.log', 'a')
    log_val = '' + str(date) + '-' + request.path + '\n'
    l.write(log_val)
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

@app.route('/ping')
def ping():

    return 'Pong'

@app.route('/log')
def log():
    date = datetime.now()
    l = open('calls.log', 'a')
    log_val = '' + str(date) + '-' + request.path + '\n'
    l.write(log_val)
    return 'Log complete '



@app.route('/callClient')
def call_client():
    date = datetime.now()
    l = open('calls.log', 'a')
    log_val = '' + str(date) + '-' + request.path + '\n'
    l.write(log_val)
    # calling the client server
    #text = request.form['text']
    with xmlrpc.client.ServerProxy("http://127.0.0.1:8001/") as proxy:
        print('connected')
        # print("weather is: %s" % str(proxy.temp_resolver(3)))
        res = proxy.temp_resolver(11)
        # printed to the browser
        return "weather is: %s" % res


