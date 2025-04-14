from crewai import Crew, Process
from tasks import research_task, write_task
from agents import military_news_researcher, military_news_writer

# Crew formation for news broadcasting
crew = Crew(
    agents=[military_news_researcher, military_news_writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
)

# Start execution with a specific news category
result = crew.kickoff(inputs={'topic': 'Military Operations and Defense Strategy'})
print(result)
