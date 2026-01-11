import csv
import sqlite3

# db creation
db_name = "users.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# table to use for users info 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE
    )
""")
conn.commit()

# analyze csv to insert data
csv_file = "users.csv"
inserted_count = 0

try:
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # empty one rows skip
            if not row or not row.get("name") or not row.get("email"):
                continue
            
            name = row["name"].strip()
            email = row["email"].strip()
            
            # empty value skipped
            if not name or not email:
                continue
            
            # skip duplicate ones to insert non duplicate data
            try:
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    (name, email)
                )
                inserted_count += 1
            except sqlite3.IntegrityError:
                # skip duplicate email
                continue
        
        conn.commit()
        print(f"Inserted {inserted_count} rows into database.")

except FileNotFoundError:
    print(f"Error: {csv_file} not found.")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
