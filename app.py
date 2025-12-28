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
            st.markdown(
                '<div class="mini-stats"><span class="dot dot--cyan"></span><span class="mini-stats__text">Neon UI • Glassmorphism</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="glass card">', unsafe_allow_html=True)
        st.markdown('<div class="card__title">Output</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card__hint">Responses appear here. HTML rendering is enabled for rich formatting.</div>',
            unsafe_allow_html=True,
        )

        # Keep results across reruns (layout-only enhancement; logic intact)
        if "final_response" not in st.session_state:
            st.session_state.final_response = ""

        if get_answer_clicked:
            if query:
                with st.spinner("Synthesizing evidence-based insights..."):
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)

                    response_events = loop.run_until_complete(runner.run_debug(query))
                    final_response = get_final_text_response(response_events)

                    st.session_state.final_response = final_response
            else:
                st.warning("Please enter a question.")

        if st.session_state.final_response:
            st.markdown(
                f'<div class="response">{st.session_state.final_response}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '''
                <div class="response response--empty">
                  <div class="response__icon">⌁</div>
                  <div class="response__text">No output yet. Ask a question to begin.</div>
                </div>
                ''',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    futuristic_ui()
