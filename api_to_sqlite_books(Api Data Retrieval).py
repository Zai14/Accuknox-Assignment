import requests
import sqlite3

# i have used an free api from google search
API_URL = "https://openlibrary.org/search.json?q=programming&limit=10"

# db setup
db_name = "books.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        year INTEGER,
        UNIQUE(title, author)
    )
""")
conn.commit()

# getting data from api
try:
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    conn.close()
    exit()

# makeing the data in req. format
try:
    books = data.get("docs", [])
    for item in books:
        title = item.get("title", "Unknown")
        authors = item.get("author_name", ["Unknown"])
        author = authors[0] if authors else "Unknown"
        year = item.get("first_publish_year", 2021)
        
        cursor.execute(
            "INSERT OR IGNORE INTO books (title, author, year) VALUES (?, ?, ?)",
            (title, author, year)
        )
    conn.commit()
    print(f"Inserted {len(books)} books into the database successfully.")
except Exception as e:
    print(f"Error inserting data: {e}")
    conn.close()
    exit()

# Get evrything and print
try:
    cursor.execute("SELECT title, author, year FROM books")
    rows = cursor.fetchall()
    
    print("\n--- Books in Database ---")
    for title, author, year in rows:
        print(f"{title} | {author} | {year}")
except Exception as e:
    print(f"Error retrieving data: {e}")
finally:
    conn.close()
