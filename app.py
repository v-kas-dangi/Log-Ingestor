# app.py
from flask import Flask, request, jsonify
import es_util as es_util

app = Flask(__name__)

# Implement log ingestion endpoint
@app.route('/ingest', methods=['POST'])
def ingest_log():
    log_data = request.get_json()
    # print(log_data)
    x=es_util.ingest_data(index_name="logs", body=log_data)
    return jsonify({"message": "Log ingested successfully", "doc id": x}), 201

@app.route('/get', methods=['GET'])
def show_recent_logs():
    es_data=es_util.get_es_data("logs")
    return jsonify({"es_data":es_data})

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
    es=es_util.es_connection()
    result = es.search(index="logs", body=search_body)
    return jsonify(result['hits']['hits']), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)  # Run Flask app on port 3000
