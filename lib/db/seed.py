from lib.db.connection import get_connection

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    
    # Add authors
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("John Doe",))
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Jane Smith",))
    
    # Add magazines
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Weekly", "Technology"))
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Fashion Monthly", "Fashion"))
    
    # Add articles
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                  ("Tech Trends", 1, 1))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                  ("Fashion Tips", 2, 2))
    
    conn.commit()
    conn.close()