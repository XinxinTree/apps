# Secure Code Quality Evaluator

A production-ready system for evaluating AI-generated code across multiple dimensions:
- Correctness
- Maintainability
- Security

## Features

- Comprehensive code analysis using static analysis tools
- RESTful API for easy integration into enterprise workflows
- Detailed reports with actionable insights
- Security vulnerability scanning
- Code complexity analysis
- Style and maintainability checks
- Authentication and authorization

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
