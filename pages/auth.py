# import streamlit as st
# from database import get_user_by_username, create_user
# from werkzeug.security import check_password_hash

# def show_login_page():
#     st.markdown("<div class='section-header'>Login</div>", unsafe_allow_html=True)
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         user = get_user_by_username(username)
#         if user and check_password_hash(user['password_hash'], password):
#             st.session_state['logged_in'] = True
#             st.session_state['user_role'] = user['role']
#             st.session_state['username'] = username # Store username in session
#             st.success(f"Logged in as {username} ({user['role']})")
#             # Redirect to main app after login (using rerun to refresh state)
#             st.rerun()
#         else:
#             st.error("Login failed. Invalid username or password.")

# def show_logout_page():
#     if st.button("Logout"):
#         st.session_state['logged_in'] = False
#         st.session_state['user_role'] = None
#         st.session_state['username'] = None
#         st.success("Logged out successfully.")
#         st.rerun() # Refresh to reflect logout


# def show_signup_page():
#     st.markdown("<div class='section-header'>Sign Up</div>", unsafe_allow_html=True)
#     new_username = st.text_input("New Username")
#     new_password = st.text_input("New Password", type="password")
#     confirm_password = st.text_input("Confirm Password", type="password")

#     if st.button("Sign Up"):
#         if new_password == confirm_password:
#             if create_user(new_username, new_password):
#                 st.success("Signup successful! Please login.")
#             else:
#                 st.error("Username already taken. Please choose another.")
#         else:
#             st.error("Passwords do not match.")


# def show_auth_page():
#     auth_choice = st.radio("Choose Action", ["Login", "Sign Up"])
#     if auth_choice == "Login":
#         show_login_page()
#     elif auth_choice == "Sign Up":
#         show_signup_page()

# if __name__ == '__main__':
#     show_auth_page() # For testing auth pages directly
import pickle
from pathlib import Path

import streamlit_authenticator as Stauth

names=['admin','user']
usernames=['admin','user']
passwords=["abc123","123abc"] 

hashed_passwords=Stauth.Hasher(passwords).generate()

file_path=Path(__file__).parent/"hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords,file)

