import sqlite3

DATABASE_NAME = 'renters_app.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update properties table to include image_url
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_name TEXT NOT NULL,
            location TEXT NOT NULL,
            rent INTEGER NOT NULL,
            duration TEXT,
            owner_contact TEXT,
            image_url TEXT DEFAULT 'https://via.placeholder.com/150' -- Default placeholder
        )
    """)

    # Reviews table (no change needed in structure for this step, but can be enhanced later)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER,
            reviewer_name TEXT,
            review_text TEXT,
            rating INTEGER,
            FOREIGN KEY (property_id) REFERENCES properties(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libraries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            library_name TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coaching_centers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            center_name TEXT NOT NULL,
            location TEXT NOT NULL,
            specialization TEXT
        )
    """)

    # Sample data (with placeholder image URLs)
    properties_data = [
        ("Student PG in Vadodara", "Vadodara", 6000, "1 Month", "ramesh_rentals@gmail.com", "https://via.placeholder.com/150/0077bb?text=PG"),
        ("1BHK near MSU", "Vadodara", 12000, "3 Months", "Kishan_houses@gmail.com", "https://via.placeholder.com/150/22aa44?text=1BHK"),
        ("Shared Hostel Room", "Mumbai", 5000, "6 Months", "satyam_pgs@gmail.com", "https://via.placeholder.com/150/dd3355?text=Hostel"),
        ("2BHK Apartment", "Ahmedabad", 18000, "12 Months", "vijay.rentals@example.com", "https://via.placeholder.com/150/ffbb22?text=2BHK"),
        ("Studio Apartment", "Vadodara", 8000, "3 Months", "info@modernliving.in", "https://via.placeholder.com/150/550099?text=Studio")
    ]
    cursor.executemany("INSERT OR IGNORE INTO properties (property_name, location, rent, duration, owner_contact, image_url) VALUES (?, ?, ?, ?, ?, ?)", properties_data)


    libraries_data = [
        ("City Central Library", "Vadodara", "Large library with extensive collection."),
        ("University Library", "Vadodara", "Primarily for university students but open to public.")
    ]
    cursor.executemany("INSERT OR IGNORE INTO libraries (library_name, location, description) VALUES (?, ?, ?)", libraries_data)

    coaching_centers_data = [
        ("Excellent Coaching Classes", "Vadodara", "IIT-JEE and NEET coaching."),
        ("Brilliant Tutors", "Vadodara", "Coaching for all subjects, all grades.")
    ]
    cursor.executemany("INSERT OR IGNORE INTO coaching_centers (center_name, location, specialization) VALUES (?, ?, ?)", coaching_centers_data)

    conn.commit()
    conn.close()


# CRUD operations for properties
def get_properties():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM properties", conn)
    conn.close()
    return df

def get_property(property_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM properties WHERE id = ?", (property_id,))
    property = cursor.fetchone()
    conn.close()
    return property

def add_property(property_name, location, rent, duration, owner_contact, image_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO properties (property_name, location, rent, duration, owner_contact, image_url)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (property_name, location, rent, duration, owner_contact, image_url))
    conn.commit()
    conn.close()

def update_property(property_id, property_name, location, rent, duration, owner_contact, image_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE properties SET
        property_name = ?, location = ?, rent = ?, duration = ?, owner_contact = ?, image_url = ?
        WHERE id = ?
    """, (property_name, location, rent, duration, owner_contact, image_url, property_id))
    conn.commit()
    conn.close()

def delete_property(property_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM properties WHERE id = ?", (property_id,))
    conn.commit()
    conn.close()

# CRUD operations for reviews (basic add and get for now)
def add_review(property_id, reviewer_name, review_text, rating):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reviews (property_id, reviewer_name, review_text, rating)
        VALUES (?, ?, ?, ?)
    """, (property_id, reviewer_name, review_text, rating))
    conn.commit()
    conn.close()

def get_reviews_for_property(property_id):
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM reviews WHERE property_id = ?", conn, params=(property_id,))
    conn.close()
    return df


if __name__ == '__main__':
    initialize_database() # Run to update table structure and data
    print("Database initialized/updated with property images and CRUD functions.")
