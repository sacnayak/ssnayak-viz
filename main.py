"""`main` is the top level module for your Flask application."""
# Imports
import os
import jinja2
import webapp2
import logging
import json
import urllib
from datetime import datetime

# Import the Flask Framework
from flask import Flask, request
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
# this is used for constructing URLs to google's APIS
from googleapiclient.discovery import build

#set up the Jinja2 Environment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

API_KEY = 'AIzaSyCGwxXuzIH6NIXsCh0x0i7Kn5l3PQsK7fo'
# This uses discovery to create an object that can talk to the 
# fusion tables API using the developer key
service = build('fusiontables', 'v1', developerKey=API_KEY)

TABLE_ID = '1R4VPwxsNq_XvNRj-v2eAP10FmLt8-QUNgUVgWWYt'

#Define Flask application
app = Flask(__name__)

@app.route('/')
def hello():
    template = JINJA_ENVIRONMENT.get_template('templates/index.html')
    return template.render()

@app.route('/_update_table', methods=['POST']) 
def update_table():
    logging.info(request.get_json())
    date = request.json['date']
    date = datetime.strptime(date, "%Y-%m-%d").strftime("%m/%d/%Y")
    result = get_all_data(make_query(date))
    return json.dumps({'content' : result['rows'], 'headers' : result['columns']})

@app.route('/about')
def about():
    template = JINJA_ENVIRONMENT.get_template('templates/about.html')
    return template.render()

@app.route('/quality')
def quality():
    template = JINJA_ENVIRONMENT.get_template('templates/quality.html')
    return template.render()

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

def get_all_data(query):
    response = service.query().sql(sql=query).execute()
    logging.info(response['columns'])
    logging.info(response['rows'])
    return response

def make_query(date):	
	query = "SELECT * FROM " + TABLE_ID + " WHERE date='" + date + "'"
	logging.info("The query to be made: ")
	logging.info(query)
	
	return query