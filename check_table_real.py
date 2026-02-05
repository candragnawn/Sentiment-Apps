import sys
sys.path.append('backend/src')
from database.database_supabase import SentimentDatabase
from postgrest.exceptions import APIError

db = SentimentDatabase()

print("DEBUG: Checking table 'sentiments'...")
try:
    # This bypasses the try-except in SentimentDatabase.fetch_all_data
    res = db.supabase.table('sentiments').select('*', count='exact').limit(1).execute()
    print(f"SUCCESS: Table exists. Row count: {res.count}")
except APIError as e:
    print(f"API ERROR: {e.message}")
    if "relation \"public.sentiments\" does not exist" in e.message:
        print("CONFIRMED: Table 'sentiments' is MISSING.")
    else:
        print("Table exists but query failed (maybe column missing?)")
except Exception as e:
    print(f"OTHER ERROR: {e}")
