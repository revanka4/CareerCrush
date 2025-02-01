# import streamlit as st
# import pandas as pd
# import json
# a = [1,2,3]

# # Load profiles from the JSON file
# def get_profiles():
#     # Open the JSON file and load it
#     with open("positions.json", "r") as f:
#         data = json.load(f)
    
#     # Convert the loaded JSON into a list of dictionaries
#     profiles = []
#     for idx in range(len(data["Job Title"])):
#         profile = {
#             "name": f"Profile {idx + 1}",
#             "job_title": data["Job Title"][str(idx)],
#             "industry": data["Industry"][str(idx)],
#             "company_name": data["Company Name"][str(idx)],
#             "employment_type": data["Employment Type"][str(idx)],
#             "tags": data["Tags"][str(idx)],
#             # Use a default image or define how to load an image for each profile
#             "image": '/path/to/your/image.jpg',  # You can update this later if you want dynamic image paths,
#             "tools": data["Languages/Programs Used"][str(idx)],
#             "description": data["Job Description"][str(idx)],
#         }
#         profiles.append(profile)
    
#     return profiles

# def main():
#     st.title("Career Crush")
#     st.text("Time to crush your career")

#     # Sidebar Navigation
#     st.sidebar.title("Navigation")
#     page = st.sidebar.radio("Go to", ["Swipe Profiles", "View Matches"])
    
#     if "index" not in st.session_state:
#         st.session_state.index = 0
#         st.session_state.liked = []
#         st.session_state.disliked = []
    
#     profiles = get_profiles()

#     # Custom CSS for card style
#     st.markdown("""
#     <style>
#         .card {
#             border: 1px solid #ccc;
#             border-radius: 10px;
#             padding: 20px;
#             margin-bottom: 10px;
#             box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#         }
#         .card img {
#             border-radius: 10px;
#             max-width: 100%;
#         }
#         .card-header {
#             font-size: 1.2em;
#             font-weight: bold;
#             margin-bottom: 10px;
#         }
#         .card-body {
#             font-size: 1em;
#             color: #333;
#         }
#         .card-actions {
#             margin-top: 10px;
#         }
#         .card-actions button {
#             background-color: #4CAF50;
#             color: white;
#             border: none;
#             padding: 10px;
#             margin: 5px;
#             border-radius: 5px;
#             cursor: pointer;
#         }
#         .card-actions button:hover {
#             background-color: #45a049;
#         }
#     </style>
#     """, unsafe_allow_html=True)

#     if page == "Swipe Profiles":
#         if st.session_state.index < len(profiles):
#             profile = profiles[st.session_state.index]
            
#             # Create profile card
#             st.markdown(f"""
#             <div class="card">
#                 <div class="card-header">
#                     {profile['job_title']} - ({profile['employment_type']})
#                 </div>
#                 <div class="card-body">
#                     {profile['company_name']}
#                     <br><br>
#                     Industry: {profile['industry']} 
#                     <br><br>
#                     Tags: {', '.join(profile['tags'])}
#                     <br><br>
#                     Tools: {', '.join(profile['tools'])}
#                     <br><br>
#                     Description: {''.join(profile['description'])}
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button("❤️ Like"):
#                     st.session_state.liked.append(profile)
#                     st.session_state.index += 1
#                     st.rerun()
            
#             with col2:
#                 if st.button("❌ Dislike"):
#                     st.session_state.disliked.append(profile)
#                     st.session_state.index += 1
#                     st.rerun()

#         else:
#             st.write("No more profiles to show!")
    
#     elif page == "View Matches":
#         st.write("### Liked Profiles:")
#         if st.session_state.liked:
#             for p in st.session_state.liked:
#                 #st.image(p["image"], width=100)
#                 st.write(f"- {p['name']}, {p['job_title']}")
#         else:
#             st.write("No liked profiles yet.")
        
#         st.write("### Disliked Profiles:")
#         if st.session_state.disliked:
#             for p in st.session_state.disliked:
#                 #st.image(p["image"], width=100)
#                 st.write(f"- {p['name']}, {p['job_title']}")
#         else:
#             st.write("No disliked profiles yet.")

# if __name__ == "__main__":
#     main()


import streamlit as st
import json
import numpy as np
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
    
    recommended_indices = set()
    for idx in liked_indices:
        similar_profiles = np.argsort(similarity_matrix[idx])[::-1]
        for sp_idx in similar_profiles:
            if sp_idx not in liked_indices and sp_idx not in disliked_indices:
                recommended_indices.add(sp_idx)
    
    return [profiles[i] for i in recommended_indices if i < len(profiles)]

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
    
    profiles = get_profiles()
    similarity_matrix = compute_similarity(profiles)
    
    if not st.session_state.recommended and st.session_state.liked:
        st.session_state.recommended = get_recommended_profiles(profiles, similarity_matrix, st.session_state.liked, st.session_state.disliked)

    st.markdown("""
    <style>
        .card {
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
    </style>
    """, unsafe_allow_html=True)
    
    if page == "Swipe Profiles":
        if st.session_state.index < len(profiles):
            profile = profiles[st.session_state.index]
        elif st.session_state.recommended:
            profile = st.session_state.recommended.pop(0)
        else:
            profile = None
        
        if profile:
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
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("❤️ Like", key=f"like_{profile['name']}"):
                    st.session_state.liked.append(profile)
                    st.session_state.index += 1
                    st.session_state.recommended = get_recommended_profiles(profiles, similarity_matrix, st.session_state.liked, st.session_state.disliked)
                    st.rerun()
            
            with col2:
                if st.button("❌ Dislike", key=f"dislike_{profile['name']}"):
                    st.session_state.disliked.append(profile)
                    st.session_state.index += 1
                    st.rerun()
        else:
            st.write("No more profiles to show!")
    
    elif page == "View Matches":
        st.write("### Liked Profiles:")
        if st.session_state.liked:
            for p in st.session_state.liked:
                if st.button(p['job_category'], key=f"liked_{p['name']}"):
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-header">
                            {p['name']} - {p['job_category']}
                        </div>
                        <div class="card-body">
                            Location: {p['location']}<br><br>
                            Years of Experience: {p['years_of_experience']}<br><br>
                            Education: {p['education']}<br><br>
                            Experience: {p['experience']}<br><br>
                            Skills: {', '.join(p['skills'])}<br><br>
                            LinkedIn: <a href="{p['linkedin']}" target="_blank">{p['linkedin']}</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.write("No liked profiles yet.")
        
        st.write("### Disliked Profiles:")
        if st.session_state.disliked:
            for p in st.session_state.disliked:
                if st.button(p['name'], key=f"disliked_{p['name']}"):
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-header">
                            {p['name']} - {p['job_category']}
                        </div>
                        <div class="card-body">
                            Location: {p['location']}<br><br>
                            Years of Experience: {p['years_of_experience']}<br><br>
                            Education: {p['education']}<br><br>
                            Experience: {p['experience']}<br><br>
                            Skills: {', '.join(p['skills'])}<br><br>
                            LinkedIn: <a href="{p['linkedin']}" target="_blank">{p['linkedin']}</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.write("No disliked profiles yet.")

if __name__ == "__main__":
    main()
