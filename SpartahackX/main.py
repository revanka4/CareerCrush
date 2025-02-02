import streamlit as st

# Add logo at the very top of the sidebar
st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Adds spacing if needed
st.sidebar.image("file-RRqigeTBQMsd77tFowkt5X.png", use_container_width=True)



# Hardcoded login credentials (for demonstration purposes)
LOGIN_CREDENTIALS = {
    "employer": {"username": "employer", "password": "employer123"},
    "employee": {"username": "employee", "password": "employee123"},
}

def login_screen():
    st.title("Career Crush Login")
    st.text("Please log in to continue.")

    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        if (username == LOGIN_CREDENTIALS["employer"]["username"] and
            password == LOGIN_CREDENTIALS["employer"]["password"]):
            st.success("Logged in as Employer!")
            st.switch_page("pages/mainpage.py")
        elif (username == LOGIN_CREDENTIALS["employee"]["username"] and
              password == LOGIN_CREDENTIALS["employee"]["password"]):
            st.success("Logged in as Employee!")
            st.switch_page("pages/mainpage.py")
        else:
            st.error("Invalid username or password.")

# Main function
def main():
    login_screen()

if __name__ == "__main__":
    main()
