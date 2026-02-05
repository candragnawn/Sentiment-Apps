from database.database_supabase import SentimentDatabase
db = SentimentDatabase()
keyword = "Timothy Ronald"
data = db.supabase.table('sentiments').select("*").eq('keyword', keyword).execute()
print(f"Rows for '{keyword}': {len(data.data)}")
if len(data.data) > 0:
    print(f"Sample labels: {[d['label'] for d in data.data[:5]]}")
