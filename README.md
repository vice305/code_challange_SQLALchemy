# Articles Code Challenge
A Python app to manage Authors, Articles, and Magazines using SQLite and raw SQL.

## Setup
1. Activate virtual environment: `source env/bin/activate`
2. Install dependencies: `pip install pytest`
3. Set up database: `python scripts/setup_db.py`
4. Run tests: `pytest`

## Features
- Create and manage Authors, Magazines, and Articles.
- Query relationships (e.g., articles by author, magazines by author).
- CLI tool for interactive queries.