import streamlit as st
import pandas as pd
from database import get_properties, get_property, add_property, update_property, delete_property

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
        location = st.selectbox("Location", ["Vadodara", "Mumbai", "Ahmedabad", "Other"]) # Example locations
        rent = st.number_input("Rent (INR)", min_value=1000)
        duration = st.text_input("Duration (e.g., 1 Month, 3 Months)")
        owner_contact = st.text_input("Owner Contact (Email)")
        image_url = st.text_input("Image URL (Optional, placeholder will be used if empty)")
        submit_button = st.form_submit_button("Add Property")

        if submit_button:
            if property_name and location and rent and duration and owner_contact:
                add_property(property_name, location, rent, duration, owner_contact, image_url if image_url else 'https://via.placeholder.com/150')
                st.success("Property added successfully!")
                st.rerun() # Refresh to show updated table
            else:
                st.error("Please fill in all required fields.")

    # Edit and Delete Functionality (using expander for each property)
    st.subheader("Edit/Delete Properties")
    for index, property_data in properties_df.iterrows():
        with st.expander(f"Edit/Delete: {property_data['property_name']}", expanded=False):
            with st.form(f"edit_property_form_{property_data['id']}"):
                property_name = st.text_input("Property Name", value=property_data['property_name'])
                location = st.selectbox("Location", ["Vadodara", "Mumbai", "Ahmedabad", "Other"], index=["Vadodara", "Mumbai", "Ahmedabad", "Other"].index(property_data['location']))
                rent = st.number_input("Rent (INR)", min_value=1000, value=property_data['rent'])
                duration = st.text_input("Duration", value=property_data['duration'])
                owner_contact = st.text_input("Owner Contact (Email)", value=property_data['owner_contact'])
                image_url = st.text_input("Image URL", value=property_data['image_url'] if property_data['image_url'] else '')
                update_button = st.form_submit_button("Update Property")
                delete_button = st.form_submit_button("Delete Property")

                if update_button:
                    update_property(property_data['id'], property_name, location, rent, duration, owner_contact, image_url if image_url else 'https://via.placeholder.com/150')
                    st.success("Property updated successfully!")
                    st.rerun() # Refresh to show updated table
                if delete_button:
                    delete_property(property_data['id'])
                    st.success("Property deleted successfully!")
                    st.rerun() # Refresh to show updated table


if __name__ == '__main__':
    show_page() # For testing page directly
