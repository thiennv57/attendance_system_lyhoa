import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'students.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE student ADD COLUMN comment_last_updated_by VARCHAR(100);")
    print("Column comment_last_updated_by added successfully.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Column comment_last_updated_by already exists.")
    else:
        print(f"Error adding column comment_last_updated_by: {e}")

try:
    cursor.execute("ALTER TABLE student ADD COLUMN comment_last_updated_at DATETIME;")
    print("Column comment_last_updated_at added successfully.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Column comment_last_updated_at already exists.")
    else:
        print(f"Error adding column comment_last_updated_at: {e}")

conn.commit()
conn.close()