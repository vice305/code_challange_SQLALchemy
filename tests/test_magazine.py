import pytest
from lib.models.magazine import Magazine
from scripts.setup_db import setup_database

@pytest.fixture
def setup_db():
    setup_database()
    yield

def test_magazine_creation(setup_db):
    magazine = Magazine("Test Mag", "Test Category")
    assert magazine.save()
    assert magazine.id is not None
    assert magazine.name == "Test Mag"

def test_magazine_articles(setup_db):
    magazine = Magazine.find_by_id(1)
    articles = magazine.articles()
    assert len(articles) > 0