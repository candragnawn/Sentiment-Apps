from supabase import create_client
import json

url ="https://fbkfqsqqkxobmdefokjz.supabase.co"
key ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZia2Zxc3Fxa3hvYm1kZWZva2p6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODkyMjg2MywiZXhwIjoyMDg0NDk4ODYzfQ.5tdJc8WIqnt9F9kPUrQEIiKQmszAlzs1OVQtFROxFiM"
supabase = create_client(url, key)

try:
    response = supabase.table('sentiments').select("*", count='exact').limit(1).execute()
    print(f"Connection success. Count: {response.count}")
    print(f"Data sample: {json.dumps(response.data, indent=2)}")
except Exception as e:
    print(f"Connection failed: {e}")
