import sys
from crewai import Crew, Process
from tasks import threat_classification_task, security_report_task
from agents import threat_investigator, security_analyst

# Ensure a file path is provided
if len(sys.argv) < 2:
    print("⚠️ Please provide a file to analyze. Example:")
    print("   python crew.py logs.csv")
    sys.exit(1)

file_path = sys.argv[1]

# Forming the Cybersecurity Crew
threat_detection_crew = Crew(
    agents=[threat_investigator, security_analyst],
    tasks=[threat_classification_task, security_report_task],
    process=Process.sequential
)

# Running Threat Detection with File Input
result = threat_detection_crew.kickoff(inputs={"log_file": file_path})

# Save report
report_filename = "security_report.md"
with open(report_filename, "w", encoding="utf-8") as f:
    f.write(result)

print(f"✅ Threat report saved to {report_filename}")
