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

# Gradio interface setup
with gr.Blocks() as iface:
    gr.Markdown("# 📈 Real-time recent logs")
    with gr.Column():
        gr.DataFrame(fetch_all_logs(), every=5)


if __name__ == '__main__':
    iface.queue().launch(share=True)
