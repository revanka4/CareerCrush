import streamlit as st

def main():
    st.set_page_config(layout="wide")
    
    # Custom CSS to make chat input smaller and style the cards
    st.markdown(
        """
        <style>
            div[data-baseweb="base-input"] > div {
                max-width: 400px !important;
                margin: auto;
            }
            .card {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                margin: 10px 0;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .card:hover {
                background-color: #f1f1f1;
            }
            .card.selected {
                background-color: #0084ff;
                color: white;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Sidebar navigation with chat list
    with st.sidebar:
        st.title("Chats")
        chat_names = ["Chat 1", "Chat 2", "Chat 3", "New Chat"]
        
        # Initialize selected chat in session state
        if "selected_chat" not in st.session_state:
            st.session_state.selected_chat = chat_names[0]
        
        # Display chat names as cards
        for chat in chat_names:
            if st.session_state.selected_chat == chat:
                st.markdown(f'<div class="card selected">{chat}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="card">{chat}</div>', unsafe_allow_html=True)
    
    st.title(f"{st.session_state.selected_chat}")
    
    # Initialize chat history per chat
    if "chats" not in st.session_state:
        st.session_state.chats = {name: [] for name in chat_names[:-1]}
    
    if st.session_state.selected_chat not in st.session_state.chats:
        st.session_state.chats[st.session_state.selected_chat] = []
    
    # Display chat history
    for message in st.session_state.chats[st.session_state.selected_chat]:
        alignment = "flex-start" if message["role"] == "assistant" else "flex-end"
        bubble_color = "#f1f0f0" if message["role"] == "assistant" else "#0084ff"
        text_color = "black" if message["role"] == "assistant" else "white"
        profile_pic = "👨‍💻" if message["role"] == "user" else "🤖"
        
        st.markdown(
            f"""
            <div style='display: flex; align-items: center; justify-content: {alignment}; margin: 5px 0;'>
                {profile_pic if message["role"] == "assistant" else ""}
                <div style='background-color: {bubble_color}; color: {text_color}; padding: 10px; border-radius: 15px; max-width: 70%; margin: 0 10px;'>
                    {message['content']}
                </div>
                {profile_pic if message["role"] == "user" else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # User input
    user_input = st.chat_input("Type your message...")
    if user_input:
        # Append user message
        st.session_state.chats[st.session_state.selected_chat].append({"role": "user", "content": user_input})
        
        # Display user message
        st.markdown(
            f"""
            <div style='display: flex; align-items: center; justify-content: flex-end; margin: 5px 0;'>
                <div style='background-color: #0084ff; color: white; padding: 10px; border-radius: 15px; max-width: 70%; margin: 0 10px;'>
                    {user_input}
                </div>
                👨‍💻
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Generate response (static for now, can be AI-powered)
        response = f"You said: {user_input}"  # Replace with AI-generated response
        
        # Append bot response
        st.session_state.chats[st.session_state.selected_chat].append({"role": "assistant", "content": response})
        
        # Display bot response
        st.markdown(
            f"""
            <div style='display: flex; align-items: center; justify-content: flex-start; margin: 5px 0;'>
                🤖
                <div style='background-color: #f1f0f0; color: black; padding: 10px; border-radius: 15px; max-width: 70%; margin: 0 10px;'>
                    {response}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

if __name__ == "__main__":
    main()