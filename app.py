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

    # --- Two-column layout: input (left) + output (right) ---
    left, right = st.columns([1, 1.25], gap="large")

    with left:
        st.markdown('<div class="glass card">', unsafe_allow_html=True)
        st.markdown('<div class="card__title">Query Console</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card__hint">Ask a question and I’ll synthesize an evidence-based answer.</div>',
            unsafe_allow_html=True,
        )

        query = st.text_input("Ask your question:", "")

        cols = st.columns([1, 1])
        with cols[0]:
            get_answer_clicked = st.button("Get Answer")
        with cols[1]:
            # Add a clear button to reset history
            if st.button("Reset Conversation"):
                st.session_state.chat_history = []
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="glass card">', unsafe_allow_html=True)
        st.markdown('<div class="card__title">Conversation History</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card__hint">Your full session history is preserved below. Scroll to review past insights.</div>',
            unsafe_allow_html=True,
        )

        # Initialize chat history if it doesn't exist
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if get_answer_clicked:
            if query:
                with st.spinner("Synthesizing evidence-based insights..."):
                    try:
                        # Use a cleaner way to run the async code in Streamlit
                        async def run_agent():
                            return await runner.run_debug(query)
                        
                        # run_until_complete can be brittle in Streamlit, 
                        # but if we are in a script, we can try to get the current loop
                        try:
                            loop = asyncio.get_running_loop()
                            # If a loop is already running (like in Streamlit), we might need to 
                            # use a different approach or run it in a thread if it's blocking.
                            # However, for Google GenAI, usually creating a new task works.
                            response_events = asyncio.run_coroutine_threadsafe(run_agent(), loop).result()
                        except RuntimeError:
                            # No loop running, use asyncio.run
                            response_events = asyncio.run(run_agent())

                        final_response = get_final_text_response(response_events)

                        # Store newest at bottom for natural chat flow
                        st.session_state.chat_history.append({"question": query, "answer": final_response})
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a question.")

        # Render all interactions
        if st.session_state.chat_history:
            # Wrap the entire history in our scrollable container
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
                  <div class="response__text">No interactions yet. Ask a question to begin.</div>
                </div>
                ''',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    futuristic_ui()
