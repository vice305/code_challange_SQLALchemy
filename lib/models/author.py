from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self._name = None
        self.name = name  
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value
    
    def save(self):
        conn = get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                if self.id is None:
                    cursor.execute("INSERT INTO authors (name) VALUES (?) RETURNING id", (self.name,))
                    self.id = cursor.fetchone()['id']
                else:
                    cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(row['name'], row['id']) if row else None
    
    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles
    
    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return magazines
    
    def add_article(self, magazine, title):
        from lib.models.article import Article
        article = Article(title, self, magazine)
        return article.save()
    
    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        categories = [row['category'] for row in cursor.fetchall()]
        conn.close()
        return categories