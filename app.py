# app.py
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Implement log ingestion endpoint
@app.route('/ingest', methods=['POST'])
def ingest_log():
    log_data = request.get_json()
    es.index(index='logs', body=log_data)
    return jsonify({"message": "Log ingested successfully"}), 201

# Implement log search endpoint
@app.route('/search', methods=['GET'])
def search_logs():
    query_params = request.args.to_dict()
    search_body = {
        "query": {
            "bool": {
                "must": [{"match": {key: value}} for key, value in query_params.items()]
            }
        }
    }
    result = es.search(index='logs', body=search_body)
    return jsonify(result['hits']['hits']), 200

if __name__ == '__main__':
    app.run(port=3000)  # Run Flask app on port 3000
