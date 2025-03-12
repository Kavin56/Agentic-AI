import streamlit as st
import pandas as pd
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# ✅ Set page config at the beginning
st.set_page_config(page_title="Threat Report", layout="wide")

# ✅ Configure Gemini API
api_key = "AIzaSyD-dLkR-ggyEHIMBAZ_34MJiBHQVfyxOAc"
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ✅ Function to get mitigation strategies
def get_mitigation_strategy(threat_type):
    prompt = f"Suggest the best mitigation strategies for {threat_type} attacks in a cybersecurity environment. Provide concise and effective recommendations."
    response = model.generate_content(prompt)
    return response.text.strip()

# ✅ Load classified logs
df = pd.read_csv("classified_logs.csv")

st.title("🛡️ Threat Mitigation Report")

if df.empty:
    st.warning("No threats detected or logs not classified yet.")
else:
    st.subheader("🔍 Detected Threats")
    st.dataframe(df)

    # ✅ Generate Mitigation Strategies
    st.subheader("🚀 Mitigation Strategies")
    unique_threats = df["Threat Type"].unique()
    
    mitigation_dict = {}
    for threat in unique_threats:
        mitigation_dict[threat] = get_mitigation_strategy(threat)

    # ✅ Display strategies in Streamlit
    for threat, strategy in mitigation_dict.items():
        with st.expander(f"🔹 {threat}"):
            st.write(strategy)

    # ✅ Generate PDF Report using ReportLab
    pdf_filename = "threat_mitigation_report.pdf"
    pdf_path = f"./{pdf_filename}"

    def generate_pdf():
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        y = height - 50  # Starting Y position
        left_margin = 40  # Left margin to avoid text cutoff
        max_width = width - left_margin - 40  # Max text width to avoid cutoff

        c.setFont("Helvetica-Bold", 14)
        c.drawString(180, y, "🛡️ Threat Mitigation Report")
        y -= 30

        c.setFont("Helvetica-Bold", 12)
        c.drawString(left_margin, y, "🔍 Detected Threats:")
        y -= 20
        c.setFont("Helvetica", 10)
        
        for index, row in df.iterrows():
            source_ip = row.get('Source IP', row.get('Src IP', row.get('IP Address', 'Unknown')))
            timestamp = row.get('Timestamp', 'Unknown')
            threat_info = f"- {row['Threat Type']} at {timestamp} (IP: {source_ip})"
            
            wrapped_text = simpleSplit(threat_info, "Helvetica", 10, max_width)
            for line in wrapped_text:
                c.drawString(left_margin, y, line)
                y -= 15
                if y < 50:  # Start a new page if out of space
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 10)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(left_margin, y, "🚀 Mitigation Strategies:")
        y -= 20
        c.setFont("Helvetica", 10)

        for threat, strategy in mitigation_dict.items():
            c.setFont("Helvetica-Bold", 10)
            c.drawString(left_margin, y, f"🔹 {threat}:")
            y -= 15
            c.setFont("Helvetica", 9)

            wrapped_strategy = simpleSplit(strategy, "Helvetica", 9, max_width)
            for line in wrapped_strategy:
                c.drawString(left_margin + 10, y, line)
                y -= 12
                if y < 50:  # New page if needed
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 9)

        c.save()

    generate_pdf()

    # ✅ Allow user to download the PDF
    with open(pdf_path, "rb") as file:
        st.download_button(
            label="📥 Download Report as PDF",
            data=file,
            file_name=pdf_filename,
            mime="application/pdf"
        )
