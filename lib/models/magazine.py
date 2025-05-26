from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self._name = None
        self._category = None
        self.name = name
        self.category = category
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Category must be a non-empty string")
        self._category = value
    
    def save(self):
        conn = get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                if self.id is None:
                    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?) RETURNING id", 
                                 (self.name, self.category))
                    self.id = cursor.fetchone()['id']
                else:
                    cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", 
                                 (self.name, self.category, self.id))
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(row['name'], row['category'], row['id']) if row else None
    
    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles
    
    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles art ON a.id = art.author_id
            WHERE art.magazine_id = ?
        """, (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return authors
    
    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        titles = [row['title'] for row in cursor.fetchall()]
        conn.close()
        return titles
    
    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.* FROM authors a
            JOIN articles art ON a.id = art.author_id
            WHERE art.magazine_id = ?
            GROUP BY a.id
            HAVING COUNT(art.id) > 2
        """, (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return authors