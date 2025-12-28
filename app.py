import streamlit as st
import asyncio
from dotenv import load_dotenv # Import load_dotenv
import os

load_dotenv() # Call load_dotenv()

from src.main import orchestrator_agent, runner, get_final_text_response


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def futuristic_ui():
    st.set_page_config(page_title="Brainiac Agentic AI", page_icon="✨", layout="wide")
    load_css("style.css")

    st.title("Brainiac Agentic AI Assistant")
    st.write("I am a expert in Healthspan and Vitality Medicine")

    query = st.text_input("Ask your question:", "")

    if st.button("Get Answer"):
        if query:
            with st.spinner("Synthesizing evidence-based insights..."):
                try:
                 loop = asyncio.get_event_loop()
                except RuntimeError:
                 loop = asyncio.new_event_loop()
                 asyncio.set_event_loop(loop)

                response_events = loop.run_until_complete(runner.run_debug(query))

                final_response = get_final_text_response(response_events)
                st.markdown(final_response, unsafe_allow_html=True)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    futuristic_ui()
