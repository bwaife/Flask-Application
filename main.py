from flask import Flask,request
import xmlrpc.client
from newsapi import NewsApiClient
import http.client
from datetime import datetime
import logging
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
    studentfirstname = request.args.get('studentfirstname')
    studentlastname = request.args.get('studentlastname')
    studentnumber = request.args.get('studentnumber')
    name = date.strftime("%H:%M:%S")+ " " + studentfirstname + " " + studentlastname + " " + studentnumber + '\n'
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
    studentfirstname = request.args.get('studentfirstname')
    # Provide a GraphQL query
    query = gql(
        """
        query getStudent($studentfirstname: String)
       { 
       studentQueryByFName(studentfirstname: $studentfirstname) {
      
      studentfirstname
      studentlastname
      studentnumber
    }

    }
    """
    )

    values = {"studentfirstname" : studentfirstname}

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
                                          from_param='2021-03-11',
                                          to='2021-03-17',
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
    date = datetime.now()
    log = open('calls.log', 'a')
    log_val = '' + str(date) + '-' + request.path + '\n'
    log.write(log_val)

    return 'Pong' + date.strftime("%H:%M:%S")

@app.route('/log')
def log():
    date = datetime.now()
    l = open('calls.log', 'a')
    log_val = '' + str(date) + '-' + request.path + '\n'
    l.write(log_val)
    return 'Log complete '


@app.route('/hprose')
def get_ip():
    date = datetime.now()
    l = open('calls.log', 'a')
    client = hprose.HttpClient("http://127.0.0.1:8080/")
    ipaddr = client.getIpAddress()
    log_val = '' + str(date) + '-' + request.path + '\n'
    l.write(log_val)
    #print("Ip Adddress = ", client.getIpAddress())
    return 'Ip address = ' + ipaddr




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


