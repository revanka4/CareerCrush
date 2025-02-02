import streamlit as st
import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load profiles from the JSON file
def get_profiles():
    with open("applicants.json", "r") as f:
        data = json.load(f)
    
    profiles = []
    for idx, applicant in data.items():
        profile = {
            "name": applicant["Name"],
            "job_category": applicant["Job Category"],
            "location": applicant["Location"],
            "years_of_experience": applicant["Years of Experience"],
            "education": applicant["Education"],
            "experience": applicant["Experience"],
            "skills": applicant["Skills"],
            "linkedin": applicant["LinkedIn"],
            "image": applicant["Image"]
        }
        profiles.append(profile)
    
    return profiles

def compute_similarity(profiles):
    skill_texts = [" ".join(profile["skills"]) for profile in profiles]
    vectorizer = TfidfVectorizer()
    skill_vectors = vectorizer.fit_transform(skill_texts)
    similarity_matrix = cosine_similarity(skill_vectors)
    return similarity_matrix

def get_recommended_profiles(profiles, similarity_matrix, liked_profiles, disliked_profiles):
    liked_indices = [profiles.index(p) for p in liked_profiles if p in profiles]
    disliked_indices = {profiles.index(p) for p in disliked_profiles if p in profiles}
    
    if not liked_indices:
        return [p for idx, p in enumerate(profiles) if idx not in disliked_indices]
    
    avg_similarity = np.mean(similarity_matrix[liked_indices], axis=0)
    
    for idx in disliked_indices:
        avg_similarity[idx] = -1
    
    recommended_indices = np.argsort(avg_similarity)[::-1]
    
    recommended_profiles = []
    for idx in recommended_indices:
        if idx not in liked_indices and idx not in disliked_indices and avg_similarity[idx] > 0:
            recommended_profiles.append(profiles[idx])
    
    return recommended_profiles

def main():
    st.title("🌟 Career Crush 🌟")
    st.text("Time to crush your career! Let's make some connections. 🚀")

    # Custom CSS for button and card styling
    st.markdown("""
    <style>
        .card {
            border: 2px solid #3498db;  /* Blue border for the card */
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            background-color: #f0f8ff;  /* Light background color */
        }
        .card img {
            border-radius: 15px;
            max-width: 100%;
        }
        .card-header {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        .card-body {
            font-size: 1.2em;
            color: #34495e;
        }
        .card-actions {
            margin-top: 15px;
        }
        .card-actions button {
            width: 100%;  /* Make button take full width of the column */
            padding: 20px;
            font-size: 22px;
            border-radius: 12px;
            color: white;
            border: none;
            cursor: pointer;
        }
        .like-button {
            background-color: #4CAF50; /* Green for Like */
        }
        .like-button:hover {
            background-color: #45a049;
        }
        .dislike-button {
            background-color: #f44336; /* Red for Dislike */
        }
        .dislike-button:hover {
            background-color: #e53935;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar Navigation
    st.sidebar.title("Career Home 🏠")
    page = st.sidebar.radio("Go to", ["Swipe Profiles", "View Matches"])

    # Initialize session state variables
    if "index" not in st.session_state:
        st.session_state.index = 0
        st.session_state.liked = []
        st.session_state.disliked = []
        st.session_state.recommended = []
        st.session_state.card_visibility = {}
        st.session_state.saved_profiles = []
        st.session_state.feedback = {}
        st.session_state.like_count = 0  # Track like button clicks

    profiles = get_profiles()
    similarity_matrix = compute_similarity(profiles)

    if not st.session_state.recommended:
        st.session_state.recommended = get_recommended_profiles(
            profiles, similarity_matrix, st.session_state.liked, st.session_state.disliked
        )

    # Trigger balloons on the 5th like
    if st.session_state.like_count == 5:
        st.success("It's a match! 🎉")
        st.balloons()  # Play balloons animation

    # Main Content
    if page == "Swipe Profiles":
        if filtered_profiles := [p for p in st.session_state.recommended if p not in st.session_state.liked + st.session_state.disliked]:
            profile = filtered_profiles[st.session_state.index]

            st.image(profile['image'])

            # Display profile card with emojis
            st.markdown(f"""
            <div class="card">
                <div class="card-header">
                    {profile['name']} - {profile['job_category']}
                </div>
                <div class="card-body">
                    <strong>📍 Location:</strong> {profile['location']}
                    <br><br>
                    <strong>💼 Years of Experience:</strong> {profile['years_of_experience']}
                    <br><br>
                    <strong>🎓 Education:</strong> {profile['education']}
                    <br><br>
                    <strong>📝 Experience:</strong> {profile['experience']}
                    <br><br>
                    <strong>🔧 Skills:</strong> {', '.join(profile['skills'])}
                    <br><br>
                    <strong>🔗 LinkedIn:</strong> <a href="{profile['linkedin']}" target="_blank">{profile['linkedin']}</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Action buttons with custom styles for larger size and spacing
            col1, col2 = st.columns(2)
            with col1:
                if st.button("❤️ Like", key="like_button", help="Like this profile", use_container_width=True):
                    st.session_state.liked.append(profile)
                    st.session_state.index += 1
                    st.session_state.like_count += 1  # Increment like count
                    st.session_state.recommended = get_recommended_profiles(
                        profiles, similarity_matrix, st.session_state.liked, st.session_state.disliked
                    )
                    st.rerun()

            with col2:
                if st.button("❌ Skip", key="dislike_button", help="Dislike this profile", use_container_width=True):
                    st.session_state.disliked.append(profile)
                    st.session_state.index += 1
                    st.session_state.recommended = get_recommended_profiles(
                        profiles, similarity_matrix, st.session_state.liked, st.session_state.disliked
                    )
                    st.rerun()

            # Feedback
            feedback = st.text_area("Why did you like/dislike this profile? 💬", height=100)
            if st.button("Submit Feedback"):
                st.session_state.feedback[profile['name']] = feedback
                st.success("Thank you for your feedback! 😊")
        else:
            st.write("No more profiles to show! 😢")

if __name__ == "__main__":
    main()
