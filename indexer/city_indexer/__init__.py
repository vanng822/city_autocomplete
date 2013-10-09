from pyelasticsearch import ElasticSearch
from datetime import datetime
import threading
local_data = threading.local()



"""

curl -X PUT localhost:9200/city_names


curl -X PUT localhost:9200/city_names/name/_mapping -d '{
  "name" : {
        "properties" : {
            "name" : { "type" : "string" },
            "suggest" : { "type" : "completion",
                          "index_analyzer" : "simple",
                          "search_analyzer" : "simple",
                          "payloads" : true
            }
        }
    }
}'

"""

def get_es():
    try:
        es = local_data.es
    except:
        es = ElasticSearch('http://localhost:9200/')
        local_data.es = es
    #print id(es)
    return es

"""
{
    "name" : "Nevermind",
    "suggest" : {
        "input": [ "Nevermind", "Nirvana" ],
        "output": "Nirvana - Nevermind",
        "payload" : { "artistId" : 2321 },
        "weight" : 34
    }
}

"""
def index_name_suggestion(data):
    payload = {}
    payload['timestamp'] = datetime.now()
    payload['name'] = data['name']
    payload['longitude'] = data['longitude']
    payload['latitude'] = data['latitude']

    index_data = {}
    index_data['name'] = data['name']
    index_data['suggest'] = {
                             'input': [data['name']],
                             'output': data['name'],
                             "payload": payload
                             }
    es = get_es()
    es.index('city_names', 'name', index_data)


