import os
from supabase import create_client, client
from datetime import datetime, timedelta

class SentimentDatabase:
    def check_existing_keyword(self, keyword):
        try:
          
            res = self.supabase.table("sentiments") \
                .select("id") \
                .eq("keyword", keyword) \
                .limit(1) \
                .execute()
            
      
            return len(res.data) > 0
        except Exception as e:
            print(f"Error checking cache: {e}")
            return False
    def __init__(self):
        url: str ="https://fbkfqsqqkxobmdefokjz.supabase.co"
        key: str ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZia2Zxc3Fxa3hvYm1kZWZva2p6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODkyMjg2MywiZXhwIjoyMDg0NDk4ODYzfQ.5tdJc8WIqnt9F9kPUrQEIiKQmszAlzs1OVQtFROxFiM"
        self.supabase: client = create_client(url, key)

    def save_results(self, data_dict):
        try:
            self.supabase.table('sentiments').insert(data_dict).execute()
        except Exception as e:
            print(f"Error saving to supabase: {e}")
    
    def hapus_semua_data(self):
        try:
            self.supabase.table('sentiments').delete().neq('id', 0).execute()
        except Exception as e:
            print(f"Error deleting from supabase: {e}")

    def fetch_all_data(self):
        try:
            response = self.supabase.table('sentiments').select("*").execute()
            return response.data
        except Exception as e:
            print(f"Error fetching: {e}")
            return []
    
    def fetch_data_by_date_range(self, start_date, end_date, keyword=None):
        try:
            query = self.supabase.table('sentiments').select("*")
            query = query.gte('created_at', start_date.isoformat())
            query = query.lte('created_at', end_date.isoformat())
            
            if keyword:
                query = query.eq('keyword', keyword)
            
            query = query.order('created_at', desc=True)
            response = query.execute()
            return response.data
        except Exception as e:
            print(f"Error fetching by range: {e}")
            return []
    
    def fetch_last_7_days(self, keyword=None):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        return self.fetch_data_by_date_range(start_date, end_date, keyword)
    
    def fetch_last_month(self, keyword=None):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        return self.fetch_data_by_date_range(start_date, end_date, keyword)
    
    def fetch_last_year(self, keyword=None):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        return self.fetch_data_by_date_range(start_date, end_date, keyword)
    
    def fetch_paginated(self, page=1, page_size=20, keyword=None):
        try:
            offset = (page - 1) * page_size
            query = self.supabase.table('sentiments').select("*")
            
            if keyword:
                query = query.eq('keyword', keyword)
            
            query = query.range(offset, offset + page_size - 1)
            query = query.order('created_at', desc=True)
            response = query.execute()
            
            count_query = self.supabase.table('sentiments').select("id", count='exact')
            if keyword:
                count_query = count_query.eq('keyword', keyword)
            count_response = count_query.execute()
            
            total = count_response.count if hasattr(count_response, 'count') else 0
            
            return {
                'data': response.data,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size if total > 0 else 0
            }
        except Exception as e:
            print(f"Error fetching paginated: {e}")
            return {'data': [], 'total': 0, 'page': page, 'page_size': page_size, 'total_pages': 0}

    def fetch_stats(self, keyword=None):
        try:
            query = self.supabase.table('sentiments').select("label", count='exact')
            if keyword:
                query = query.eq('keyword', keyword)
            
            response = query.execute()
            labels = [item['label'] for item in response.data]
            
            return {
                "total": len(labels),
                "positive": labels.count('positive'),
                "negative": labels.count('negative'),
                "neutral": labels.count('neutral')
            }
        except Exception as e:
            print(f"Error fetching stats: {e}")
            return {"total": 0, "positive": 0, "negative": 0, "neutral": 0}

    def fetch_chart_data(self, days=30, keyword=None):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            data = self.fetch_data_by_date_range(start_date, end_date, keyword)
            
            grouped = {}
            for item in data:
                date_str = item['created_at'].split('T')[0]
                if date_str not in grouped:
                    grouped[date_str] = {"date": date_str, "positive": 0, "negative": 0, "neutral": 0, "total": 0}
                
                label = item['label']
                if label in grouped[date_str]:
                    grouped[date_str][label] += 1
                grouped[date_str]["total"] += 1
            
            return sorted(grouped.values(), key=lambda x: x['date'])
        except Exception as e:
            print(f"Error fetching chart: {e}")
            return []
