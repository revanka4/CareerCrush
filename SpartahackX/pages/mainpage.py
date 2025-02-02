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
    st.title("Career Crush")
    st.text("Time to crush your career!")

    # Sidebar Navigation
    st.sidebar.title("Career Home!")
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

    profiles = get_profiles()
    similarity_matrix = compute_similarity(profiles)

    if not st.session_state.recommended:
        st.session_state.recommended = get_recommended_profiles(
            profiles, similarity_matrix, st.session_state.liked, st.session_state.disliked
        )

    # Custom CSS for card style
    st.markdown("""
    <style>
        .card {
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .card img {
            border-radius: 10px;
            max-width: 100%;
        }
        .card-header {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .card-body {
            font-size: 1em;
            color: white;
        }
        .card-actions {
            margin-top: 10px;
        }
        .card-actions button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
        }
        .card-actions button:hover {
            background-color: #45a049;
        }
    </style>
    """, unsafe_allow_html=True)

    # Filters
    st.sidebar.title("Filters")
    job_category_filter = st.sidebar.selectbox("Job Category", ["All"] + list(set(p["job_category"] for p in profiles)))
    location_filter = st.sidebar.selectbox("Location", ["All"] + list(set(p["location"] for p in profiles)))
    experience_filter = st.sidebar.slider("Years of Experience", min_value=0, max_value=20, value=(0, 20))

    # Sort By
    sort_by = st.sidebar.selectbox("Sort By", ["Relevance", "Years of Experience", "Name"])

    # Filter and sort profiles
    filtered_profiles = [p for p in st.session_state.recommended if 
                         (job_category_filter == "All" or p["job_category"] == job_category_filter) and
                         (location_filter == "All" or p["location"] == location_filter) and
                         (experience_filter[0] <= p["years_of_experience"] <= experience_filter[1])]

    if sort_by == "Years of Experience":
        filtered_profiles.sort(key=lambda x: x["years_of_experience"], reverse=True)
    elif sort_by == "Name":
        filtered_profiles.sort(key=lambda x: x["name"])

    # Main Content
    if page == "Swipe Profiles":
        if filtered_profiles:
            profile = filtered_profiles[st.session_state.index]

            st.image(profile['image'])

            # Display profile card
            st.markdown(f"""
            <div class="card">
                <div class="card-header">
                    {profile['name']} - {profile['job_category']}
                </div>
                <div class="card-body">
                    Location: {profile['location']}
                    <br><br>
                    Years of Experience: {profile['years_of_experience']}
                    <br><br>
                    Education: {profile['education']}
                    <br><br>
                    Experience: {profile['experience']}
                    <br><br>
                    Skills: {', '.join(profile['skills'])}
                    <br><br>
                    LinkedIn: <a href="{profile['linkedin']}" target="_blank">{profile['linkedin']}</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("❤️ Like"):
                    st.session_state.liked.append(profile)
                    st.session_state.index += 1
                    st.session_state.recommended = get_recommended_profiles(
                        profiles, similarity_matrix, st.session_state.liked, st.session_state.disliked
                    )
                    st.rerun()
            with col2:
                if st.button("❌ Dislike"):
                    st.session_state.disliked.append(profile)
                    st.session_state.index += 1
                    st.session_state.recommended = get_recommended_profiles(
                        profiles, similarity_matrix, st.session_state.liked, st.session_state.disliked
                    )
                    st.rerun()

            # Feedback
            feedback = st.text_area("Why did you like/dislike this profile?")
            if st.button("Submit Feedback"):
                st.session_state.feedback[profile['name']] = feedback
                st.success("Thank you for your feedback!")
        else:
            st.write("No more profiles to show!")

    elif page == "View Matches":
        # Search bar for filtering liked profiles
        search_term = st.text_input("Search Liked Profiles")

        # Filter liked profiles based on search
        filtered_liked_profiles = [p for p in st.session_state.liked if search_term.lower() in p["name"].lower() or 
                                   any(search_term.lower() in skill.lower() for skill in p["skills"])]

        st.write("### Liked Profiles:")
        if filtered_liked_profiles:
            for p in filtered_liked_profiles:
                # Double-click to remove the profile
                if st.button(p["name"], key=f"liked_{p['name']}"):
                    if p['name'] in st.session_state.card_visibility:
                        st.session_state.card_visibility[p['name']] = not st.session_state.card_visibility[p['name']]
                    else:
                        st.session_state.card_visibility[p['name']] = True
                
                # Display the card if it's visible
                if st.session_state.card_visibility.get(p['name'], False):
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-header">
                            {p['name']} - {p['job_category']}
                        </div>
                        <div class="card-body">
                            Location: {p['location']}
                            <br><br>
                            Years of Experience: {p['years_of_experience']}
                            <br><br>
                            Education: {p['education']}
                            <br><br>
                            Experience: {p['experience']}
                            <br><br>
                            Skills: {', '.join(p['skills'])}
                            <br><br>
                            LinkedIn: <a href="{p['linkedin']}" target="_blank">{p['linkedin']}</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.write("No liked profiles match your search.")

        st.write("### Disliked Profiles:")
        if st.session_state.disliked:
            for p in st.session_state.disliked:
                st.markdown(f"""
                <div class="card">
                    <div class="card-header">
                        {p['name']} - {p['job_category']}
                    </div>
                    <div class="card-body">
                        Location: {p['location']}
                        <br><br>
                        Years of Experience: {p['years_of_experience']}
                        <br><br>
                        Skills: {', '.join(p['skills'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No disliked profiles yet.")

if __name__ == "__main__":
    main()
