import streamlit as st

# Streamlit UI Configuration
st.set_page_config(page_title="Threat Report", layout="wide")
st.title("📊 AI-Generated Cybersecurity Threat Report")

# Read and display report
report_filename = "security_report.md"

try:
    with open(report_filename, "r", encoding="utf-8") as f:
        report_content = f.read()
    st.markdown(report_content)

    # Provide Download Button
    st.download_button(
        label="📥 Download Report",
        data=report_content,
        file_name="security_report.md",
        mime="text/markdown"
    )

except FileNotFoundError:
    st.error("⚠️ No report found. Please run the analysis in `app.py` first.")
