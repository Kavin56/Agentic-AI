import os
from crewai import Agent
from tools import tool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Call Gemini model
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash',
                            verbose=True,
                            temperature=0.5,
                            google_api_key=os.getenv('GOOGLE_API_KEY'))               

# Military News Researcher Agent
military_news_researcher = Agent(
        role="Military Analyst",
        goal="Gather and analyze the latest military news from reliable sources.",
        verbose=True,
        memory=True,
        backstory="A defense journalist passionate about reporting strategic updates worldwide.",
        tools=[tool],
        llm=llm,
        allow_delegation=True
)

# Military News Writer Agent
military_news_writer = Agent(
    role="News Presenter",
    goal="Convert military updates into an engaging television-style news script.",
    verbose=True,
    memory=True,
    backstory="A charismatic news anchor delivering authoritative military reports.",
    tools=[tool],
    llm=llm,
    allow_delegation=False
)
