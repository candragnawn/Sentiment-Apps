from database.database_supabase import SentimentDatabase
db = SentimentDatabase()
data = db.fetch_all_data()
print(f"Total rows in DB: {len(data)}")
if len(data) > 0:
    print(f"First row: {data[0]}")
