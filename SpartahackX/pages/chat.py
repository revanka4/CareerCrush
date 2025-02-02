import streamlit as st
from datetime import datetime
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key='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')

CONTEXT_DATA = """
Company Information:
Name: EcoTech Solutions
Industry: Renewable Energy & Sustainable Technology
Headquarters: Austin, Texas, USA
Regional Offices: San Francisco, Boston, and Denver
Founded: 2015
Company Size: 750 employees

About Us:
EcoTech Solutions is a leading innovator in renewable energy technologies and sustainable solutions. We specialize in developing and implementing solar power systems, energy storage solutions, and smart grid technologies for residential and commercial applications.

Mission Statement:
"To accelerate the world's transition to sustainable energy through innovative technology and accessible solutions."

Core Values:
1. Environmental Stewardship: We prioritize the planet in every decision we make
2. Innovation: We constantly push boundaries to create better solutions
3. Accessibility: We make sustainable technology available to everyone
4. Integrity: We operate with transparency and honesty in all our dealings
5. Community Impact: We believe in creating positive change in our communities

Key Products & Services:
- SolarFlex™: Advanced solar panel systems
- PowerVault™: Home energy storage solutions
- GridSmart™: Intelligent energy management systems
- GreenConsult: Sustainability consulting services

Company Culture:
- Flexible work arrangements with hybrid options
- Strong emphasis on professional development
- Regular team building and wellness activities
- Commitment to diversity and inclusion
- Green office practices and zero-waste initiatives

Recent Achievements:
- Named "Most Innovative Clean Tech Company 2023" by GreenTech Magazine
- Reduced carbon emissions by 1.5M tons through customer installations
- Achieved carbon-neutral operations in 2022
- Launched groundbreaking energy storage technology
"""

# Initialize session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": f"You are a helpful customer service assistant for our company. Use this information to answer questions: {CONTEXT_DATA}",
            "timestamp": datetime.now()
        }
    ]

# Function to add a message to the session state
def add_message(role, content):
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now()
    })

# Function to get OpenAI response
def get_bot_response(user_input):
    # Create a messages list without timestamps for the API
    api_messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.messages
    ]
    # Add the current user input
    api_messages.append({"role": "user", "content": user_input})
    
    # Send the request to OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=api_messages,
        max_tokens=150
    )
    return response.choices[0].message.content

# Streamlit app layout
st.title("Company Chat Assistant")

# Display existing messages (skip the system message)
for message in [m for m in st.session_state.messages if m["role"] != "system"]:
    with st.chat_message(message["role"]):
        st.write(f"{message['content']}")
        st.caption(f"{message['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")

# Input for new message
user_input = st.chat_input("Type a message...")

if user_input:
    # Add user message to the session state
    add_message("user", user_input)
    
    # Get and add bot response
    bot_response = get_bot_response(user_input)
    add_message("assistant", bot_response)
    
    # Rerun the app to display the new messages
    st.rerun()
