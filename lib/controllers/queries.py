from lib.db.connection import get_connection

def magazines_with_multiple_authors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.* FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.id
        HAVING COUNT(DISTINCT a.author_id) >= 2
    """)
    magazines = cursor.fetchall()
    conn.close()
    return magazines

def article_count_per_magazine():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.name, COUNT(a.id) as article_count FROM magazines m
        LEFT JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.id
    """)
    counts = cursor.fetchall()
    conn.close()
    return counts

def most_prolific_author():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.*, COUNT(art.id) as article_count FROM authors a
        LEFT JOIN articles art ON a.id = art.author_id
        GROUP BY a.id
        ORDER BY article_count DESC
        LIMIT 1
    """)
    author = cursor.fetchone()
    conn.close()
    return author