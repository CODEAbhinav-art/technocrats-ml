import streamlit as st
import pandas as pd
from database import get_db_connection, add_review, get_reviews_for_property
import streamlit_folium as st_folium # Import folium integration

def show_page():
    st.markdown("<div class='section-header'>Discover Rental Properties</div>", unsafe_allow_html=True)

    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM properties", conn)
    locations = df["location"].unique()
    property_types = df["property_type"].unique() # Get unique property types
    conn.close()

    # Sidebar Filters
    with st.sidebar.expander("Filter Listings", expanded=True):
        location_filter = st.selectbox("Location", locations, index=0)
        property_type_filter = st.multiselect("Property Type", property_types, default=property_types.tolist()) # Multi-select property type
        max_rent = st.slider("Max Rent (INR)", min_value=3000, max_value=30000, value=20000)
        search_keyword = st.text_input("Keyword Search", placeholder="Search in property name") # Keyword search

    # Filtering Logic
    filtered_df = df[
        (df["location"] == location_filter) &
        (df["rent"] <= max_rent) &
        (df["property_type"].isin(property_type_filter)) # Filter by property type
    ]
    if search_keyword: # Apply keyword search if entered
        filtered_df = filtered_df[df["property_name"].str.contains(search_keyword, case=False)]

    if filtered_df.empty:
        st.markdown("No listings found matching your criteria.")
    else:
        # Map Display - Streamlit Folium
        st.subheader("Property Locations on Map")
        map_data = filtered_df[['latitude', 'longitude', 'property_name', 'property_type', 'rent', 'location', 'image_filename']].copy() # Data for map
        if not map_data.empty:
            map_center_lat = map_data['latitude'].mean()
            map_center_lon = map_data['longitude'].mean()

            # Create map with properties as markers
            property_map = st_folium.folium.Map(location=[map_center_lat, map_center_lon], zoom_start=12)
            for index, row in map_data.iterrows():
                popup_content = f"<b>{row['property_name']}</b><br>Type: {row['property_type']}<br>Rent: INR {row['rent']}<br>Location: {row['location']}<br><img src='./{row['image_filename']}' width='100'>" # Local image path in popup (needs to be accessible by Streamlit)
                st_folium.folium.Marker(
                    [row['latitude'], row['longitude']],
                    popup=st_folium.folium.Popup(popup_content, max_width=250),
                    tooltip=row['property_name']
                ).add_to(property_map)
            st_folium.st_folium(property_map, width=700, height=500) # Display map

        # Property Listings Display (List View Below Map)
        st.subheader("Listings")
        for index, property_data in filtered_df.iterrows():
            st.markdown(f"#### {property_data['property_name']} ({property_data['property_type']})") # Include property type in header
            col1, col2 = st.columns([1, 2])
            with col1:
                property_image_path = property_data['image_filename']
                if property_image_path and os.path.exists(property_image_path): # Check if image exists
                    st.image(property_image_path, width=150) # Display local image
                else:
                    st.image("https://via.placeholder.com/150/cccccc?text=No+Image", width=150) # Placeholder if no image

            with col2:
                st.write(f"**Location:** {property_data['location']}")
                st.write(f"**Rent:** INR {property_data['rent']} per month")
                st.write(f"**Duration:** {property_data['duration']}")
                st.write(f"**Contact:** {property_data['owner_contact']}")

            # Reviews Section (Enhanced Display)
            reviews_df = get_reviews_for_property(property_data['id'])
            if not reviews_df.empty:
                st.markdown("##### Reviews:")
                average_rating = reviews_df['rating'].mean() # Calculate average rating
                st.write(f"**Average Rating: {average_rating:.2f} / 5 stars**") # Display average rating
                for review_index, review_data in reviews_df.iterrows():
                    st.write(f"**{review_data['reviewer_name']}** (Rated: {review_data['rating']}/5):")
                    st.write(f"  > *\"{review_data['review_text']}\"*")
            else:
                st.write("No reviews yet.")

            # Review Submission Form
            with st.expander("Leave a Review", expanded=False):
                with st.form(f"review_form_{property_data['id']}", clear_on_submit=True):
                    reviewer_name = st.text_input("Your Name")
                    review_text = st.text_area("Your Review")
                    rating = st.slider("Rating (1-5 stars)", 1, 5, 3)
                    submit_review_button = st.form_submit_button("Submit Review")

                    if submit_review_button:
                        if reviewer_name and review_text:
                            add_review(property_data['id'], reviewer_name, review_text, rating)
                            st.success("Review submitted successfully! Refresh to see it.")
                        else:
                            st.error("Please enter your name and review.")
            st.markdown("---")

        # Booking Request Form (at the bottom)
        st.markdown("<div class='section-header'>Book a Property</div>", unsafe_allow_html=True)
        if not filtered_df.empty:
            selected_property_name_book = st.selectbox("Choose a Property to Book (from listings above)", filtered_df["property_name"].tolist(), key="booking_selectbox")
            name = st.text_input("Your Name", placeholder="Enter your full name", key="booking_name_input")
            email = st.text_input("Your Email", placeholder="Enter your email address", key="booking_email_input")
            if st.button("Submit Booking Request", key="booking_submit_button"):
                st.success(f"Booking request sent for '{selected_property_name_book}'. Owner will contact you soon!")
        else:
            st.write("Please select criteria to see available properties and book.")


if __name__ == '__main__':
    show_page()
