import os
from supabase import create_client, client

class SentimentDatabase:
    def __init__(self):
        url: str ="https://fbkfqsqqkxobmdefokjz.supabase.co"
        key: str ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZia2Zxc3Fxa3hvYm1kZWZva2p6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODkyMjg2MywiZXhwIjoyMDg0NDk4ODYzfQ.5tdJc8WIqnt9F9kPUrQEIiKQmszAlzs1OVQtFROxFiM"
        self.supabase: client = create_client(url,key)

    def save_results(self, data_dict):
        try:
            response = self.supabase.table('sentiments').insert(data_dict).execute()
            print(f"data saved to supabase {len(data_dict)} data ke cloud")
        except Exception as e:
            print(f"error saving data to supabase: {e}")
    def hapus_semua_data(self):
        try:
            self.supabase.table('sentiments').delete().neq('id', 0).execute()
            print("all data delete from supabase")

        except Exception as e:
            print(f"error deleting data from supabase: {e}")

    def fetch_all_data(self):
        try:
            response = self.supabase.table('sentiments').select("*").execute()
            return response.data
        except Exception as e:
            print(f"error fetching data from supabase: {e}")
            return []