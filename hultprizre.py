
import streamlit as st
import pandas as pd

# Sample data for listings
data = {
    "Property Name": ["Student PG in Vadodara", "1BHK near MSU", "Shared Hostel Room"],
    "Location": ["Vadodara", "Vadodara", "Vadodara"],
    "Rent (INR)": [6000, 12000, 5000],
    "Duration": ["1 Month", "3 Months", "6 Months"],
    "Owner Contact": ["owner1@example.com", "owner2@example.com", "owner3@example.com"]
}

df = pd.DataFrame(data)

# Streamlit App
st.title("Student Rental Platform - Prototype")

# Sidebar Filters
st.sidebar.header("Search Filters")
location_filter = st.sidebar.selectbox("Select Location", df["Location"].unique())
max_rent = st.sidebar.slider("Max Rent (INR)", min_value=3000, max_value=20000, value=10000)

# Filtered Results
filtered_df = df[(df["Location"] == location_filter) & (df["Rent (INR)"] <= max_rent)]
st.write("### Available Listings")
st.table(filtered_df)

# Booking Request Form
st.write("## Book a Property")
selected_property = st.selectbox("Choose a Property", filtered_df["Property Name"])
name = st.text_input("Your Name")
email = st.text_input("Your Email")
if st.button("Submit Request"):
    st.success(f"Booking request sent for {selected_property}. The owner will contact you soon!")

# Review & Rating Section
st.write("## Leave a Review")
review_text = st.text_area("Write your feedback")
rating = st.slider("Rate out of 5", 1, 5, 3)
if st.button("Submit Review"):
    st.success("Review submitted successfully!")
