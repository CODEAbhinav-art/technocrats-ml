import sqlite3
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash # For password hashing

DATABASE_NAME = 'renters_app.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # User Roles: admin, property_owner, renter (basic for now)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'renter' -- default role
        )
    """)

    # Update properties table: Add property_type and location data (lat, long)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_name TEXT NOT NULL,
            property_type TEXT DEFAULT 'Apartment', -- e.g., Apartment, PG, 1BHK, Studio
            location TEXT NOT NULL,
            latitude REAL,    -- Latitude for map
            longitude REAL,   -- Longitude for map
            rent INTEGER NOT NULL,
            duration TEXT,
            owner_contact TEXT,
            image_filename TEXT -- Store filename instead of URL (for local upload)
        )
    """)

    # Reviews table (no changes needed in structure for this step)
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

    # Sample data updates: Include property_type, image_filename, lat/long (example lat/long)
    properties_data = [
        ("Student PG - Cozy", "PG", "Vadodara", 22.3072, 73.1812, 6000, "1 Month", "ramesh_rentals@gmail.com", "property_pg1.jpg"),
        ("1BHK - Near University", "1BHK", "Vadodara", 22.3145, 73.1797, 12000, "3 Months", "Kishan_houses@gmail.com", "property_1bhk1.jpg"),
        ("Shared Hostel - Central Mumbai", "Hostel", "Mumbai", 19.0760, 72.8777, 5000, "6 Months", "satyam_pgs@gmail.com", "property_hostel1.jpg"),
        ("2BHK Apartment - Ahmedabad Suburbs", "2BHK", "Ahmedabad", 23.0225, 72.5714, 18000, "12 Months", "vijay.rentals@example.com", "property_2bhk1.jpg"),
        ("Studio Apt - Downtown Vadodara", "Studio", "Vadodara", 22.2982, 73.1868, 8000, "3 Months", "info@modernliving.in", "property_studio1.jpg")
    ]
    cursor.executemany("INSERT OR IGNORE INTO properties (property_name, property_type, location, latitude, longitude, rent, duration, owner_contact, image_filename) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", properties_data)

    # Sample User (Admin - username 'admin', password 'adminpass')
    admin_password = generate_password_hash('adminpass') # Hash the password
    cursor.execute("INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)", ('admin', admin_password, 'admin'))


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


# Authentication related functions
def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(username, password, role='renter'):
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    try:
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, password_hash, role))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError: # Username already exists
        conn.close()
        return False


# (CRUD operations for properties remain the same, but update to use 'image_filename' and 'property_type')
def get_properties(): # Updated to select property_type as well
    conn = get_db_connection()
    df = pd.read_sql("SELECT id, property_name, property_type, location, latitude, longitude, rent, duration, owner_contact, image_filename FROM properties", conn) # Select image_filename
    conn.close()
    return df

def get_property(property_id): # Updated to select property_type and image_filename
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, property_name, property_type, location, latitude, longitude, rent, duration, owner_contact, image_filename FROM properties WHERE id = ?", (property_id,)) # Select image_filename
    property = cursor.fetchone()
    conn.close()
    return property

def add_property(property_name, property_type, location, latitude, longitude, rent, duration, owner_contact, image_filename): # Added property_type, latitude, longitude, image_filename
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO properties (property_name, property_type, location, latitude, longitude, rent, duration, owner_contact, image_filename)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (property_name, property_type, location, latitude, longitude, rent, duration, owner_contact, image_filename))
    conn.commit()
    conn.close()

def update_property(property_id, property_name, property_type, location, latitude, longitude, rent, duration, owner_contact, image_filename): # Added property_type, latitude, longitude, image_filename
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE properties SET
        property_name = ?, property_type = ?, location = ?, latitude = ?, longitude = ?, rent = ?, duration = ?, owner_contact = ?, image_filename = ?
        WHERE id = ?
    """, (property_name, property_type, location, latitude, longitude, rent, duration, owner_contact, image_filename, property_id))
    conn.commit()
    conn.close()

def delete_property(property_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM properties WHERE id = ?", (property_id,))
    conn.commit()
    conn.close()

# Review CRUD operations (same as before - no structural change needed for basic review functionality)
def add_review(property_id, reviewer_name, review_text, rating): # Same
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reviews (property_id, reviewer_name, review_text, rating)
        VALUES (?, ?, ?, ?)
    """, (property_id, reviewer_name, review_text, rating))
    conn.commit()
    conn.close()

def get_reviews_for_property(property_id): # Same
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM reviews WHERE property_id = ?", conn, params=(property_id,))
    conn.close()
    return df


if __name__ == '__main__':
    initialize_database()
    print("Database initialized/updated with User Authentication, Property Types, Location Data, and Image Filenames.")
