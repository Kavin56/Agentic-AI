# 📡 AI Military News Reader

## 🚀 Project Overview
The **AI Military News Reader** is an advanced AI-powered web application that extracts military news from images, retrieves related news articles using external APIs, and generates structured TV-style news scripts with text-to-speech functionality.

## 🛠️ Features
- 🖼️ **OCR Extraction**: Extracts text from uploaded military news images using Azure & Tesseract.
- 📖 **Summarization**: Uses BART (Hugging Face) and Gemini (Google AI) for high-quality text summarization.
- 🔍 **News Retrieval**: Fetches related military news via Serp API and enhances it with AI-generated reports.
- 📝 **AI News Script**: Structures raw news into a professional TV-style script.
- 🎙️ **Text-to-Speech**: Converts AI-generated news scripts into an audio format.
- 📡 **Pinecone Integration**: Stores and retrieves news embeddings for future reference.

## 📂 Installation
### 🔽 Clone the Repository
```bash
git clone https://github.com/Kavin56/Delta.git
cd Delta
```

### 🖥️ Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔑 Set Up Environment Variables
Create a `.env` file in the project root and add your API keys:
```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=us-east-1
PINECONE_INDEX_NAME=military-news
GOOGLE_API_KEY=your_google_api_key
SERP_API_KEY=your_serp_api_key
```

## 🚀 Running the Application
```bash
streamlit run app.py
```

## 🏗️ Project Structure
```
📂 crew/
│-- 📜 app.py           # Streamlit web application
│-- 📜 requirements.txt # List of dependencies
│-- 📜 .env             # Environment variables
│-- 📜 crew.py             # Environment variables
│-- 📜 tools.py             # Environment variables
│-- 📜 agents.py             # Environment variables
│-- 📜 tasks.py             # Environment variables





```

## 🤝 Contributing
Feel free to submit issues, feature requests, or pull requests to improve the project!


## 🌟 Acknowledgments
- **Google Gemini** for OCR and AI-generated news.
- **Pinecone** for vector search.
- **SerpAPI** for fetching real-time news articles.
- **Streamlit** for building the UI.
