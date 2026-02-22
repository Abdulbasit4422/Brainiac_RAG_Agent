import streamlit as st
import asyncio
from dotenv import load_dotenv  # Import load_dotenv
import os

load_dotenv()  # Call load_dotenv()

from src.main import orchestrator_agent, runner, get_final_text_response


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def futuristic_ui():
    st.set_page_config(page_title="Brainiac Agentic AI", page_icon="✨", layout="wide")
    load_css("style.css")

    # --- Subtle background helpers (purely layout; logic unchanged) ---
    st.markdown(
        '''
        <div class="bg-grid"></div>
        <div class="bg-glow bg-glow--a"></div>
        <div class="bg-glow bg-glow--b"></div>
        ''',
        unsafe_allow_html=True,
    )

    # --- Hero / Header ---
    st.markdown(
        '''
        <div class="hero">
          <div class="hero__badge">✨ Brainiac • Agentic AI</div>
          <div class="hero__title">Brainiac Agentic AI Assistant</div>
          <div class="hero__subtitle">I am a expert in Healthspan and Vitality Medicine</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    # --- Main Chat Area ---
    # Wrap everything in a single layout rather than columns
    st.markdown('<div class="glass card">', unsafe_allow_html=True)
    st.markdown('<div class="card__title">Conversation History</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="card__hint">Your full session history is preserved below. Scroll to review past insights.</div>',
        unsafe_allow_html=True,
    )

    # Initialize chat history if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Render all interactions
    if st.session_state.chat_history:
        st.markdown('<div class="chat-history-container">', unsafe_allow_html=True)
        for chat in st.session_state.chat_history:
            st.markdown(
                f'<div class="chat-question"><b>Query:</b> {chat["question"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="response">{chat["answer"]}</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '''
            <div class="response response--empty">
              <div class="response__icon">⌁</div>
              <div class="response__text">No interactions yet. Ask a question at the bottom to begin your consultation.</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


    # --- Fixed Bottom Input Area ---
    # We use st.container with a markdown hack to apply the fixed styling
    st.markdown('<div class="fixed-bottom-container">', unsafe_allow_html=True)
    
    # Create columns for the input and buttons within the fixed container
    # Streamlit renders these inside the div if placed sequentially
    input_cols = st.columns([4, 1, 1], gap="small")
    
    with input_cols[0]:
        query = st.text_input("Ask your question:", "", key="query_input", label_visibility="collapsed", placeholder="Enter your query here...")
        
    with input_cols[1]:
        get_answer_clicked = st.button("Get Answer")
        
    with input_cols[2]:
        if st.button("Reset"):
            st.session_state.chat_history = []
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Processing Logic ---
    if get_answer_clicked:
        if query:
            with st.spinner("Synthesizing evidence-based insights..."):
                try:
                    async def run_agent():
                        return await runner.run_debug(query)
                    
                    try:
                        loop = asyncio.get_running_loop()
                        response_events = asyncio.run_coroutine_threadsafe(run_agent(), loop).result()
                    except RuntimeError:
                        response_events = asyncio.run(run_agent())

                    final_response = get_final_text_response(response_events)
                    st.session_state.chat_history.append({"question": query, "answer": final_response})
                    st.rerun() # Rerun to update the scrollable history above
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a question.")


if __name__ == "__main__":
    futuristic_ui()
