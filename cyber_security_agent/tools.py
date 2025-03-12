import os
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import Tool

load_dotenv()

# Initialize Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# AI-Powered Threat Classifier Function
def classify_threat(log_entry: str) -> str:
    """Classifies security logs into threat categories using Gemini AI."""
    prompt = f"Analyze the following log and classify it into one of these categories: DDoS, SQLi, Phishing, Malware, Unauthorized Access, Suspicious, Failure, No_Threat.\n\nLog: {log_entry}"
    
    try:
        response = llm.invoke(prompt)
        return response if response else "Unknown"
    except Exception as e:
        return f"Error: {str(e)}"

# Define the threat classifier tool
threat_classifier_tool = Tool(
    name="Threat Classifier",
    description="Classifies security logs into threat categories using Gemini AI.",
    func=classify_threat  # Ensure the function is correctly assigned
)

# IP Geolocation Lookup Function
def get_ip_geolocation(ip: str) -> dict:
    """Fetches geolocation data for a given IP address."""
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        return response.json()
    except Exception as e:
        return {"error": f"Unable to fetch geolocation: {str(e)}"}

# Define the IP lookup tool
ip_lookup_tool = Tool(
    name="IP Lookup",
    description="Retrieves geolocation details for an IP address.",
    func=get_ip_geolocation  # Ensure the function is correctly assigned
)
