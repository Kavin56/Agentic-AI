from crewai import Task
from tools import tool
from agents import military_news_researcher, military_news_writer

# Military News Research Task
research_task = Task(
    description=(
        "Investigate and summarize the latest developments in global military affairs. "
        "Focus on official defense reports, military conflicts, and technological advancements."
        "Provide verified information with credibility and neutrality."
    ),
    expected_output="A structured military news report highlighting key global events.",
    tools=[tool],
    agent=military_news_researcher
)

# Military News Writing Task
write_task = Task(
    description=(
        "Draft a TV-style military news script based on extracted information. "
        "Ensure the report is engaging, fact-based, and delivered with clarity."
        "Format the script to be suitable for a news anchor reading on-air."
    ),
    expected_output="A news script formatted for TV narration, saved as `military_news.txt`.",
    tools=[tool],
    agent=military_news_writer,
    async_execution=False,
    output_file='military_news.txt'
)
