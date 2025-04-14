from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
import google.generativeai as genai
import requests
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
import requests
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import io

# Set up Streamlit UI
st.set_page_config(page_title="AI Military News Reader", layout="wide")
st.title("📰 AI-Powered Military News Reader & Audio Broadcaster")

# Load environment variables
load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")
# Initialize ElevenLabs Client
client = ElevenLabs(api_key=api_key)

# Voice Mapping for Languages
voice_ids = {
    "English": "EXAVITQu4vr4xnSDxMaL",  # Example: Sarah (Change if needed)
    "French": "Xb7hH8MSUJpSbSDYk0k2",   # Example: Alice
    "German": "XrExE9yKIg1WjnnlVkGX",   # Example: Matilda
}

# API Keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "military-news")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
if PINECONE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(name=PINECONE_INDEX_NAME, dimension=384, metric="cosine")

index = pc.Index(PINECONE_INDEX_NAME)

# Initialize Embeddings Model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Select Language
selected_language = st.sidebar.selectbox("Select Language", ["English", "French", "German"])
voice_id = voice_ids.get(selected_language, voice_ids["English"])  # Default to English

def ocr_extract_text(image):
    """Extract text from an image using Gemini-1.5-Flash OCR."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(["Extract text from this image:", image])
    return response.text.strip()

def store_in_pinecone(news_text):
    """Store extracted text in Pinecone."""
    vector = embeddings.embed_query(news_text)  
    pinecone_payload = {
        "id": news_text[:30],  
        "values": vector,
        "metadata": {"source": "news"}
    }
    _ = index.upsert(vectors=[pinecone_payload])

def retrieve_from_pinecone(query):
    """Retrieve military news using Serp or Serper API."""
    url = "https://serpapi.com/search"
    params = {
        "q": query + " military news",
        "api_key": SERP_API_KEY,
        "num": 5
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json().get("organic_results", [])
        if results:
            return "\n\n".join([f"🔹 {r['title']}: {r['link']}" for r in results])
    
    return generate_military_news(query)

def generate_military_news(query):
    """Generate military news using Gemini AI."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Generate a current, realistic military news report in {selected_language}:
    {query}
    Include country, location, military activities, and official statements.
    """
    response = model.generate_content(prompt)
    return response.text.strip()

import re

def generate_structured_news(query, language, script_type):
    """Generate structured news in the selected language."""
    retrieved_news = retrieve_from_pinecone(query)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    if script_type == "news":
        prompt = f"""
        You are a professional news scriptwriter. Structure the following news information into a well-organized TV-style script in {language}.
        - Include speaker labels such as 'Anchor:', 'Reporter:', etc.
        - Ensure the script follows a professional news format.
        """
    else:
        prompt = f"""
        You are a professional news scriptwriter. Generate a short 4-6 line anchor speech for the news in {language}.
        - No speaker labels like 'Anchor:'.
        - Write in {language}.
        - Do not use special characters like * or #.
        """

    prompt += f"\n\nHere is the news content:\n{retrieved_news}"
    
    response = model.generate_content(prompt)
    
    # Clean output
    news_text = response.text.strip()
    if script_type == "anchor_speech":
        news_text = re.sub(r"\*\*.*?:\*\*", "", news_text)  # Remove labels
        news_text = re.sub(r"\(.*?\)", "", news_text)  # Remove parenthesis content
    
    return news_text.strip()

# Sidebar for uploading an image
st.sidebar.header("📤 Upload Image for Analysis")
uploaded_file = st.sidebar.file_uploader("Upload a news-related image", type=["png", "jpg", "jpeg"])

# Main page layout
if uploaded_file:
    st.header("🖼️ Image Preview & Text Extraction")
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Extracting text from image..."):
        extracted_text = ocr_extract_text(image)
    st.success("✅ Text Extracted!")

    # Show extracted text
    st.subheader("Extracted Military News Text")
    st.text_area("Extracted Text:", extracted_text, height=200)

    # Store extracted text in Pinecone
    store_in_pinecone(extracted_text)

    # Retrieve related news
    st.subheader("📡 Retrieving Related News...")
    with st.spinner("🔍 Retrieving news..."):
        retrieved_news = retrieve_from_pinecone(extracted_text)
    st.success("📡 Related News Retrieved!")

    # Display similar news
    st.text_area("Similar Military News:", retrieved_news, height=200)

    # Generate AI News Script
    with st.expander("📝 Generate AI News Script"):
        if st.button("Generate AI News Script"):
            with st.spinner("📜 Generating structured news script..."):
                structured_news = generate_structured_news(extracted_text, selected_language, script_type="news")
            st.success("✅ Structured News Script Generated!")

            with st.spinner("📜 Generating anchor speech script..."):
                anchor_script = generate_structured_news(extracted_text, selected_language, script_type="anchor_speech")
            st.success("✅ Anchor Speech Script Generated!")

            st.text_area("📰 AI-Generated Military News Script:", structured_news, height=400)
            st.text_area("🎤 Anchor Speech Script:", anchor_script, height=300)
            
            with st.spinner("🎤 Converting text to speech..."):
                audio_stream  = client.text_to_speech.convert(
                    text=anchor_script,
                    voice_id=voice_id,
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128"
                )
                audio_bytes = b"".join(audio_stream)
                st.audio(io.BytesIO(audio_bytes), format="audio/mp3")
            st.success("🎧 Audio Playback Complete!")

