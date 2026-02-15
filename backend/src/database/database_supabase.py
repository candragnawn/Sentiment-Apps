import os
import dateparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from functools import lru_cache

class SentimentDatabase:
    
    def __init__(self):
        self.url = "https://fbkfqsqqkxobmdefokjz.supabase.co"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZia2Zxc3Fxa3hvYm1kZWZva2p6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODkyMjg2MywiZXhwIjoyMDg0NDk4ODYzfQ.5tdJc8WIqnt9F9kPUrQEIiKQmszAlzs1OVQtFROxFiM"
        self.base_url = f"{self.url}/rest/v1"
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    def _get(self, endpoint: str, params: dict = None) -> dict:
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            count = response.headers.get('Content-Range', '').split('/')[-1]
            return {
                'data': response.json(),
                'count': int(count) if count and count.isdigit() else None
            }
        except Exception as e:
            print(f"GET Error: {e}")
            return {'data': [], 'count': 0}

    def _post(self, endpoint: str, data: list) -> bool:
        try:
            response = requests.post(f"{self.base_url}/{endpoint}", headers=self.headers, json=data, timeout=30)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"POST Error: {e}")
            return False

    def _delete(self, endpoint: str, params: dict = None) -> bool:
        try:
            response = requests.delete(f"{self.base_url}/{endpoint}", headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"DELETE Error: {e}")
            return False

    def check_existing_keyword(self, keyword):
        try:
            result = self._get("sentiments", {"keyword": f"eq.{keyword}", "select": "id", "limit": "1"})
            return len(result['data']) > 0
        except Exception as e:
            print(f"Error checking cache: {e}")
            return False

    def save_results(self, data_dict):
        try:
            chunk_size = 500
            for i in range(0, len(data_dict), chunk_size):
                chunk = data_dict[i:i + chunk_size]
                if not self._post("sentiments", chunk):
                    return False
            return True
        except Exception as e:
            print(f"Error saving to supabase: {e}")
            return False
    
    def hapus_semua_data(self):
        try:
            self._delete("sentiments", {"id": "neq.0"})
        except Exception as e:
            print(f"Error deleting from supabase: {e}")

    def fetch_all_data(self, keyword=None):
        try:
            params = {"select": "*"}
            if keyword:
                params["keyword"] = f"eq.{keyword}"
            result = self._get("sentiments", params)
            return result['data']
        except Exception as e:
            print(f"Error fetching all data: {e}")
            return []
    
    def fetch_data_by_date_range(self, start_date, end_date, keyword=None):
        try:
            all_data = []
            page_size = 1000
            offset = 0
            
            while True:
                params = {
                    "select": "*",
                    "published_date": f"gte.{start_date.isoformat()}",
                    "published_date": f"lte.{end_date.isoformat()}",
                    "order": "published_date.desc",
                    "offset": str(offset),
                    "limit": str(page_size)
                }
                
                if keyword:
                    params["keyword"] = f"eq.{keyword}"
                
                result = self._get("sentiments", params)
                data = result['data']
                
                if not data:
                    break
                    
                all_data.extend(data)
                if len(data) < page_size:
                    break
                
                offset += page_size
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
            params = {"select": "platform", "limit": "10000"}
            if keyword:
                params["keyword"] = f"eq.{keyword}"
            
            result = self._get("sentiments", params)
            data = result['data']
            
            counts = {}
            for item in data:
                p = item.get('platform', 'unknown').lower()
                counts[p] = counts.get(p, 0) + 1

            formatted_stats = []
            for platform, count in counts.items(): 
                formatted_stats.append({
                    "label": platform,
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
            params = {
                "select": "*",
                "order": "created_at.desc",
                "offset": str(offset),
                "limit": str(page_size)
            }
            
            if keyword:
                params["keyword"] = f"eq.{keyword}"
            
            result = self._get("sentiments", params)
            
            count_params = {"select": "id"}
            if keyword:
                count_params["keyword"] = f"eq.{keyword}"
            count_headers = self.headers.copy()
            count_headers["Prefer"] = "count=exact"
            count_response = requests.head(f"{self.base_url}/sentiments", headers=count_headers, params=count_params, timeout=30)
            total = int(count_response.headers.get('Content-Range', '0-0/0').split('/')[-1])
            
            return {
                'data': result['data'],
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
            params = {"select": "label"}
            if keyword:
                params["keyword"] = f"eq.{keyword}"
            
            result = self._get("sentiments", params)
            labels = [item['label'].lower() for item in result['data']]
            
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
                raw_date = item.get('published_date') or item.get('created_at')
                date_obj = None
                if raw_date:
                    try:
                        date_obj = dateparser.parse(str(raw_date))
                    except:
                        pass
                
                if not date_obj:
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

    @lru_cache(maxsize=1)
    def fetch_search_history(self):
        try:
            # Fetch all data to aggregate in Python (Supabase free tier limitation on complex GROUP BY queries via API)
            # For production with many rows, this should be a stored procedure or proper SQL view
            params = {"select": "keyword,label,created_at,platform"}
            result = self._get("sentiments", params)
            data = result['data']
            
            history = {}
            
            for item in data:
                keyword = item.get('keyword')
                if not keyword:
                    continue
                    
                if keyword not in history:
                    history[keyword] = {
                        "keyword": keyword,
                        "total": 0,
                        "positive": 0,
                        "negative": 0,
                        "neutral": 0,
                        "platforms": set(),
                        "last_updated": item.get('created_at')
                    }
                
                # Update counts
                label = item.get('label', '').lower()
                history[keyword]["total"] += 1
                if label in history[keyword]:
                    history[keyword][label] += 1
                
                # Update platform
                if item.get('platform'):
                    history[keyword]["platforms"].add(item.get('platform'))
                
                # Update last_updated if newer
                curr_date = item.get('created_at')
                if curr_date and curr_date > history[keyword]["last_updated"]:
                    history[keyword]["last_updated"] = curr_date

            # Calculate percentages and format output
            output = []
            for k, v in history.items():
                total = v["total"]
                if total > 0:
                    v["positive_pct"] = round((v["positive"] / total) * 100, 1)
                    v["negative_pct"] = round((v["negative"] / total) * 100, 1)
                    v["neutral_pct"] = round((v["neutral"] / total) * 100, 1)
                else:
                    v["positive_pct"] = 0
                    v["negative_pct"] = 0
                    v["neutral_pct"] = 0
                
                v["platforms"] = list(v["platforms"]) # Convert set to list for JSON serialization
                output.append(v)
            
            # Sort by last_updated desc
            return sorted(output, key=lambda x: x['last_updated'], reverse=True)
            
        except Exception as e:
            print(f"Error fetching history: {e}")
    @lru_cache(maxsize=1)
    def fetch_word_cloud(self, keyword=None):
        try:
            params = {"select": "top_keyword", "limit": "2000", "order": "created_at.desc"}
            if keyword:
                params["keyword"] = f"eq.{keyword}"
            
            result = self._get("sentiments", params)
            data = result['data']
            
            word_counts = {}
            for item in data:
                keywords = item.get('top_keyword')
                if keywords and isinstance(keywords, list):
                    for word in keywords:
                        if word:
                            word_counts[word] = word_counts.get(word, 0) + 1
            
            # Format for frontend: { text: string, value: number }
            formatted = [{"text": k, "value": v} for k, v in word_counts.items()]
            
            # Sort by value desc and take top 1000
            return sorted(formatted, key=lambda x: x['value'], reverse=True)[:1000]
        except Exception as e:
            print(f"Error fetching word cloud: {e}")
            return []