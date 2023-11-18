from elasticsearch import Elasticsearch
import es_config as es_conf
def es_connection():
    es = Elasticsearch(
        cloud_id=es_conf.CLOUD_ID,
        basic_auth=(es_conf.ELASTIC_USERNAME, es_conf.ELASTIC_PASSWORD)
    )
    return es

def check_elasticsearch_connection():
    es = es_connection()
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

# check_elasticsearch_connection()