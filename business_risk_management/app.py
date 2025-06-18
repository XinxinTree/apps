import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from pathlib import Path
import os

# Configure Streamlit
st.set_page_config(
    page_title="Business Risk Management Platform",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'risk_data' not in st.session_state:
    st.session_state.risk_data = pd.DataFrame()
if 'risk_assessment' not in st.session_state:
    st.session_state.risk_assessment = {}

# Load sample data if exists
DATA_PATH = Path(__file__).parent / "data"
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

@st.cache_data
def load_sample_data():
    """Load sample risk data"""
    sample_data = {
        'Risk Category': ['Financial', 'Operational', 'Reputational', 'Compliance', 'Strategic'],
        'Likelihood': [0.3, 0.4, 0.2, 0.5, 0.3],
        'Impact': [0.8, 0.7, 0.9, 0.6, 0.8],
        'Current Controls': ['Partial', 'Strong', 'Weak', 'Moderate', 'Strong'],
        'Mitigation Status': ['In Progress', 'Complete', 'Planned', 'In Progress', 'Complete']
    }
    return pd.DataFrame(sample_data)

# Main app
st.title("Business Risk Management Platform")

# Sidebar - Navigation
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Go to",
        ["📊 Dashboard", "📝 Risk Assessment", "🔍 Risk Analysis", "🤖 AI Assistant"]
    )

# Main content based on selected page
if page == "📊 Dashboard":
    st.header("Risk Management Dashboard")
    
    # Load or create sample data
    if st.session_state.risk_data.empty:
        st.session_state.risk_data = load_sample_data()
    
    # Risk Heatmap
    st.subheader("Risk Heatmap")
    fig = px.scatter(
        st.session_state.risk_data,
        x="Likelihood",
        y="Impact",
        size="Impact",
        color="Risk Category",
        hover_name="Risk Category",
        labels={
            "Likelihood": "Risk Likelihood",
            "Impact": "Risk Impact"
        }
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk Categories Distribution
    st.subheader("Risk Categories Distribution")
    fig = px.pie(
        st.session_state.risk_data,
        names="Risk Category",
        title="Risk Categories Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "📝 Risk Assessment":
    st.header("Risk Assessment Form")
    
    with st.form("risk_assessment_form"):
        risk_category = st.selectbox(
            "Risk Category",
            ["Financial", "Operational", "Reputational", "Compliance", "Strategic", "Other"]
        )
        
        risk_description = st.text_area(
            "Risk Description",
            "Please describe the potential risk..."
        )
        
        likelihood = st.slider(
            "Likelihood (0-1)",
            0.0, 1.0, 0.5, 0.1
        )
        
        impact = st.slider(
            "Impact (0-1)",
            0.0, 1.0, 0.5, 0.1
        )
        
        controls = st.text_area(
            "Current Controls",
            "List existing controls to mitigate this risk..."
        )
        
        mitigation_status = st.selectbox(
            "Mitigation Status",
            ["Planned", "In Progress", "Complete", "Not Started"]
        )
        
        submitted = st.form_submit_button("Submit Risk Assessment")
        
        if submitted:
            new_risk = {
                "Risk Category": risk_category,
                "Risk Description": risk_description,
                "Likelihood": likelihood,
                "Impact": impact,
                "Current Controls": controls,
                "Mitigation Status": mitigation_status,
                "Date Added": datetime.now().strftime("%Y-%m-%d")
            }
            
            # Save to session state
            if 'risk_assessments' not in st.session_state:
                st.session_state.risk_assessments = []
            st.session_state.risk_assessments.append(new_risk)
            st.success("Risk assessment submitted successfully!")

elif page == "🔍 Risk Analysis":
    st.header("Risk Analysis")
    
    if not st.session_state.risk_data.empty:
        st.subheader("Risk Analysis Summary")
        
        # Calculate risk scores
        st.session_state.risk_data['Risk Score'] = \
            st.session_state.risk_data['Likelihood'] * \
            st.session_state.risk_data['Impact']
        
        # Display top risks
        st.subheader("Top 5 Risks by Score")
        top_risks = st.session_state.risk_data.sort_values(
            'Risk Score', ascending=False
        ).head(5)
        st.dataframe(top_risks)
        
        # Risk trend analysis
        st.subheader("Risk Trend Analysis")
        fig = px.line(
            st.session_state.risk_data,
            x="Risk Score",
            y="Risk Category",
            title="Risk Score Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No risk data available. Please add some risk assessments first.")

elif page == "🤖 AI Assistant":
    st.header("AI Risk Management Assistant")
    
    # TODO: Implement AI integration with OpenAI/LangChain
    st.warning("AI Assistant integration coming soon!")
    
    # Placeholder for AI features
    st.info("""
    This section will provide AI-powered assistance for:
    - Risk identification and categorization
    - Risk mitigation strategy recommendations
    - Natural language processing for risk documentation
    - Automated risk pattern detection
    """)

# Footer
st.markdown("---")
with st.expander("About"):
    st.write("""
    This platform helps organizations manage and mitigate business risks by:
    - Identifying potential risks
    - Assessing risk likelihood and impact
    - Tracking mitigation efforts
    - Providing data-driven insights
    - Integrating AI for enhanced risk management
    """)
