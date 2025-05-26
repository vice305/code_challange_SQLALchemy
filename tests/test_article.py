import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from scripts.setup_db import setup_database

@pytest.fixture
def setup_db():
    setup_database()
    yield

def test_article_creation(setup_db):
    author = Author.find_by_id(1)
    magazine = Magazine.find_by_id(1)
    article = Article("New Article", author, magazine)
    assert article.save()
    assert article.id is not None