import os
from crewai import Agent
from tools import threat_classifier_tool, ip_lookup_tool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Initialize Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key="AIzaSyD-dLkR-ggyEHIMBAZ_34MJiBHQVfyxOAc"
)

# Threat Investigator Agent
threat_investigator = Agent(
    role="Threat Investigator",
    goal="Analyze logs and classify potential cyber threats.",
    verbose=True,
    memory=True,
    backstory=(
        "As a cybersecurity expert, you specialize in detecting malicious activities "
        "and categorizing them for further investigation."
    ),
    tools=[threat_classifier_tool, ip_lookup_tool],
    llm=llm,
    allow_delegation=True
)

# Security Analyst Agent
security_analyst = Agent(
    role="Security Analyst",
    goal="Generate structured security reports based on classified threats.",
    verbose=True,
    memory=True,
    backstory=(
        "A cybersecurity analyst with expertise in summarizing security insights "
        "and providing actionable recommendations."
    ),
    tools=[],
    llm=llm,
    allow_delegation=False
)
