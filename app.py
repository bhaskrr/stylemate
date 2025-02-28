__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from core import main
import streamlit as st
import time

st.set_page_config(page_title="StyleMate: Your AI Fashion Assistant", layout="wide")

st.title("StyleMate: Your AI Fashion Assistant")
st.subheader("Get AI-powered fashion advice and outfit recommendations!")


def respond(query):
    # AI Response with Typing Effect
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = main(query)

        with st.spinner("Thinking..."):
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)


# Quick prompts
quick_prompts = [
    "Suggest me a funky outfit for a house party.",
    "Give me some outfit ideas for office.",
    "What type of accessories should i wear for a wedding?",
]
st.markdown("**Quick Prompts:**")

for prompt in quick_prompts:
    st.markdown(f"- {prompt}")


# Chat Input
if query := st.chat_input("Your fashion query..."):
    with st.chat_message("user", avatar="👤"):
        st.markdown(query)
    respond(query)
