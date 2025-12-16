import streamlit as st
import asyncio
from dotenv import load_dotenv # Import load_dotenv
from src.main import orchestrator_agent, runner, get_final_text_response

load_dotenv() # Call load_dotenv()


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def futuristic_ui():
    st.set_page_config(page_title="BSL Agentic AI", page_icon="✨", layout="wide")
    load_css("style.css")

    st.title("BSL Agentic AI Assistant")
    st.write("Your expert consultant for BSL services.")

    query = st.text_input("Ask your question:", "")

    if st.button("Get Answer"):
        if query:
            with st.spinner("Finding the best answer for you..."):
                response_events = asyncio.run(runner.run_debug(query))
                final_response = get_final_text_response(response_events)
                st.markdown(final_response, unsafe_allow_html=True)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    futuristic_ui()
