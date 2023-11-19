import gradio as gr
import requests
import pandas as pd

# Function to fetch all logs from the Flask app
def fetch_all_logs():
    response = requests.get('http://localhost:3000/get')  # Assuming Flask app is running on localhost:3000
    if response.status_code == 200:
        es_data=response.json()["es_data"]
        return pd.DataFrame(es_data)
    else:
        return {"error": "Failed to retrieve data from Flask app"}

# Function to search log data in the Flask app
def search_logs(query_val):
    query={}
    l=["level", "message", "resourceId", "start_date", "end_date", "traceId", "spanId", "commit", "metadata"]
    for i, key in enumerate(query_val):
        query[l[i]]=query_val[key]
    if(query["start_date"]!="" and query["end_date"]==""):
        query["start_date"]=query["end_date"]
    # print(query)
    response = requests.post('http://localhost:3000/search', json=query)
    if response.status_code == 200:
        es_data=response.json()["search_data"]
        print(es_data)
        return pd.DataFrame(es_data)
    else:
        return {"error": "Failed to search and retrieve data"}

# Function to submit log data to the Flask app
def submit_log(log_data_val):
    log_data={}
    l=["level", "message", "resourceId", "timestamp", "traceId", "spanId", "commit", "metadata"]
    for i, key in enumerate(log_data_val):
        if(l[i]!="metadata"):
            log_data[l[i]]=log_data_val[key]
        else:
            log_data[l[i]]={"parentResourceId":log_data_val[key]}
    print(log_data)
    response = requests.post('http://localhost:3000/ingest', json=log_data)
    if response.status_code == 201:
        return "Log ingested successfully!"
    else:
        return {"error": "Failed to ingest log"}

def greet(name):
    return "Hello " + name + "!"

# Gradio interface setup
with gr.Blocks() as demo:
    with gr.Tab("Home"):
        gr.Markdown("# 📈 Real-time recent logs")
        with gr.Column():
            gr.DataFrame(fetch_all_logs(), every=5)
    with gr.Tab("Search"):
        level = gr.Textbox(label="Level")
        message = gr.Textbox(label="Message")
        resourceId = gr.Textbox(label="Resource ID")
        start_date = gr.Textbox(label="Start Date or just timestamp(YYYY-MM-DDTHH:mm:ssZ)")
        end_date = gr.Textbox(label="End Date(optional) (YYYY-MM-DDTHH:mm:ssZ)")
        traceId = gr.Textbox(label="Trace ID")
        spanId = gr.Textbox(label="Span ID")
        commit = gr.Textbox(label="Commit")
        metadata = gr.Textbox(label="metadata_parentResourceId")
        gr.Button("Search").click(fn=search_logs, inputs={level, message, resourceId, start_date, end_date, traceId, spanId, commit, metadata}, outputs=gr.DataFrame(), every=5)            
    with gr.Tab("Ingest"):
        level = gr.Textbox(label="level")
        message = gr.Textbox(label="message")
        resourceId = gr.Textbox(label="resource ID")
        timestamp = gr.Textbox(label="timestamp")
        traceId = gr.Textbox(label="traceId")
        spanId = gr.Textbox(label="spanId")
        commit = gr.Textbox(label="commit")
        metadata=gr.Textbox(label="metadata_parentResourceId")
        output = gr.Textbox(label="Output")
        gr.Button("Ingest").click(fn=submit_log, inputs={level, message, resourceId, timestamp, traceId, spanId, commit, metadata}, outputs=output)

if __name__ == '__main__':
    demo.queue().launch(share=True)
