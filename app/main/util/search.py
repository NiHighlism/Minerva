from flask import current_app
from logging import getLogger

LOG = getLogger(__name__)

def create_index(index, model):
    es = current_app.elasticsearch
    es.indices.delete(index=index, ignore=[400, 404])

    try:
        payload = {
        "settings" : {
            "number_of_replicas" : 1
        },
        "mappings" : {
            "properties" : {
                "title" : { 
                    "type" : "text" 
                },
                "year" : {
                    "type" : "long"
                },
                "actor" : {
                    "type" : "nested", 
                    "properties" : {
                        "actorList" : {
                        "type" : "text"
                    }}
                },
                "country" : {
                    "type" : "nested", 
                    "properties" : {
                        "countryList" : {
                        "type" : "text"
                    }}
                },
                "director" : {
                    "type" : "nested", 
                    "properties" : {
                        "directorList" : {
                        "type" : "text"
                    }}
                },
                "language" : {
                    "type" : "nested", 
                    "properties" : {
                        "languageList" : {
                        "type" : "text"
                    }}
                }
            }
            }
        }
        es.indices.create(index=index, body=payload)
        return True
    
    except BaseException:
        LOG.error("Elastic Search Index couldn't be create. Try again later.", exc_info=True) 
        return False

def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, query, page, per_page):
    page = int(page)
    per_page = int(per_page)

    if not current_app.elasticsearch:
        return [], 0
    try:
        search = current_app.elasticsearch.search(
            index=index,
            body = {
                'query': {
                    'multi_match': {
                        'query': query, 
                        'fields': ["title^2", "year^1", "*"]
                        }
                    },
                    "from" : (page - 1) * per_page,
                    "size" : per_page
                })
        ids = [int(hit['_id']) for hit in search['hits']['hits']]
        return ids, search['hits']['total']['value']
    
    except Exception as e:
        LOG.error("FUCKED UP", exc_info=True)
        
    
