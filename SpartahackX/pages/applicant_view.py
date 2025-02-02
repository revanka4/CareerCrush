import streamlit as st
import pandas as pd
import json

# Load profiles from the JSON file
def get_profiles():
    # Open the JSON file and load it
    with open("positions.json", "r") as f:
        data = json.load(f)
    
    # Convert the loaded JSON into a list of dictionaries
    profiles = []
    for idx in range(len(data["Job Title"])):
        profile = {
            "name": f"Profile {idx + 1}",
            "job_title": data["Job Title"][str(idx)],
            "industry": data["Industry"][str(idx)],
            "company_name": data["Company Name"][str(idx)],
            "employment_type": data["Employment Type"][str(idx)],
            "tags": data["Tags"][str(idx)],
            # Use a default image or define how to load an image for each profile
            "image": '/path/to/your/image.jpg',  # You can update this later if you want dynamic image paths,
            "tools": data["Languages/Programs Used"][str(idx)],
            "description": data["Job Description"][str(idx)],
        }
        profiles.append(profile)
    
    return profiles

def main():
    st.title("Career Crush 🌟")
    st.text("Time to crush your career 🚀")

    # Sidebar Navigation
    st.sidebar.title("Navigation 🧭")
    page = st.sidebar.radio("Go to", ["Swipe Profiles", "View Matches"])
    
    if "index" not in st.session_state:
        st.session_state.index = 0
        st.session_state.liked = []
        st.session_state.disliked = []
    
    profiles = get_profiles()

    # Custom CSS for card style and button size adjustments
    st.markdown("""
    <style>
        .card {
            border: 1px solid #ccc;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            font-size: 18px;  /* Larger text for better readability */
        }
        .card img {
            border-radius: 12px;
            max-width: 100%;
        }
        .card-header {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .card-body {
            font-size: 1.2em;
            color: #333;
        }
        .card-actions {
            margin-top: 15px;
            display: flex;
            justify-content: space-between;
        }
        .card-actions button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 15px;
            margin: 10px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1.2em; /* Larger button text */
            width: 45%; /* Ensure even spacing for the buttons */
        }
        .card-actions button:hover {
            background-color: #45a049;
        }
        .card-actions button:focus {
            outline: none;
        }
        .sidebar .sidebar-content {
            font-size: 1.2em;
        }
    </style>
    """, unsafe_allow_html=True)

    if page == "Swipe Profiles":
        if st.session_state.index < len(profiles):
            profile = profiles[st.session_state.index]
            
            # Create profile card with emojis
            st.markdown(f"""
            <div class="card">
                <div class="card-header">
                    {profile['job_title']} - ({profile['employment_type']}) 💼
                </div>
                <div class="card-body">
                    <strong>🏢 Company:</strong> {profile['company_name']}
                    <br><br>
                    <strong>🌍 Industry:</strong> {profile['industry']}
                    <br><br>
                    <strong>🏷️ Tags:</strong> {', '.join(profile['tags'])}
                    <br><br>
                    <strong>🛠️ Tools:</strong> {', '.join(profile['tools'])}
                    <br><br>
                    <strong>📝 Description:</strong> {''.join(profile['description'])}
                </div>
 
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("❤️ Like", use_container_width=True):
                    st.session_state.liked.append(profile)
                    st.session_state.index += 1
                    st.rerun()
            
            with col2:
                if st.button("❌ Dislike", use_container_width=True):
                    st.session_state.disliked.append(profile)
                    st.session_state.index += 1
                    st.rerun()

        else:
            st.write("No more profiles to show! 😢")
    
    elif page == "View Matches":
        st.write("### Liked Profiles ❤️:")
        if st.session_state.liked:
            for p in st.session_state.liked:
                st.write(f"- {p['name']}, {p['job_title']} 💼")
        else:
            st.write("No liked profiles yet.")
        
        st.write("### Disliked Profiles ❌:")
        if st.session_state.disliked:
            for p in st.session_state.disliked:
                st.write(f"- {p['name']}, {p['job_title']} 💼")
        else:
            st.write("No disliked profiles yet.")

if __name__ == "__main__":
    main()
