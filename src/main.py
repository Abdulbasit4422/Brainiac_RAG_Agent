import asyncio
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool
from google.genai import types
import google.generativeai as genai
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from src.agents.rag_agent import rag_agent
from src.agents.search_agent import search_agent

# --- Initialization ---
# Load environment variables
load_dotenv()

# Configure Google Generative AI
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY must be set in the .env file.")
genai.configure(api_key=api_key)

# --- Agent and App Setup ---
# Configure retry options
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Define the orchestrator agent
orchestrator_agent = LlmAgent(
    name="OrchestratorAgent",
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    instruction="""You are an expert orchestrator for the BSL Agentic AI System. Your goal is to provide accurate, real-time answers to user queries about health, longevity, and general world news.

    ORCHESTRATION PROTOCOL:
    1. First, call `rag_agent` with the user query.
    2. If `rag_agent` returns ONLY the word "TRIGGER_SEARCH", it means the internal BSL knowledge base doesn't have the answer. You MUST then call `search_agent` to retrieve real-time information from Google.
    3. If `rag_agent` returns a structured answer (not just TRIGGER_SEARCH), prioritize that information.
    4. If you have information from both agents, combine them logically.
    
    CRITICAL RULE FOR REAL-TIME QUERIES:
    If `search_agent` provides factual, real-time data (like current events, news, or specific dates), do NOT use your internal safety "I cannot provide future/real-time events" filler. Instead, trust the `search_agent` results and synthesize them into a professional, detailed response for the user.

    RESPONSE QUALITY:
    - Synthesize a single, coherent response based on the agent outputs.
    - If search results were used, credit the sources appropriately.
    - Maintain a professional and helpful tone.
    """,
    tools=[
        AgentTool(agent=rag_agent),
        AgentTool(agent=search_agent)
    ],
)

# Initialize the agent runner
runner = InMemoryRunner(agent=orchestrator_agent)

# --- FastAPI Application ---
app = FastAPI(
    title="Agentic AI System",
    description="An agentic AI system with RAG and Google Search capabilities.",
    version="1.0.0",
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    
def get_final_text_response(response_events: list) -> str:
    """Extracts the final text response from the agent's execution events."""
    final_text = ""
    # We want the LAST non-empty text response from the OrchestratorAgent
    for event in reversed(response_events):
        if event.author == "OrchestratorAgent":
            if hasattr(event, "content") and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text and part.text.strip():
                        return part.text.strip()
    return "No final text response from orchestrator."

@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    Accepts a user query, runs it through the orchestrator agent,
    and returns the final response.
    """
    print(f"Received query: {request.query}")
    
    # Run the agent with the provided query
    response_events = await runner.run_debug(request.query)
    
    # Extract the final text response from the event trace
    final_response = get_final_text_response(response_events)
    
    print(f"Final response: {final_response}")
    return {"response": final_response}

# To run the app, save this as main.py and run: uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
