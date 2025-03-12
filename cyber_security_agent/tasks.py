from crewai import Task
from tools import threat_classifier_tool, ip_lookup_tool
from agents import threat_investigator, security_analyst

def create_dynamic_threat_classification_task(log_data):
    """Creates a Threat Classification Task dynamically using uploaded logs."""
    return Task(
        description=(
            "Analyze security logs and classify them into cyber threat categories. "
            "Use AI to detect potential threats such as DDoS, Phishing, SQLi, Malware, and Unauthorized Access. "
            f"The logs provided contain {len(log_data)} entries."
        ),
        expected_output="A structured classification of threats based on log analysis.",
        tools=[threat_classifier_tool, ip_lookup_tool],
        agent=threat_investigator,
        inputs={"log_data": log_data}  # Pass log data
    )

# Security Report Task (Remains Unchanged)
security_report_task = Task(
    description=(
        "Generate a structured cybersecurity report based on identified threats. "
        "Include severity levels, affected IPs, and recommended mitigations."
    ),
    expected_output="A cybersecurity report with threat summaries and recommendations.",
    tools=[],
    agent=security_analyst,
    async_execution=False,
    output_file="security_report.md"
)
