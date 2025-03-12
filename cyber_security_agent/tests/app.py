import streamlit as st
import pandas as pd
import json
import random
import datetime
import subprocess
from bs4 import BeautifulSoup
from openai import AzureOpenAI
import plotly.express as px

# Initialize Azure OpenAI Client
client = AzureOpenAI(
    azure_endpoint='https://chen-m44hs78n-swedencentral.cognitiveservices.azure.com/',
    api_key='CeOe3qZF4f3j45XfgDPJ1FWGzKMPkgYtpjSgi0jkhyiH1EAi5s8fJQQJ99AKACfhMk5XJ3w3AAAAACOGihSC',
    api_version='2024-02-15-preview'
)

THREAT_CATEGORIES = [
    "DDoS", "SQLi", "Phishing", "Malware", "Unauthorized Access",
    "Suspicious", "Failure", "No_Threat"
]

# Function to extract logs from various file types
def extract_logs(file):
    file_type = file.name.split(".")[-1].lower()
    try:
        if file_type == "json":
            return json.load(file)
        elif file_type == "html":
            soup = BeautifulSoup(file.read(), 'html.parser')
            return {"html_text": soup.get_text()}
        elif file_type == "csv":
            df = pd.read_csv(file)
            return df.to_dict(orient="records")
        elif file_type in ["txt", "log"]:
            return [{"log_entry": line.strip()} for line in file.read().decode("utf-8", errors="ignore").splitlines() if line.strip()]
        else:
            return {"error": "Unsupported file format."}
    except Exception as e:
        return {"error": f"Failed to process file: {e}"}

# Function to generate a random timestamp
def generate_random_timestamp():
    return (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")

# Function to assign severity levels to threats
def assign_severity(threat_type):
    severity_mapping = {
        "DDoS": "High",
        "SQLi": "High",
        "Phishing": "Medium",
        "Malware": "Critical",
        "Unauthorized Access": "Medium",
        "Suspicious": "Low",
        "Failure": "Low",
        "No_Threat": "None",
        "Anomaly": "Medium"
    }
    return severity_mapping.get(threat_type, "None/Unknown")

# Streamlit UI Configuration
import streamlit as st
import subprocess
import time

# Streamlit Page Config
st.set_page_config(page_title="AI-Powered Threat Detection", layout="wide")
st.title("🔍 AI-Powered Threat Detection Dashboard")

st.sidebar.title("Navigation")

# ✅ View Threat Report
if st.sidebar.button("📊 View Threat Report"):
    subprocess.Popen(["streamlit", "run", "report.py"], shell=True)
    st.sidebar.success("Redirecting to report page...")

# ✅ Run Locust Test
if st.sidebar.button("🚀 Run Locust Test"):
    locust_process = subprocess.Popen(["locust", "-f", "locustfile.py"], shell=True)
    st.sidebar.success("Locust load test started! Open [http://localhost:8089](http://localhost:8089) to view.")

# ✅ Monitor Security Logs
if st.sidebar.button("🔎 Monitor Security Logs"):
    subprocess.Popen(["python", "monitor_security.py"], shell=True)
    st.sidebar.success("Monitoring security logs...")

# ✅ Run Pytest Security Tests
if st.sidebar.button("🛡 Run Security Tests"):
    test_results = st.empty()  # Placeholder for dynamic updates

    pytest_process = subprocess.Popen(["pytest", "test_security.py", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    output_lines = []
    for line in iter(pytest_process.stdout.readline, ""):
        output_lines.append(line.strip())  
        test_results.write("\n".join(output_lines))  # Update the output dynamically

    st.success("✅ Security tests completed!")

# File Upload
uploaded_files = st.file_uploader("Upload log files (JSON, HTML, CSV, TXT, LOG)", 
                                  type=["json", "html", "csv", "txt", "log"], 
                                  accept_multiple_files=True)

all_logs = []
data = []

if uploaded_files:
    for file in uploaded_files:
        logs = extract_logs(file)
        if isinstance(logs, list):
            all_logs.extend(logs)
        elif "error" in logs:
            st.error(f"⚠️ Error in {file.name}: {logs['error']}")

    if all_logs:
        st.subheader("Extracted Logs")
        st.json(all_logs)

        # Threat Classification & DataFrame Creation
        st.subheader("🔐 Threat Classification")
        for log in all_logs[:10]:  # Limit to first 10 logs for processing
            threat_type = random.choice(THREAT_CATEGORIES)  # Assigning random threats for now
            ip_address = log.get("ip", "N/A")
            
            data.append({
                "Timestamp": generate_random_timestamp(),
                "Threat Type": threat_type,
                "Severity": assign_severity(threat_type),
                "IP Address": ip_address,
                "Log Snippet": str(log)[:150]
            })

        df = pd.DataFrame(data)
        df.to_csv("classified_logs.csv", index=False)  # Save for report.py
        
        st.subheader("📋 Classified Logs")
        st.dataframe(df)

        # 📊 Visualizations
        if not df.empty:
            col1, col2 = st.columns(2)
            
            # 🔹 Bar Chart - Threat Distribution (Fixed)
            with col1:
                threat_counts = df["Threat Type"].value_counts().reset_index()
                threat_counts.columns = ["Threat Type", "Count"]
                fig1 = px.bar(threat_counts, x="Threat Type", y="Count", 
                              title="Threat Type Distribution", text_auto=True, 
                              color="Threat Type", template="plotly_dark")
                st.plotly_chart(fig1, use_container_width=True)

            # 🔹 Pie Chart - Severity Levels
            with col2:
                severity_counts = df["Severity"].value_counts().reset_index()
                severity_counts.columns = ["Severity Level", "Count"]
                fig2 = px.pie(severity_counts, names="Severity Level", values="Count", 
                              title="Threat Severity Distribution", template="plotly_dark")
                st.plotly_chart(fig2, use_container_width=True)

            # 🔹 Sunburst Chart - Threats by Severity
            st.subheader("🌞 Threat Classification Breakdown")
            fig3 = px.sunburst(df, path=["Severity", "Threat Type"], values=[1] * len(df),
                               title="Threats by Severity & Type", template="plotly_dark",
                               color="Severity", hover_data=["Threat Type"])
            st.plotly_chart(fig3, use_container_width=True)

        st.success("✅ Threat analysis and visualization completed!")
