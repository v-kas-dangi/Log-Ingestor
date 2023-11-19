<a name="readme-top"></a>

<!-- ABOUT THE PROJECT -->
## About The Project

[![Home-Page][home-page]](https://example.com)

This project is a Flask application for ingesting logs into Elasticsearch and providing a simple interface using Gradio to interact with the data. Elasticsearch is used for storing and querying logs.



<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [Flask](https://flask.palletsprojects.com/)
* [Elasticsearch](https://www.elastic.co/)
* [Gradio](https://www.gradio.app/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Getting Started

To run this project locally, follow these steps:

### Prerequisites

Make sure you have Python installed and have a cloud instance of elastic.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/dyte-submissions/november-2023-hiring-v-kas-dangi.git
2. Install dependencies in the project directory
   ```sh
   pip install -r requirements.txt
   ```
   This should start the server at port 3000.
3. Replace CLOUD_ID with your cloud id and ELASTIC_PASSWORD with your elastic cloud deployment password
4. Start the Flask app in the project directory
   ```sh
   python app.py
5. Start the Gradio app using
   ```sh
   gradio gradio/interface.py
   ```
   This should start the gradio app at the port 7860
6. Open your browser and go to http://localhost:7860 to access the Gradio interface.

<!-- USAGE EXAMPLES -->
## Usage
Utilize the Gradio interface to view the most recent 20 logs, search logs based on filters, and ingest new logs. The interface is organized into three tabs to facilitate these functionalities. To input log data, you must provide each field in a separate text box, both for ingesting and searching logs. It was done to improve user experience. 
<br>
For direct ingestion in JSON format, send a POST request to the server at port 3000 using the /ingest API endpoint.
  ```sh
   http://localhost:3000/ingest
  ```
The Home runs on
  ```sh
   http://localhost:3000/get
  ```
And the Search runs on
  ```sh
   http://localhost:3000/search
  ```
respectively
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Vikas Dangi - [@linkedin](https://www.linkedin.com/in/vikas-dangi-6155b01bb/) - b20238@students.iitmandi.ac.in

Project Link: [Log Ingestor](https://github.com/dyte-submissions/november-2023-hiring-v-kas-dangi)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[home-page]: images/home.png