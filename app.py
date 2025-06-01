# chatbot_app.py

import streamlit as st
import requests
import urllib3

# Config
RGT_API_URL =  # Replace with your actual API URL
RGT_API_KEY =  # Replace with your actual API key

# Page config
st.set_page_config(page_title="Simple Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Simple Chatbot")
st.markdown("Ask your question below:")

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def call_rgt_llm(prompt: str) -> str:
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1000,
    }
    headers = {
        "Authorization": f"Bearer {RGT_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(RGT_API_URL, json=payload, headers=headers, verify=False, timeout=30)
        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "No content returned.")
    except Exception as e:
        return f"⚠️ Error: {e}"

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Type your message here...")
    submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        bot_response = call_rgt_llm(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", bot_response))

# Display history
for sender, msg in st.session_state.chat_history:
    with st.chat_message("assistant" if sender == "Bot" else "user"):
        st.markdown(f"**{sender}:** {msg}")
