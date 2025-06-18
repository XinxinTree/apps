import streamlit as st
import requests
import json
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="Secure Code Quality Evaluator",
    page_icon="🔍",
    layout="wide"
)

# Add title and description
st.title("Secure Code Quality Evaluator")
evaluators = ["correctness", "maintainability", "security"]

# Create sidebar with options
with st.sidebar:
    st.header("Evaluator Options")
    selected_evaluators = st.multiselect(
        "Select Evaluators",
        evaluators,
        default=evaluators
    )

# Main content area
with st.container():
    st.write("""
    This application evaluates the quality of your code using multiple metrics:
    - Correctness: Code correctness and functionality
    - Maintainability: Code structure and readability
    - Security: Potential security vulnerabilities
    """)

    # Code input area
    code_input = st.text_area(
        "Enter your code to evaluate:",
        height=300,
        placeholder="Paste your code here..."
    )

    # Submit button
    if st.button("Evaluate Code"):
        if not code_input.strip():
            st.error("Please enter some code to evaluate!")
            st.stop()

        # Prepare request
        request_data = {
            "code": code_input,
            "evaluators": selected_evaluators
        }

        try:
            # Make request to FastAPI backend
            response = requests.post(
                "http://localhost:8000/evaluate",
                json=request_data
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Display results
                st.subheader("Evaluation Results")
                
                # Overall score
                st.metric(
                    "Overall Score",
                    f"{result['overall_score']:.2f}",
                    delta="Higher is better"
                )
                
                # Individual evaluator results
                st.subheader("Detailed Results")
                for evaluator, details in result['results'].items():
                    with st.expander(f"{evaluator.capitalize()} Results"):
                        st.json(details)
                        
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
