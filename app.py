import streamlit as st
import pandas as pd
from pages import rentals, libraries, coaching_centers, chatbot, admin, auth # Import auth page module

st.set_page_config(
    page_title="Avishkar Rentals",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS (same as before - include in full app.py below)

# Initialize session state (for login status)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None


# Main App Content - Conditional on Login
def main():
    st.markdown("<div class='main-header'>Avishkar Rentals</div>", unsafe_allow_html=True)
    st.image("https://via.placeholder.com/800x200.png?text=Your+Rental+Banner", use_container_width=True, class_name="banner-image")

    if not st.session_state['logged_in']:
        auth.show_auth_page() # Show login/signup if not logged in
        return # Stop further execution if not logged in

    # Sidebar for Navigation (only shown after login)
    with st.sidebar:
        st.markdown(f"<h3 style='color: #007bff;'>Welcome, {st.session_state['username']}</h3>", unsafe_allow_html=True) # Welcome message
        auth.show_logout_page() # Logout button in sidebar
        st.markdown("<hr>") # Separator
        st.markdown("<h2 style='color: #007bff;'>Navigation</h2>", unsafe_allow_html=True)
        page = st.radio(
            "Choose a section",
            ['Rental Listings', 'Libraries', 'Coaching Centers', 'Chatbot', 'Leave a Review'], # Public pages
            index=0
        )
        if st.session_state['user_role'] == 'admin': # Show Admin Panel only for admin
            admin_page = st.radio("Admin Actions", ['Admin Panel']) # Admin options in a separate radio group - to keep main nav cleaner
        else:
            admin_page = None # No admin options for non-admins


    # Page Routing - Conditional on Page Selection
    if page == 'Rental Listings':
        rentals.show_page()
    elif page == 'Libraries':
        libraries.show_page()
    elif page == 'Coaching Centers':
        coaching_centers.show_page()
    elif page == 'Chatbot':
        chatbot.show_page()
    elif page == 'Leave a Review':
        show_review_section()
    elif admin_page == 'Admin Panel': # Admin page route
        if st.session_state['user_role'] == 'admin': # Double check role before showing admin page
            admin.show_page()
        else:
            st.error("You are not authorized to access the Admin Panel.")


def show_review_section(): # Same as before
    st.markdown("<div class='section-header'>Leave a Review</div>", unsafe_allow_html=True)
    review_text = st.text_area("Your Feedback", placeholder="Share your thoughts about our service or a property...")
    rating = st.slider("Rating (1-5 stars)", 1, 5, 3)
    if st.button("Submit Review", key="review_button"):
        # In a real app, store review & associate with property if possible
        st.success("Thank you for your review!")


if __name__ == '__main__':
    main()


# Full CSS (same as before - included for completeness)
st.markdown(
    """
    <style>
    /* General App Styling */
    .stApp {
        background-color: #f8f9fa; /* Light background */
        color: #343a40; /* Dark text */
        font-family: 'Arial', sans-serif;
    }

    /* Sidebar Styling */
    .stSidebar {
        background-color: #e9ecef; /* Lighter sidebar */
        padding: 20px;
        border-radius: 5px;
    }
    .stSidebar .st-expander header p {
        font-size: 1.2em;
        font-weight: bold;
        color: #007bff; /* Primary color for sidebar headers */
    }

    /* Main Content Area */
    .main-container {
        padding: 20px;
    }

    /* Header Styling */
    .main-header {
        font-size: 3.5em; /* Slightly reduced size */
        font-weight: bold;
        text-align: center;
        color: #0056b3; /* Darker primary color */
        margin-bottom: 15px;
        text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.1);
        font-family: 'Arial Black', sans-serif;
        animation: fadeIn 1s ease-out; /* Fade-in animation */
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Banner Image Styling */
    .banner-image {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        animation: slideIn 1.5s ease-out; /* Slide-in animation */
    }
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    /* Sections (like Available Listings, Book a Property) */
    .section-header {
        font-size: 2em;
        color: #28a745; /* Success color for section headers */
        margin-top: 25px;
        margin-bottom: 15px;
        border-bottom: 2px solid #28a745;
        padding-bottom: 5px;
        animation: underline 1.5s ease-out forwards; /* Underline animation */
    }
    @keyframes underline {
        0% { width: 0%; }
        100% { width: 100%; }
    }


    /* Form Element Styling (consistent with theme) */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>div,
    .stTextArea>div>div>textarea {
        background-color: #fff !important; /* White input background */
        border: 1px solid #ced4da !important; /* Light border */
        border-radius: 0.25rem !important;
        padding: 8px !important;
        margin-bottom: 10px !important;
    }
    .stButton>button {
        background-color: #007bff !important; /* Primary button color */
        color: white !important;
        border: none !important;
        border-radius: 0.25rem !important;
        padding: 10px 20px !important;
        transition: background-color 0.3s ease !important;
    }
    .stButton>button:hover {
        background-color: #0056b3 !important; /* Darker shade on hover */
    }

    /* Table Styling */
    .dataframe {
        background-color: #fff !important;
        border-radius: 0.5rem !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        animation: fadeInTable 2s ease-out; /* Fade-in animation for table */
    }
    @keyframes fadeInTable {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }

    /* Success Message Styling */
    .streamlit-success {
        color: #155724;
        background-color: #d4edda;
        border-color: #c3e6cb;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid transparent;
        border-radius: 0.25rem;
    }

    /* Responsive Adjustments (already in your original CSS, can be further enhanced) */
    @media (max-width: 768px) {
        .main-header { font-size: 2.5em; }
        .section-header { font-size: 1.7em; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)
