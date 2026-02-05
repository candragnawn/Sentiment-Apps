import sys
sys.path.append('backend/src')
from database.database_supabase import SentimentDatabase

db = SentimentDatabase()

print("Checking Supabase 'sentiments' table availability...")
try:
    # We use a direct query to bypass any internal try-except that might hide errors
    response = db.supabase.table('sentiments').select("*", count='exact').limit(1).execute()
    print(" Table 'sentiments' FOUND.")
    print(f"   Total records according to Supabase: {response.count}")
except Exception as e:
    print(" ERROR: Table 'sentiments' might be MISSING or there is a connection issue.")
    print(f"   Error Details: {e}")

print("\n--- Listing schemas (if possible) ---")
try:
    # This might fail depending on permissions but good to try
    res = db.supabase.rpc('get_tables').execute()
    print(f"Tables: {res.data}")
except:
    print("Could not list tables via RPC.")
