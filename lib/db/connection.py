import sqlite3

def get_connection():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row  # Lets us access columns by name (e.g., row['name'])
    conn.execute("PRAGMA foreign_keys = ON;")  # Enforce foreign key constraints
    return conn
