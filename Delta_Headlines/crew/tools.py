import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from crewai_tools import SerperDevTool

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

tool = SerperDevTool()

NEWS_DB_PATH = "military_news.txt"


def ocr_extract_text(image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(["Extract text from this image:", image])
    return response.text.strip()


def store_in_pinecone(news_text):
    with open(NEWS_DB_PATH, "a", encoding="utf-8") as file:
        file.write(news_text + "\n\n")


def retrieve_from_pinecone(query):
    if not os.path.exists(NEWS_DB_PATH):
        return "No relevant military news found."

    with open(NEWS_DB_PATH, "r", encoding="utf-8") as file:
        news_entries = file.readlines()

    if not news_entries:
        return "No relevant military news found."

    return "".join(news_entries[-5:])


def generate_news_from_gemini(query):
    retrieved_news = retrieve_from_pinecone(query)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    You are a professional news reader. Based on the following retrieved information, generate a structured and engaging news script:

    {retrieved_news}
    """

    response = model.generate_content(prompt)
    return response.text.strip()


tools = {
    "search": tool,
    "ocr": ocr_extract_text,
    "store_news": store_in_pinecone,
    "retrieve_news": retrieve_from_pinecone,
    "generate_news": generate_news_from_gemini
}
