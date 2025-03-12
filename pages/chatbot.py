import streamlit as st

def show_page():
    st.markdown("<div class='section-header'>Chatbot - Your Rental Assistant</div>", unsafe_allow_html=True)

    # Improved rule-based chatbot with more responses
    faq_responses = {
        "hello": "Hello there! Welcome to Avishkar Rentals. How can I help you find the perfect place today?",
        "hi": "Greetings! What rental questions do you have for me?",
        "hey": "Hey!  Looking for rentals? I'm here to assist.",
        "rentals": "You can browse all our available rental listings on the 'Rental Listings' page. Filter by location and rent to find your ideal property.",
        "properties": "Looking for properties?  Visit 'Rental Listings' to see what's available.",
        "listings": "Available listings are on the 'Rental Listings' page.",
        "libraries": "Need a quiet place to study? Check out the 'Libraries' page for a list of local libraries in the city.",
        "coaching centers": "Preparing for exams? Find local coaching centers on the 'Coaching Centers' page.",
        "book a property": "To book a property, go to the 'Rental Listings' page, filter the listings, and you'll find a booking form below the property details.",
        "booking": "Property bookings can be made on the 'Rental Listings' page.  See a listing you like? Book it there!",
        "how to book": "Booking is easy! On the 'Rental Listings' page, find your property and use the booking form provided.",
        "leave a review": "We value your feedback! You can leave a review on the main page in the 'Leave a Review' section, or find it in the navigation sidebar.",
        "reviews": "Want to leave feedback? Use the 'Leave a Review' section in the navigation.",
        "contact": "For property-specific inquiries, you'll find the owner's contact information in each listing. For general questions, feel free to ask me!",
        "help": "I can help you with finding rental listings, information on libraries and coaching centers, booking properties, and leaving reviews. What do you need help with today?",
        "default": "I'm here to help with rentals, local libraries, and coaching centers. Please ask me about listings, locations, booking, or reviews.  For specific property inquiries, see the owner's contact in the listing."
    }

    user_query = st.text_input("Ask me a question about rentals, libraries, or coaching centers:", placeholder="Type your question here...")

    if user_query:
        query_lower = user_query.lower()
        response = ""
        for keyword, answer in faq_responses.items():
            if keyword in query_lower:
                response = answer
                break
        if not response:
            response = faq_responses["default"]

        st.write("Chatbot: ", response)

if __name__ == '__main__':
    show_page()
