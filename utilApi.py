# encoding: iso-8859-1

from flask import jsonify

API_DATA_KEYS = (
    'title',
    'date',
    'domain',
    'url',
    'categories',
    'tags',
    'people',
    'companies',
    'body'
)

API_DATA_KEYS_TYPE = (
    'string',
    'string',
    'string',
    'string',
    'list of strings',
    'list of strings',
    'list of strings',
    'list of string',
    'string'
)



def jsonRaw(raw):
    """
    Takes the raw input and return in the json format

    Parameters
    ----------
    raw : cursor object or dict

    Returns
    -------
    json
        json of the dicts

    """
    output = []
    if type(raw) is dict:
        output = format_dict(raw, API_DATA_KEYS)
    else:
        output = [format_dict(x, API_DATA_KEYS) for x in raw]
    return jsonify(output)

def format_dict(raw_dict, keys_list):
    """
    Takes the raw dict and return a f formated one given a list of keys

    Parameters
    ----------
    raw_dict : dict
    keys_list : list

    Returns
    -------
    dict
        formated dict
    """
    return {key: raw_dict[key] for key in keys_list}

KEYS_TYPE = zip(API_DATA_KEYS, API_DATA_KEYS_TYPE)

API_DOC = 'GET /news - To receive all the news on the database\n'\
'       Expected responses: 200\n\n'\
'GET /news?filter0=param&filterN=paramN - To receive all the news that pass on those filters\n'\
'       Allowed filters (name, type): {}'.format(KEYS_TYPE)+'\n'\
'       Expected responses: 200, 404\n\n'\
'POST /news - with payload in json format with the previous filters\n'\
'       Expected responses: 201, 400\n\n'\
'OPTIONS /news - To get the api options\n'\
'       Expected responses: 200\n\n'\
'Example: Getting the news that has the category : "Corrupção"\n'\
'       GET /news?categories=Corrupção\n\n'\
'Example: Getting the news that has the category : "Corrupção" and are related to the person "João Silva"\n'\
'       GET /news?categories=Corrupção&people=João+Silva\n\n'\
'GET /keys - To receive all keys of each news on the database\n'\
'       Expected responses: 200\n\n'\
