import sys
import os
from pathlib import Path

# Add backend/src to path
sys.path.append(str(Path.cwd() / "backend" / "src"))

from database.database_supabase import SentimentDatabase

def check():
    db = SentimentDatabase()
    data = db.fetch_all_data()
    print(f"Total rows: {len(data)}")
    if not data:
        print("No data found.")
        return

    print(f"Keys in a row: {list(data[0].keys())}")

    # Check first few rows
    for i, row in enumerate(data[:10]):
        print(f"Row {i}: Platform={row.get('platform')}, Published Date={row.get('published_date')}, Created At={row.get('created_at')}")

    # Check if 'published_date' column exists in any row
    has_pub_date = any('published_date' in row for row in data)
    print(f"Has 'published_date' key in at least one row: {has_pub_date}")

    # Find rows WITH published_date
    rows_with_date = [r for r in data if r.get('published_date') is not None]
    print(f"Rows with non-None published_date: {len(rows_with_date)}")
    if rows_with_date:
        print(f"Example valid date: {rows_with_date[0].get('published_date')}")

if __name__ == "__main__":
    check()
