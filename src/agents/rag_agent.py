import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from src.tools import pinecone_rag
from google.genai import types # For HttpRetryOptions

# Load environment variables from .env file
load_dotenv()

# Configure Retry Options (from the sample code)
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

def retrieve_from_pinecone(query: str) -> str:
    """
    Retrieves relevant information from the Pinecone knowledge base based on the query.
    If no relevant information is found, it returns 'TRIGGER_SEARCH'.
    """
    rag_results, _ = pinecone_rag.rag(query)

    if not rag_results or not rag_results.get('matches'):
        return "TRIGGER_SEARCH"

    # Combine context from top results (can be adjusted)
    context = ""
    for match in rag_results['matches']:
        if match.get('score', 0) > 0.7: # Only include results with a good score
            context += match['metadata']['text'] + "\n"
    
    final_context = context.strip()
    return final_context if final_context else "TRIGGER_SEARCH"


rag_agent = LlmAgent(
    name="rag_agent",
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    instruction="""You are a Retrieval-Augmented Generation agent specialized in BSL health and longevity services.
    
    CRITICAL PROTOCOL:
    1. Call the `retrieve_from_pinecone` tool first.
    2. If the tool returns "TRIGGER_SEARCH", you MUST respond ONLY with the exact word "TRIGGER_SEARCH". No conversational filler.
    3. If the tool returns actual context, use it to answer the query following this structure:
       - A. Summary Overview: High-level summary.
       - B. Detailed Explanation: Use Markdown headings.
       - C. Key Takeaways: Bulleted list.
       - D. Source Attribution: "Source: Internal BSL Knowledge Base."
    
    Do not speculate. If the information isn't in the context, signal TRIGGER_SEARCH.
    """,
    tools=[retrieve_from_pinecone],
)
