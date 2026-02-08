import os
import dateparser
from supabase import create_client, client
from datetime import datetime, timedelta

class SentimentDatabase:
    def __init__(self):
        url: str = "https://fbkfqsqqkxobmdefokjz.supabase.co"
        key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZia2Zxc3Fxa3hvYm1kZWZva2p6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODkyMjg2MywiZXhwIjoyMDg0NDk4ODYzfQ.5tdJc8WIqnt9F9kPUrQEIiKQmszAlzs1OVQtFROxFiM"
        self.supabase: client = create_client(url, key)

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

    def save_results(self, data_dict):
        try:
            chunk_size = 100
            for i in range(0, len(data_dict), chunk_size):
                chunk = data_dict[i:i + chunk_size]
                self.supabase.table('sentiments').insert(chunk).execute()
            return True
        except Exception as e:
            print(f"Error saving to supabase: {e}")
            return False
    
    def hapus_semua_data(self):
        try:
            self.supabase.table('sentiments').delete().neq('id', 0).execute()
        except Exception as e:
            print(f"Error deleting from supabase: {e}")

    def fetch_all_data(self, keyword=None):
        try:
            query = self.supabase.table('sentiments').select("*")
            if keyword:
                query = query.eq('keyword', keyword)
            response = query.execute()
            return response.data
        except Exception as e:
            print(f"Error fetching all data: {e}")
            return []
    
    def fetch_data_by_date_range(self, start_date, end_date, keyword=None):
        try:
            all_data = []
            page_size = 1000
            offset = 0
            
            while True:
                query = self.supabase.table('sentiments').select("*")
                query = query.gte('published_date', start_date.isoformat())
                query = query.lte('published_date', end_date.isoformat())
                
                if keyword:
                    query = query.eq('keyword', keyword)
                
                query = query.order('published_date', desc=True)
                query = query.range(offset, offset + page_size - 1)
                
                response = query.execute()
                data = response.data
                
                if not data:
                    break
                    
                all_data.extend(data)
                if len(data) < page_size:
                    break
                
                offset += page_size
                # Safety break at 20k rows
                if offset >= 20000:
                    break
                    
            return all_data
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

    def fetch_platform_stats(self, keyword=None):
        try:
            query = self.supabase.table('sentiments').select('platform')
            if keyword:
                query = query.eq("keyword", keyword)
            
            # Increase limit to handle more data for accurate distribution
            result = query.limit(10000).execute()
            data = result.data
            
            counts = {}
            for item in data:
                # Use lowercase for consistent mapping
                p = item.get('platform', 'unknown').lower()
                counts[p] = counts.get(p, 0) + 1

            formatted_stats = []
            for platform, count in counts.items(): 
                formatted_stats.append({
                    "label": platform, # Keep it lowercase to match chartConfig keys
                    "value": count,
                    "fill": f"var(--color-{platform})"
                })
            return formatted_stats
        except Exception as e:
            print(f"Error fetching platform stats: {e}")
            return []

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
            query = self.supabase.table('sentiments').select("label")
            if keyword:
                query = query.eq('keyword', keyword)
            
            response = query.execute()
            labels = [item['label'].lower() for item in response.data]
            
            return {
                "total": len(labels),
                "positive": labels.count('positive'),
                "negative": labels.count('negative'),
                "neutral": labels.count('neutral')
            }
        except Exception as e:
            print(f"Error fetching stats: {e}")
            return {"total": 0, "positive": 0, "negative": 0, "neutral": 0}

    def fetch_chart_data(self, days=30, keyword=None, group_by='day'):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            data = self.fetch_data_by_date_range(start_date, end_date, keyword)
            
            grouped = {}
         
            curr = start_date
            while curr <= end_date:
                if group_by == 'month':
                    date_str = curr.strftime('%Y-%m')
                elif group_by == 'year':
                    date_str = curr.strftime('%Y')
                else:
                    date_str = curr.strftime('%Y-%m-%d')
                
                if date_str not in grouped:
                    grouped[date_str] = {"date": date_str, "positive": 0, "negative": 0, "neutral": 0, "total": 0}
                
                if group_by == 'month':
                 
                    next_month = curr.month % 12 + 1
                    next_year = curr.year + (curr.month // 12)
                    curr = curr.replace(year=next_year, month=next_month, day=1)
                elif group_by == 'year':
                    curr = curr.replace(year=curr.year + 1, month=1, day=1)
                else:
                    curr += timedelta(days=1)

            for item in data:
            # Prioritize published_date for the chart's timeline
                raw_date = item.get('published_date') or item.get('created_at')
                date_obj = None
                if raw_date:
                    try:
                        date_obj = dateparser.parse(str(raw_date))
                    except:
                        pass
                
                if not date_obj:
                    # If parsing fails, skip or use created_at if available
                    continue
                
                if group_by == 'month':
                    date_str = date_obj.strftime('%Y-%m')
                elif group_by == 'year':
                    date_str = date_obj.strftime('%Y')
                else: 
                    date_str = date_obj.strftime('%Y-%m-%d')

                if date_str in grouped:
                    label = item.get('label', '').lower()
                    if label in grouped[date_str]:
                        grouped[date_str][label] += 1
                    grouped[date_str]["total"] += 1
            
            return sorted(grouped.values(), key=lambda x: x['date'])
        except Exception as e:
            print(f"Error fetching chart: {e}")
            return []