from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
import json
from typing import List, Dict

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

app = FastAPI(title="Risk Signal Analyzer")

# Define data models
class IncidentReport(BaseModel):
    title: str
    description: str
    timestamp: str
    severity: str

class RiskSignal(BaseModel):
    category: str
    severity: str
    description: str
    confidence: float

class AnalysisSummary(BaseModel):
    risk_signals: List[RiskSignal]
    overall_severity: str
    recommendations: List[str]

# Risk categories and keywords
RISK_CATEGORIES = {
    "security": ["breach", "attack", "vulnerability", "malware", "hacked"],
    "system": ["failure", "crash", "outage", "performance", "latency"],
    "network": ["connectivity", "bandwidth", "latency", "packet loss"],
    "data": ["corruption", "loss", "integrity", "backup", "restore"]
}

def extract_risk_signals(text: str) -> List[RiskSignal]:
    """Extract risk signals from text using keyword matching and TF-IDF."""
    signals = []
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalpha()]
    
    # Check for risk category keywords
    for category, keywords in RISK_CATEGORIES.items():
        for keyword in keywords:
            if keyword in tokens:
                signal = RiskSignal(
                    category=category,
                    severity="HIGH" if keyword in ["breach", "attack", "failure"] else "MEDIUM",
                    description=f"Potential {category} risk related to {keyword}",
                    confidence=0.85
                )
                signals.append(signal)
    
    return signals

def generate_summary(signals: List[RiskSignal]) -> AnalysisSummary:
    """Generate a comprehensive analysis summary."""
    severity_counts = {
        "HIGH": len([s for s in signals if s.severity == "HIGH"]),
        "MEDIUM": len([s for s in signals if s.severity == "MEDIUM"]),
        "LOW": len([s for s in signals if s.severity == "LOW"])
    }
    
    overall_severity = "HIGH" if severity_counts["HIGH"] > 0 else (
        "MEDIUM" if severity_counts["MEDIUM"] > 0 else "LOW"
    )
    
    recommendations = []
    if severity_counts["HIGH"] > 0:
        recommendations.append("Immediate investigation required for high-severity risks")
    if severity_counts["MEDIUM"] > 0:
        recommendations.append("Monitor and investigate medium-severity risks")
    
    return AnalysisSummary(
        risk_signals=signals,
        overall_severity=overall_severity,
        recommendations=recommendations
    )

@app.post("/analyze/incident")
async def analyze_incident_report(report: IncidentReport):
    """Analyze an incident report and generate risk signals."""
    signals = extract_risk_signals(report.description)
    summary = generate_summary(signals)
    return summary

@app.post("/analyze/log")
async def analyze_log_file(file: UploadFile = File(...)):
    """Analyze a system log file and extract risk signals."""
    contents = await file.read()
    text = contents.decode()
    
    # Split log into individual entries
    log_entries = text.split('\n')
    
    all_signals = []
    for entry in log_entries:
        if entry.strip():
            signals = extract_risk_signals(entry)
            all_signals.extend(signals)
    
    summary = generate_summary(all_signals)
    return summary

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
