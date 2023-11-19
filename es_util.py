from elasticsearch import Elasticsearch
import es_config as es_conf
import hashlib

def es_connection():
    es = Elasticsearch(
        cloud_id=es_conf.CLOUD_ID,
        basic_auth=(es_conf.ELASTIC_USERNAME, es_conf.ELASTIC_PASSWORD)
    )
    return es

def check_elasticsearch_connection(es):
    try:
        info = es.info()
        print("Elasticsearch cluster information:")
        print(f"Cluster Name: {info['cluster_name']}")
        print(f"Cluster Version: {info['version']['number']}")
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {e}")

def create_index(index_name):
    es=es_connection()
    es.indices.create(index=index_name)

def generate_unique_id(data):
    data_str=str(data)
    sha256_hash = hashlib.sha256(data_str.encode()).hexdigest()
    return sha256_hash[:40]

def ingest_data(index_name, body):
    es=es_connection()
    doc_id = generate_unique_id(data=body)
    x=es.index(index=index_name, body=body, id=doc_id)
    return x['_id']

def get_es_data(index_name, query={}):
    es=es_connection()
    q_body={'size' : 20,
            'query': {
                'match_all' : query
                }
            }
    res=es.search(index=index_name, body=q_body)
    hits = res["hits"]["hits"]
    data=[]
    for hit in hits:
        data.append(hit['_source'])
        # print(f"Document ID: {hit['_id']}, Data: {hit['_source']}")
    return data

def search_es_data(index_name, query={}):
    must_clauses = [
        {"term": {key + ".keyword": value}} for key, value in query.items() if ("date" not in key and value != "" and key != "metadata")
    ]
    if query["metadata"] != "":
        metadata_search = {"term": {"metadata.parentResourceId.keyword": query["metadata"]}}
        must_clauses.append(metadata_search)
    print("must clause: ")
    print(must_clauses)
    q_body={}
    if(query["start_date"]!=""):
        q_body = {
            "query": {
                "bool": {
                    "must": must_clauses,
                    "filter": {
                        "range": {
                            "timestamp": {"gte": query["start_date"], "lte": query["end_date"]}
                        }
                    }
                }
            }
        }
    else:
        q_body = {
            "query": {
                "bool": {
                    "must": must_clauses,
                }
            }
        }
    es=es_connection()
    res = es.search(index=index_name, body=q_body)
    hits = res["hits"]["hits"]
    data=[]
    for hit in hits:
        data.append(hit['_source'])
    return data

# print(search_es_data("logs", query={'level': '', 'message': '', 'resourceId': '', 'start_date': '', 'end_date': '', 'traceId': '', 'spanId': '', 'commit': '', 'metadata': 'server-007'}))
# print(get_es_data("logs"))
# es=es_connection()
# check_elasticsearch_connection(es)