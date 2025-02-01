import streamlit as st
from datetime import datetime

# Initialize session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to add a message to the session state
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content, "timestamp": datetime.now()})

# Streamlit app layout
st.title("Simple Messaging App")

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(f"{message['content']}")
        st.caption(f"{message['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")

# Input for new message
user_input = st.chat_input("Type a message...")

if user_input:
    # Add user message to the session state
    add_message("user", user_input)
    
    # Simulate a bot response (you can replace this with an actual bot logic)
    bot_response = f"Echo: {user_input}"
    add_message("bot", bot_response)
    
    # Rerun the app to display the new messages
    st.rerun()  # Use st.rerun() instead of st.experimental_rerun()