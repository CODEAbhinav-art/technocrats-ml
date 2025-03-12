import streamlit as st
import pandas as pd
from database import get_db_connection, add_review, get_reviews_for_property

def show_page():
    st.markdown("<div class='section-header'>Available Rental Listings</div>", unsafe_allow_html=True)

    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM properties", conn)
    locations = df["location"].unique()
    conn.close()

    # Sidebar Filters
    with st.sidebar.expander("Filter Listings", expanded=True):
        location_filter = st.selectbox("Location", locations, index=0)
        max_rent = st.slider("Max Rent (INR)", min_value=3000, max_value=25000, value=15000)

    # Filtered Results
    filtered_df = df[(df["location"] == location_filter) & (df["rent"] <= max_rent)]

    if filtered_df.empty:
        st.markdown("No listings found in the selected location and rent range.")
    else:
        # Display Listings with Image and Details
        for index, property_data in filtered_df.iterrows():
            st.markdown(f"#### {property_data['property_name']}")
            col1, col2 = st.columns([1, 2]) # Adjust column ratio as needed
            with col1:
                st.image(property_data['image_url'], width=150) # Display image
            with col2:
                st.write(f"**Location:** {property_data['location']}")
                st.write(f"**Rent:** INR {property_data['rent']} per month")
                st.write(f"**Duration:** {property_data['duration']}")
                st.write(f"**Contact:** {property_data['owner_contact']}")

            # Reviews Section for each property (basic display)
            reviews_df = get_reviews_for_property(property_data['id'])
            if not reviews_df.empty:
                st.markdown("##### Reviews:")
                for review_index, review_data in reviews_df.iterrows():
                    st.write(f"**{review_data['reviewer_name']}** (Rated: {review_data['rating']}/5):")
                    st.write(f"  > *\"{review_data['review_text']}\"*")
            else:
                st.write("No reviews yet.")

            # Review Submission Form for each property
            with st.expander("Leave a Review", expanded=False):
                with st.form(f"review_form_{property_data['id']}", clear_on_submit=True):
                    reviewer_name = st.text_input("Your Name")
                    review_text = st.text_area("Your Review")
                    rating = st.slider("Rating (1-5 stars)", 1, 5, 3)
                    submit_review_button = st.form_submit_button("Submit Review")

                    if submit_review_button:
                        if reviewer_name and review_text:
                            add_review(property_data['id'], reviewer_name, review_text, rating)
                            st.success("Review submitted successfully! Refresh to see it.") # Refresh hint
                        else:
                            st.error("Please enter your name and review.")
            st.markdown("---") # Separator between properties

        # Booking Request Form (remains mostly the same but moved inside the loop for each property if needed)
        st.markdown("<div class='section-header'>Book a Property</div>", unsafe_allow_html=True) # Moved outside loop for single form at bottom, can be moved inside if needed per property
        if not filtered_df.empty:
            selected_property_name_book = st.selectbox("Choose a Property to Book (from listings above)", filtered_df["property_name"].tolist(), key="booking_selectbox") # Unique key
            name = st.text_input("Your Name", placeholder="Enter your full name", key="booking_name_input") # Unique keys
            email = st.text_input("Your Email", placeholder="Enter your email address", key="booking_email_input")
            if st.button("Submit Booking Request", key="booking_submit_button"): # Unique key
                st.success(f"Booking request sent for '{selected_property_name_book}'. Owner will contact you soon!")
        else:
            st.write("Please select a location and rent to see available properties and book.")


if __name__ == '__main__':
    show_page()
