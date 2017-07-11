# encoding: iso-8859-1

from flask import Flask, Response, jsonify, request
from flask import make_response as apiResponse
from utilApi import serializer, API_DATA_KEYS, API_DOC
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'neoway-one'
app.config['MONGO_URI'] = 'mongodb://mfrata:sudofrata@ds129459.mlab.com:29459/neoway-one'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def index():
    '''
    Returns the options of the api in text format
    [to be vizualized in the browser]
    '''
    resp = apiResponse(API_DOC)
    resp.headers['Content-type'] = 'text/plain; charset=utf-8'
    return resp

@app.route('/keys', methods=['GET'])
def api_keys_get():
    '''
    Return all keys of th database schema
    '''
    return apiResponse(jsonify({'keys':API_DATA_KEYS}))

@app.route('/news', methods=['GET'])
def api_news_get():
    '''
    Return all news based on the requests filters
    '''
    #finding the news in the mongodb
    all_documents = mongo.db.news.find(request.args.to_dict())
    if all_documents.count() > 0:
        return apiResponse(serializer(all_documents))
    else:
        return apiResponse('',404)

@app.route('/news', methods=['POST'])
def api_news_post():
    '''
    Creates a existing news on the database
    '''
    #saving in the mongodb
    news_collection = mongo.db.news
    #inserting
    newDocummentId = news_collection.insert(request.json)
    #checking if resource was created
    if news_collection.find_one({'_id': newDocummentId }):
        return apiResponse(jsonify({'_id': str(newDocummentId) }), 201)
    else:
        return apiResponse('Could not create resource', 400)

@app.route('/news', methods=['PATCH'])
def api_news_patch():
    '''
    Updates a existing news on the database
    '''
    #checking if a filter was passed
    if request.args.to_dict() == {}:
        return apiResponse('No filter specified.', 400)
    #checking if a update data was passed
    if request.json == {}:
        return apiResponse('No update data specified', 400)
    #saving in the mongodb
    try:
        mongo.db.news.update_one(request.args.to_dict(),{'$set':request.json},
            upsert=False)
    except Exception as e:
        return apiResponse(e, 422)
    return apiResponse('done', 201)

@app.route('/news', methods=['OPTIONS'])
def api_news_options():
    '''
    Returns the options of the api
    '''
    return apiResponse(API_DOC)

if __name__ == '__main__':
    app.run(debug=True)
