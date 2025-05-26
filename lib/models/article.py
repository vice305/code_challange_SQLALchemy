from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author, magazine, id=None):
        self.id = id
        self._title = None
        self._author = None
        self._magazine = None
        self.title = title
        self.author = author
        self.magazine = magazine
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string")
        self._title = value
    
    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, value):
        from lib.models.author import Author
        if not isinstance(value, Author) or not value.id:
            raise ValueError("Author must be a saved Author object")
        self._author = value
    
    @property
    def magazine(self):
        return self._magazine
    
    @magazine.setter
    def magazine(self, value):
        from lib.models.magazine import Magazine
        if not isinstance(value, Magazine) or not value.id:
            raise ValueError("Magazine must be a saved Magazine object")
        self._magazine = value
    
    def save(self):
        conn = get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                if self.id is None:
                    cursor.execute("""
                        INSERT INTO articles (title, author_id, magazine_id) 
                        VALUES (?, ?, ?) RETURNING id
                    """, (self.title, self.author.id, self.magazine.id))
                    self.id = cursor.fetchone()['id']
                else:
                    cursor.execute("""
                        UPDATE articles SET title = ?, author_id = ?, magazine_id = ? 
                        WHERE id = ?
                    """, (self.title, self.author.id, self.magazine.id, self.id))
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False