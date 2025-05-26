import pytest
from lib.models.author import Author
from scripts.setup_db import setup_database

@pytest.fixture
def setup_db():
    setup_database()
    yield

def test_author_creation(setup_db):
    author = Author("Test Author")
    assert author.save()
    assert author.id is not None
    assert author.name == "Test Author"

def test_author_articles(setup_db):
    author = Author.find_by_id(1)
    articles = author.articles()
    assert len(articles) > 0
    assert articles[0]['title'] == "Tech Trends"