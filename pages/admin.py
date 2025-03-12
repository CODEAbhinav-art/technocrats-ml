import streamlit as st
import pandas as pd
from database import get_properties, get_property, add_property, update_property, delete_property
import os # For file operations

# Ensure 'property_images' directory exists
PROPERTY_IMAGES_DIR = 'property_images'
if not os.path.exists(PROPERTY_IMAGES_DIR):
    os.makedirs(PROPERTY_IMAGES_DIR)

def show_page():
    st.markdown("<div class='section-header'>Admin Panel - Manage Properties</div>", unsafe_allow_html=True)

    properties_df = get_properties()

    # Display Properties Table
    st.subheader("Current Listings")
    st.dataframe(properties_df, use_container_width=True)

    # Add New Property Form
    st.subheader("Add New Property")
    with st.form("add_property_form", clear_on_submit=True):
        property_name = st.text_input("Property Name")
        property_type = st.selectbox("Property Type", ["Apartment", "PG", "1BHK", "Studio", "Hostel", "Other"], index=0)
        location = st.selectbox("Location", ["Vadodara", "Mumbai", "Ahmedabad", "Other"]) # Example locations
        latitude = st.number_input("Latitude", format="%.6f") # Latitude input
        longitude = st.number_input("Longitude", format="%.6f") # Longitude input
        rent = st.number_input("Rent (INR)", min_value=1000)
        duration = st.text_input("Duration (e.g., 1 Month, 3 Months)")
        owner_contact = st.text_input("Owner Contact (Email)")
        uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg']) # Image upload
        submit_button = st.form_submit_button("Add Property")

        if submit_button:
            if property_name and location and rent and duration and owner_contact and uploaded_file:
                image_filename = save_uploaded_image(uploaded_file) # Save image and get filename
                if image_filename:
                    add_property(property_name, property_type, location, latitude, longitude, rent, duration, owner_contact, image_filename)
                    st.success("Property added successfully!")
                    st.rerun() # Refresh
                else:
                    st.error("Error saving image.") # Handle image save error
            else:
                st.error("Please fill in all required fields and upload an image.") # Image upload is now required

    # Edit and Delete Functionality
    st.subheader("Edit/Delete Properties")
    for index, property_data in properties_df.iterrows():
        with st.expander(f"Edit/Delete: {property_data['property_name']}", expanded=False):
            with st.form(f"edit_property_form_{property_data['id']}"):
                property_name = st.text_input("Property Name", value=property_data['property_name'])
                property_type = st.selectbox("Property Type", ["Apartment", "PG", "1BHK", "Studio", "Hostel", "Other"], index=["Apartment", "PG", "1BHK", "Studio", "Hostel", "Other"].index(property_data['property_type']))
                location = st.selectbox("Location", ["Vadodara", "Mumbai", "Ahmedabad", "Other"], index=["Vadodara", "Mumbai", "Ahmedabad", "Other"].index(property_data['location']))
                latitude = st.number_input("Latitude", value=property_data['latitude'], format="%.6f") # Latitude input
                longitude = st.number_input("Longitude", value=property_data['longitude'], format="%.6f") # Longitude input
                rent = st.number_input("Rent (INR)", min_value=1000, value=property_data['rent'])
                duration = st.text_input("Duration", value=property_data['duration'])
                owner_contact = st.text_input("Owner Contact (Email)", value=property_data['owner_contact'])
                uploaded_file_edit = st.file_uploader("Upload New Image (Optional)", type=['png', 'jpg', 'jpeg'], key=f"file_uploader_{property_data['id']}") # Unique key
                update_button = st.form_submit_button("Update Property")
                delete_button = st.form_submit_button("Delete Property")

                if update_button:
                    updated_image_filename = property_data['image_filename'] # Default to existing image
                    if uploaded_file_edit:
                        updated_image_filename = save_uploaded_image(uploaded_file_edit) # Save new image if uploaded
                        if not updated_image_filename:
                            st.error("Error saving new image.")
                            continue # Skip update if image save fails
                    update_property(property_data['id'], property_name, property_type, location, latitude, longitude, rent, duration, owner_contact, updated_image_filename)
                    st.success("Property updated successfully!")
                    st.rerun() # Refresh
                if delete_button:
                    delete_property(property_data['id'])
                    # Optionally delete image file from filesystem here if needed
                    st.success("Property deleted successfully!")
                    st.rerun() # Refresh


def save_uploaded_image(uploaded_file):
    try:
        file_extension = os.path.splitext(uploaded_file.name)[1]
        filename = f"{PROPERTY_IMAGES_DIR}/property_image_{st.session_state['username']}_{st.session_state.get('image_counter', 0)}{file_extension}" # Unique filename - user and counter based
        st.session_state['image_counter'] = st.session_state.get('image_counter', 0) + 1 # Increment counter in session state
        with open(filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return filename # Return the saved filename (path)
    except Exception as e:
        st.error(f"Error saving image: {e}")
        return None
    finally:
        if 'image_counter' in st.session_state and st.session_state['image_counter'] > 1000: # Reset counter after a limit to avoid very large numbers
            st.session_state['image_counter'] = 0 # Reset after some limit


if __name__ == '__main__':
    show_page()
