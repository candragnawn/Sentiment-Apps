import os
from supabase import create_client, client

class SentimentDatabase:
    def __init__(self):
        url: str ="https://fbkfqsqqkxobmdefokjz.supabase.co"
        key: str ="sb_publishable_fpW0PwIkQpDeGfdUzOq8wA_6fQ0DNvK"
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