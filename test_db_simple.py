import sys
sys.path.append('backend/src')
from database.database_supabase import SentimentDatabase

print("="*60)
print("TEST DATABASE - TAHAP 1")
print("="*60)


print("\n1. Testing koneksi database...")
try:
    db = SentimentDatabase()
    print("   [OK] Koneksi berhasil!")
except Exception as e:
    print(f"   [FAIL] Error: {e}")
    exit(1)

print("\n2. Testing fetch_all_data()...")
try:
    data = db.fetch_all_data()
    print(f"   [OK] Total data: {len(data)} records")
    has_data = len(data) > 0
except Exception as e:
    print(f"   [FAIL] Error: {e}")
    has_data = False


if has_data:
    print("\n3. Testing fetch_last_7_days()...")
    try:
        data = db.fetch_last_7_days()
        print(f"   [OK] Returned {len(data)} records")
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        print("   NOTE: Kolom 'created_at' belum ada!")
        print("   ACTION: Jalankan SQL migration script di Supabase")
    
    print("\n4. Testing fetch_last_month()...")
    try:
        data = db.fetch_last_month()
        print(f"   [OK] Returned {len(data)} records")
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
    
    print("\n5. Testing fetch_last_year()...")
    try:
        data = db.fetch_last_year()
        print(f"   [OK] Returned {len(data)} records")
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
    
    print("\n6. Testing fetch_paginated()...")
    try:
        result = db.fetch_paginated(page=1, page_size=5)
        print(f"   [OK] Page 1: {len(result['data'])} records")
        print(f"        Total: {result['total']} | Pages: {result['total_pages']}")
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
else:
    print("\n[SKIP] Database kosong - lakukan scraping dulu")

print("\n" + "="*60)
print("TESTING SELESAI")
print("="*60)
