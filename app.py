# encoding: iso-8859-1

from flask import Flask, Response, jsonify, request
from flask import make_response as apiResponse
from utilApi import jsonRaw, format_dict, API_DATA_KEYS, API_DOC
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'neoway-one'
app.config['MONGO_URI'] = 'mongodb://mfrata:sudofrata@ds129459.mlab.com:29459/neoway-one'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def index():
    resp = apiResponse(API_DOC)
    resp.headers['Content-type'] = 'text/plain; charset=utf-8'
    return resp

@app.route('/keys', methods=['GET'])
def api_keys():
    return apiResponse(jsonify({'keys':API_DATA_KEYS}))

@app.route('/news', methods=['GET', 'POST', 'PATCH', 'OPTIONS'])
def api_news():
    """
    News Api for neoway-one team Project

    For more info:

    OPTIONS on /news

    Parameters
    ----------
    None

    Returns
    -------
    json
        json of the filtered news

    """
    if request.method == 'GET':
        #filtering keys on the url
        filters_keys = [key for key in request.args.keys() if key in API_DATA_KEYS]
        filter_dict = format_dict(request.args.to_dict(), filters_keys)
        #finding the news in the mongodb
        all_documents = mongo.db.news.find(filter_dict)
        if all_documents.count() > 0:
            return apiResponse(jsonRaw(all_documents))
        else:
            return apiResponse('',404)

    elif request.method == 'POST':
        #saving in the mongodb
        news_collection = mongo.db.news
        newDocummentId = news_collection.insert(format_dict(request.json, API_DATA_KEYS))
        #checking if resource was created
        if news_collection.find_one({'_id': newDocummentId }):
            return apiResponse(jsonify({'_id': str(newDocummentId) }), 201)
        else:
            return apiResponse('Could not create resource', 400)

    elif request.method == 'PATCH':
        #filtering keys on the url
        filters_keys = [key for key in request.args.keys() if key in API_DATA_KEYS]
        filtered_args = format_dict(request.args.to_dict(), filters_keys)
        if filtered_args == {}:
            return apiResponse('No filter specified.', 400)
        #filtering keys on the payload
        filters_keys =  set(request.json.keys()).intersection(API_DATA_KEYS)
        filtered_values = format_dict(request.json, filters_keys)
        if filtered_values == {}:
            return apiResponse('No update data specified', 400)
        #saving in the mongodb
        try:
            mongo.db.news.update_one(filtered_args,{'$set':filtered_values},
                upsert=False)
        except Exception as e:
            return apiResponse(e, 422)
        return apiResponse('done', 204)

    elif request.method == 'OPTIONS':
        return apiResponse(API_DOC)

    else:
        return apiResponse('',405)


if __name__ == '__main__':
    app.run(debug=True)
