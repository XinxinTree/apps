import json
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import List, Dict, Any

class DataProcessor:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.incidents = []
        self.logs = []
        
    def load_sample_data(self) -> None:
        """Load sample data from JSON and log files."""
        # Load incidents
        with open(os.path.join(self.data_dir, "sample_incidents.json"), "r") as f:
            self.incidents = json.load(f)
            
        # Load logs
        with open(os.path.join(self.data_dir, "sample_logs.txt"), "r") as f:
            self.logs = f.read().splitlines()
            
    def process_incidents(self) -> List[Dict[str, Any]]:
        """Process and enrich incident data."""
        processed_incidents = []
        for incident in self.incidents:
            processed = {
                "title": incident["title"],
                "description": incident["description"],
                "timestamp": incident["timestamp"],
                "severity": incident["severity"],
                "category": self._categorize_incident(incident["description"]),
                "priority": self._determine_priority(incident["severity"]),
                "time_to_resolve": self._estimate_resolution_time(incident["severity"]),
                "impact_level": self._calculate_impact(incident["description"])
            }
            processed_incidents.append(processed)
        return processed_incidents
    
    def process_logs(self) -> List[Dict[str, Any]]:
        """Process and enrich log data."""
        processed_logs = []
        for log in self.logs:
            try:
                timestamp, level, message = self._parse_log_entry(log)
                processed = {
                    "timestamp": timestamp,
                    "severity": level,
                    "message": message,
                    "category": self._categorize_log(message),
                    "priority": self._determine_priority(level),
                    "time_to_resolve": self._estimate_resolution_time(level),
                    "impact_level": self._calculate_impact(message)
                }
                processed_logs.append(processed)
            except ValueError:
                continue
        return processed_logs
    
    def _parse_log_entry(self, log: str) -> tuple:
        """Parse log entry into timestamp, level, and message."""
        timestamp_str, level, message = log.strip()[1:].split(" ", 2)
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return timestamp.strftime("%Y-%m-%d %H:%M:%S"), level, message
    
    def _categorize_incident(self, description: str) -> str:
        """Categorize incident based on description."""
        if "latency" in description.lower() or "performance" in description.lower():
            return "performance"
        elif "network" in description.lower() or "connectivity" in description.lower():
            return "network"
        elif "data" in description.lower() or "backup" in description.lower():
            return "data"
        elif "security" in description.lower() or "authentication" in description.lower():
            return "security"
        return "unknown"
    
    def _categorize_log(self, message: str) -> str:
        """Categorize log message based on content."""
        if "latency" in message.lower() or "performance" in message.lower():
            return "performance"
        elif "network" in message.lower() or "connectivity" in message.lower():
            return "network"
        elif "data" in message.lower() or "backup" in message.lower():
            return "data"
        elif "security" in message.lower() or "authentication" in message.lower():
            return "security"
        return "unknown"
    
    def _determine_priority(self, severity: str) -> int:
        """Determine priority level based on severity."""
        if severity == "HIGH":
            return 1
        elif severity == "MEDIUM":
            return 2
        return 3
    
    def _estimate_resolution_time(self, severity: str) -> str:
        """Estimate time to resolve based on severity."""
        if severity == "HIGH":
            return "1-2 hours"
        elif severity == "MEDIUM":
            return "2-4 hours"
        return "4+ hours"
    
    def _calculate_impact(self, text: str) -> int:
        """Calculate impact level based on keywords in text."""
        impact_keywords = {
            "critical": 5,
            "error": 4,
            "failure": 4,
            "high": 4,
            "warning": 3,
            "slow": 3,
            "degradation": 3,
            "warning": 2
        }
        
        impact = 1
        text_lower = text.lower()
        for keyword, weight in impact_keywords.items():
            if keyword in text_lower:
                impact = max(impact, weight)
        return impact

def load_and_process_data():
    """Load and process all sample data."""
    processor = DataProcessor()
    processor.load_sample_data()
    
    incidents = processor.process_incidents()
    logs = processor.process_logs()
    
    return incidents, logs

if __name__ == "__main__":
    incidents, logs = load_and_process_data()
    print("\nProcessed Incidents:")
    for incident in incidents:
        print(f"Title: {incident['title']}")
        print(f"Category: {incident['category']}")
        print(f"Priority: {incident['priority']}")
        print("-" * 50)
    
    print("\nProcessed Logs:")
    for log in logs:
        print(f"Timestamp: {log['timestamp']}")
        print(f"Category: {log['category']}")
        print(f"Priority: {log['priority']}")
        print("-" * 50)
