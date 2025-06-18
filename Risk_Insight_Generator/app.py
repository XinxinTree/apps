import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from data_processor import DataProcessor

# Initialize data processor
processor = DataProcessor()
processor.load_sample_data()

# Process data
incidents, logs = processor.process_incidents(), processor.process_logs()

# Create DataFrame for incidents
incidents_df = pd.DataFrame(incidents)
if 'timestamp' in incidents_df.columns:
    incidents_df['timestamp'] = pd.to_datetime(incidents_df['timestamp'])

# Create DataFrame for logs
logs_df = pd.DataFrame(logs)
if 'timestamp' in logs_df.columns:
    logs_df['timestamp'] = pd.to_datetime(logs_df['timestamp'])

# Add date column for trend analysis
if 'timestamp' in incidents_df.columns:
    incidents_df['date'] = incidents_df['timestamp'].dt.date
if 'timestamp' in logs_df.columns:
    logs_df['date'] = logs_df['timestamp'].dt.date

# Streamlit UI
def main():
    st.title("Risk Signal Analyzer Dashboard")
    
    # Sidebar options
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        ["Incident Analysis", "Log Analysis", "Trend Analysis"],
        key="analysis_type_selector"
    )
    
    if analysis_type == "Incident Analysis":
        st.header("Incident Analysis Dashboard")
        
        # Display incident statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Incidents", len(incidents))
        with col2:
            st.metric("High Priority", len(incidents_df[incidents_df['priority'] == 1]))
        with col3:
            st.metric("Average Impact", incidents_df['impact_level'].mean())
        
        # Incident category distribution
        st.subheader("Incident Category Distribution")
        category_counts = incidents_df['category'].value_counts()
        fig = px.pie(values=category_counts.values, 
                    names=category_counts.index,
                    title="Incident Categories")
        st.plotly_chart(fig)
        
        # Incident priority distribution
        st.subheader("Incident Priority Distribution")
        priority_counts = incidents_df['priority'].value_counts().sort_index()
        fig = px.bar(x=priority_counts.index,
                    y=priority_counts.values,
                    labels={'x': 'Priority Level', 'y': 'Count'},
                    title="Incident Priority Distribution")
        st.plotly_chart(fig)
        
        # Display incidents table
        st.subheader("Recent Incidents")
        st.dataframe(incidents_df.sort_values('timestamp', ascending=False).head(10))
    
    elif analysis_type == "Log Analysis":
        st.header("Log Analysis Dashboard")
        
        # Display log statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Logs", len(logs))
        with col2:
            st.metric("Error Logs", len(logs_df[logs_df['severity'] == 'ERROR']))
        with col3:
            st.metric("Average Impact", logs_df['impact_level'].mean())
        
        # Log category distribution
        st.subheader("Log Category Distribution")
        category_counts = logs_df['category'].value_counts()
        fig = px.pie(values=category_counts.values, 
                    names=category_counts.index,
                    title="Log Categories")
        st.plotly_chart(fig)
        
        # Log severity distribution
        st.subheader("Log Severity Distribution")
        severity_counts = logs_df['severity'].value_counts()
        fig = px.bar(x=severity_counts.index,
                    y=severity_counts.values,
                    labels={'x': 'Severity Level', 'y': 'Count'},
                    title="Log Severity Distribution")
        st.plotly_chart(fig)
        
        # Display logs table
        st.subheader("Recent Logs")
        st.dataframe(logs_df.sort_values('timestamp', ascending=False).head(10))
    
    elif analysis_type == "Trend Analysis":
        st.header("Trend Analysis Dashboard")
        
        # Incident trend over time
        st.subheader("Incident Trend Over Time")
        incidents_df['date'] = incidents_df['timestamp'].dt.date
        incident_trend = incidents_df.groupby('date').size()
        fig = px.line(x=incident_trend.index,
                     y=incident_trend.values,
                     labels={'x': 'Date', 'y': 'Number of Incidents'},
                     title="Daily Incident Trend")
        st.plotly_chart(fig)
        
        # Impact trend over time
        st.subheader("Impact Trend Over Time")
        impact_trend = incidents_df.groupby('date')['impact_level'].mean()
        fig = px.line(x=impact_trend.index,
                     y=impact_trend.values,
                     labels={'x': 'Date', 'y': 'Average Impact Level'},
                     title="Daily Impact Level Trend")
        st.plotly_chart(fig)
        
        # Category trend
        st.subheader("Category Distribution Over Time")
        category_trend = incidents_df.groupby(['date', 'category']).size().unstack().fillna(0)
        fig = px.area(category_trend)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
