import streamlit as st
import pandas as pd
import json
import os
import subprocess  # To call report.py
from bs4 import BeautifulSoup
from crewai import Crew, Process
from agents import threat_investigator, security_analyst
from tasks import create_dynamic_threat_classification_task, security_report_task
from tools import threat_classifier_tool, ip_lookup_tool

# Streamlit UI Configuration
st.set_page_config(page_title="AI-Powered Threat Detection", layout="wide")
st.title("🔍 AI-Powered Cybersecurity Threat Analysis")

# Sidebar Navigation
st.sidebar.title("Navigation")
if st.sidebar.button("📊 View Threat Report"):
    subprocess.Popen(["streamlit", "run", "report.py"])
    st.sidebar.success("Opening Threat Report...")

# File Upload Section
uploaded_file = st.file_uploader("Upload log files (CSV, JSON, TXT, HTML)", type=["csv", "json", "txt", "html"])

def process_uploaded_file(file):
    """Reads uploaded log file and returns structured data."""
    file_type = file.name.split(".")[-1].lower()
    
    try:
        if file_type == "json":
            return json.load(file)
        elif file_type == "html":
            soup = BeautifulSoup(file.read(), "html.parser")
            return [{"log_entry": soup.get_text()}]
        elif file_type == "csv":
            df = pd.read_csv(file)
            return df.to_dict(orient="records")
        elif file_type in ["txt", "log"]:
            return [{"log_entry": line.strip()} for line in file.read().decode("utf-8", errors="ignore").splitlines() if line.strip()]
        else:
            return [{"error": "Unsupported file format."}]
    except Exception as e:
        return [{"error": f"Failed to process file: {str(e)}"}]

# Run Analysis Button
if uploaded_file:
    st.subheader("📂 Extracted Logs")
    log_data = process_uploaded_file(uploaded_file)
    
    if "error" in log_data[0]:
        st.error(f"⚠️ {log_data[0]['error']}")
    else:
        st.json(log_data[:10])  # Show first 10 logs

        # Dynamically Create Threat Classification Task
        threat_classification_task = create_dynamic_threat_classification_task(log_data)

        # CrewAI Threat Analysis Execution
        with st.spinner("🔎 Analyzing logs..."):
            threat_detection_crew = Crew(
                agents=[threat_investigator, security_analyst],
                tasks=[threat_classification_task, security_report_task],
                process=Process.sequential
            )
            result = threat_detection_crew.kickoff()

        # Save report to a file
        report_filename = "security_report.md"
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(result)

        st.success("✅ Analysis Complete! Open the Threat Report from the Sidebar.")
