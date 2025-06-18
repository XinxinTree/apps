# Risk Signal Analyzer

A tool for processing incident reports and system logs to extract risk signals and generate actionable summaries.

## Features

- Analyzes incident reports and system logs
- Extracts risk signals using keyword matching and TF-IDF
- Generates comprehensive risk summaries
- Provides severity categorization and recommendations
- Interactive Streamlit dashboard
- RESTful API interface

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the package:
```bash
pip install .
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Streamlit dashboard:
```bash
streamlit run app.py
```

2. (Optional) Start the FastAPI backend:
```bash
uvicorn main:app --reload
```

## Usage

Access the dashboard at `http://localhost:8501` and:
1. Choose between analyzing an incident report or uploading a log file
2. View real-time analysis results with visualizations
3. Get actionable recommendations based on the analysis

## API Endpoints

- `POST /analyze/incident`: Analyze an incident report
- `POST /analyze/log`: Analyze a system log file
- `GET /health`: Health check endpoint

## Example Usage with API

```python
import requests

# Analyze an incident report
report = {
    "title": "System Performance Issue",
    "description": "The system has been experiencing high latency and performance degradation",
    "timestamp": "2025-06-17T22:00:00",
    "severity": "HIGH"
}

response = requests.post("http://localhost:8000/analyze/incident", json=report)
print(response.json())

# Analyze a log file
with open("system.log", "rb") as f:
    response = requests.post(
        "http://localhost:8000/analyze/log",
        files={"file": f}
    )
print(response.json())
```

## Streamlit Interface

Access the Streamlit interface at `http://localhost:8501` and:
1. Choose between analyzing an incident report or uploading a log file
2. View real-time risk signal analysis
3. Visualize severity distribution with interactive charts
4. Get actionable recommendations

## API Endpoints

- `POST /analyze/incident`: Analyze an incident report
- `POST /analyze/log`: Analyze a system log file
- `GET /health`: Health check endpoint

## Example Usage with Streamlit

1. Open `http://localhost:8501` in your browser
2. Select "Incident Report" and enter your report details
3. Or select "System Log File" and upload a log file
4. View the analysis results in the dashboard

## Example Usage with API

```python
import requests

# Analyze an incident report
report = {
    "title": "System Performance Issue",
    "description": "The system has been experiencing high latency and performance degradation",
    "timestamp": "2025-06-17T22:00:00",
    "severity": "HIGH"
}

response = requests.post("http://localhost:8000/analyze/incident", json=report)
print(response.json())

# Analyze a log file
with open("system.log", "rb") as f:
    response = requests.post(
        "http://localhost:8000/analyze/log",
        files={"file": f}
    )
print(response.json())
```
