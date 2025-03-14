
import streamlit as st
import pandas as pd

# Custom CSS for styling
st.markdown(
    unsafe_allow_html=True,
)

# Page Title with a custom header
st.markdown("<div class='main-header'>Rental house</div>",unsafe_allow_html=True)

# Display a banner image (replace the URL with your logo or image)
st.image(r"https://www.bing.com/images/search?view=detailV2&ccid=BrjQsl9c&id=09B5DBE6D3560E850D7C903F8159E7D04CE00D66&thid=OIP.BrjQsl9crKJYA7O_F_wjPwHaEU&mediaurl=https%3a%2f%2fcaboplatinum.com%2fwp-content%2fuploads%2f2020%2f04%2finternational-luxury-villa.jpg&exph=1119&expw=1920&q=rentals&simid=608038362199041216&FORM=IRPRST&ck=BFFAEA110A39CA9BD802B850C6F96643&selectedIndex=1&itb=0", use_container_width=True)

# Sample data for listings
data = {
    "Property Name": ["Student PG in Vadodara", "1BHK near MSU", "Shared Hostel Room", "2BHK Apartment", "Studio Apartment"],
    "Location": ["Vadodara", "Vadodara", "Mumbai", "Ahmedabad", "Vadodara"],
    "Rent (INR)": [6000, 12000, 5000, 18000, 8000],
    "Duration": ["1 Month", "3 Months", "6 Months", "12 Months", "3 Months"],
    "Owner Contact": ["ramesh_rentals@gmail.com", "Kishan_houses@gmail.com", "satyam_pgs@gmail.com", "vijay.rentals@example.com", "info@modernliving.in"]
}
df = pd.DataFrame(data)

# Sidebar with custom styling header
st.sidebar.markdown("<h2 style='color: #4CAF50;'>Search Filters</h2>", unsafe_allow_html=True)
location_filter = st.sidebar.selectbox("Select Location", df["Location"].unique())
max_rent = st.sidebar.slider("Max Rent (INR)", min_value=3000, max_value=20000, value=15000)

# Filtered Results
filtered_df = df[(df["Location"] == location_filter) & (df["Rent (INR)"] <= max_rent)]

if filtered_df.empty:
    st.markdown("<h3>No Listings Found</h3>", unsafe_allow_html=True)
else:
    st.markdown("<h3>Available Listings</h3>", unsafe_allow_html=True)
    st.table(filtered_df)

# Booking Request Form with a stylish form
st.markdown("<h3>Book a Property</h3>", unsafe_allow_html=True)

if not filtered_df.empty:
    selected_property = st.selectbox("Choose a Property", filtered_df["Property Name"])
    name = st.text_input("Your Name", placeholder="Enter your full name")
    email = st.text_input("Your Email", placeholder="Enter your email address")
    if st.button("Submit Request"):
        st.success(f"Booking request sent for {selected_property}. The owner will contact you soon!")
else:
    st.write("Please select a location and rent to see available properties and book.")

# Review & Rating Section
st.markdown("<h3>Leave a Review</h3>", unsafe_allow_html=True)
review_text = st.text_area("Write your feedback", placeholder="Your thoughts...")
rating = st.slider("Rate out of 5", 1, 5, 3)
if st.button("Submit Review"):
    st.success("Review submitted successfully!")


