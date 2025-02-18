# import streamlit as st
# import pandas as pd

# # Custom CSS for styling
# st.markdown(
#     """
#     <style>
#     /* Custom background for the whole app */
#     .stApp {
#         background: linear-gradient(135deg, #f0f0f0, #e0e0e0);
#     }
#     /* Main header styling */
#     .main-header {
#         font-size: 3em;
#         font-weight: bold;
#         text-align: center;
#         color: #333;
#         margin-bottom: 20px;
#     }
#     /* Sidebar header styling */
#     .sidebar .sidebar-content {
#         background-color: #fafafa;
#         padding: 20px;
#         border-radius: 8px;
#     }
#     /* Button styling */
#     .css-1emrehy.edgvbvh3 { 
#         background-color: #4CAF50;
#         border: none;
#         color: white;
#         padding: 10px 20px;
#         text-align: center;
#         border-radius: 4px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Page Title with a custom header
# st.markdown("<div class='main-header'>Avishkar Rentals</div>", unsafe_allow_html=True)

# # Display a banner image (replace the URL with your logo or image)
# st.image("https://via.placeholder.com/800x200.png?text=Student+Rental+Platform", use_column_width=True)

# # Sample data for listings
# data = {
#     "Property Name": ["Student PG in Vadodara", "1BHK near MSU", "Shared Hostel Room"],
#     "Location": ["Vadodara", "ahmedabad", "mumbai"],
#     "Rent (INR)": [6000, 12000, 5000],
#     "Duration": ["1 Month", "3 Months", "6 Months"],
#     "Owner Contact": ["ramesh_rentals@gmail.com", "Kishan_houses@gmail.com", "satyam_pgs@gmail.com"]
# }
# df = pd.DataFrame(data)

# # Sidebar with custom styling header
# st.sidebar.markdown("<h2 style='color: #4CAF50;'>Search Filters</h2>", unsafe_allow_html=True)
# location_filter = st.sidebar.selectbox("Select Location", df["Location"].unique())
# max_rent = st.sidebar.slider("Max Rent (INR)", min_value=3000, max_value=10000, value=5000)

# # Filtered Results
# filtered_df = df[(df["Location"] == location_filter) & (df["Rent (INR)"] <= max_rent)]
# st.markdown("<h3>Available Listings</h3>", unsafe_allow_html=True)
# st.table(filtered_df)

# # Booking Request Form with a stylish form
# st.markdown("<h3>Book a Property</h3>", unsafe_allow_html=True)
# selected_property = st.selectbox("Choose a Property", filtered_df["Property Name"])
# name = st.text_input("Your Name", placeholder="Enter your full name")
# email = st.text_input("Your Email", placeholder="Enter your email address")
# if st.button("Submit Request"):
#     st.success(f"Booking request sent for {selected_property}. The owner will contact you soon!")

# # Review & Rating Section
# st.markdown("<h3>Leave a Review</h3>", unsafe_allow_html=True)
# review_text = st.text_area("Write your feedback", placeholder="Your thoughts...")
# rating = st.slider("Rate out of 5", 1, 5, 3)
# if st.button("Submit Review"):
#     st.success("Review submitted successfully!")

# import streamlit as st
# import pandas as pd

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Custom background for the whole app */
    .stApp {
        background: url('https://i.pinimg.com/560x/e0/75/62/e0756209594f8615c44ca0f55e5b600f.jpg'); /* Replace with your image URL */
        background-size: cover;
        background-repeat: no-repeat;
        color: #333; /* Adjust text color for contrast */
    }

    /* Overlay for better text readability (optional) */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
    }

    /* Main header styling */
    .main-header {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        color: #333;
        margin-bottom: 20px;
    }
    /* Sidebar header styling */
    .sidebar .sidebar-content {
        background-color: rgba(250, 250, 250, 0.9);
        padding: 20px;
        border-radius: 8px;
    }
    /* Button styling */
    .css-1emrehy.edgvbvh3 { 
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        border-radius: 4px;
    }
    /* Table Styling */
    .dataframe {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 8px;
    }
    /* Form Styling */
    .stTextInput, .stSelectbox, .stTextArea {
        background-color: rgba(255, 255, 255, 0.7); /* Transparent white background for inputs */
        border-radius: 5px;
        padding: 8px;
        margin-bottom: 10px;  /* Space between form elements */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page Title with a custom header
st.markdown("<div class='main-header'>Avishkar Rentals</div>", unsafe_allow_html=True)

# Display a banner image (replace the URL with your logo or image)
st.image("https://via.placeholder.com/800x200.png?text=Student+Rental+Platform", use_column_width=True)

# Sample data for listings (Improved data)
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
max_rent = st.sidebar.slider("Max Rent (INR)", min_value=3000, max_value=20000, value=15000) # Increased max value

# Filtered Results
filtered_df = df[(df["Location"] == location_filter) & (df["Rent (INR)"] <= max_rent)]

if filtered_df.empty:  # Handle the case where no listings match
    st.markdown("<h3>No Listings Found</h3>", unsafe_allow_html=True)
else:
    st.markdown("<h3>Available Listings</h3>", unsafe_allow_html=True)
    st.table(filtered_df)


# Booking Request Form with a stylish form
st.markdown("<h3>Book a Property</h3>", unsafe_allow_html=True)

if not filtered_df.empty:  # Only show the form if there are listings
    selected_property = st.selectbox("Choose a Property", filtered_df["Property Name"])
    name = st.text_input("Your Name", placeholder="Enter your full name")
    email = st.text_input("Your Email", placeholder="Enter your email address")
    if st.button("Submit Request"):
        st.success(f"Booking request sent for {selected_property}. The owner will contact you soon!")
else:
    st.write("Please select a location and rent to see available properties and book.")  # Informative message


# Review & Rating Section (No changes needed, but you can improve this later)
st.markdown("<h3>Leave a Review</h3>", unsafe_allow_html=True)
review_text = st.text_area("Write your feedback", placeholder="Your thoughts...")
rating = st.slider("Rate out of 5", 1, 5, 3)
if st.button("Submit Review"):
    st.success("Review submitted successfully!")
