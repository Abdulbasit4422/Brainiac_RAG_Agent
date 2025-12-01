# Agentic AI System

This project is an agentic AI system that uses the Gemini 2.5 flash model. It features multiple agents and function calling, including a RAG chatbot with a Pinecone knowledge base and a Google Search fallback.

## Getting Started

1.  **Set up Environment Variables:**
    Create a `.env` file in the project root (`C:\Users\HP\Desktop\Agent_AI_Project`) by copying `.env.example` and filling in your `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`, `PINECONE_CLOUD`, `PINECONE_REGION`, and `GOOGLE_API_KEY`.

2.  **Populate Pinecone Index with Word Document:**
    The RAG agent relies on a Pinecone index containing your knowledge base. The `populate_pinecone.py` script has been updated to read your Word document.

    First, ensure you have placed your Word document at the specified path within `populate_pinecone.py`:
    `C:\Users\HP\Desktop\Agent_AI_Project\LONGEVITY CHATBOT Q&A KNOWLEDGE BASE .docx`

    Then, run the script to populate your Pinecone index:

    ```bash
    venv\Scripts\python.exe populate_pinecone.py
    ```

    This script will read the Word document, split its content into paragraphs, embed each paragraph, and upsert them into your configured Pinecone index.

3.  **Run the API Server:**
    Once your Pinecone index is populated, you can run the FastAPI server:

    ```bash
    venv\Scripts\python.exe -m src.main
    ```

    This will start the server on `http://0.0.0.0:8000`.

4.  **Interact with the API:**
    You can now send queries to the `/query` endpoint. For example, using `curl`:

    ```bash
    curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d '{"query": "What is the capital of France?"}'
    ```

    Alternatively, you can access the interactive API documentation at `http://127.0.0.1:8000/docs` to try out the endpoint from your browser.