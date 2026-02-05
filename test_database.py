
import sys
sys.path.append('backend/src')

from database.database_supabase import SentimentDatabase
from datetime import datetime, timedelta

def test_database_connection():
    """Test koneksi ke Supabase"""
    print("=" * 60)
    print("TEST 1: Koneksi Database")
    print("=" * 60)
    
    try:
        db = SentimentDatabase()
        print(" Koneksi ke Supabase berhasil!")
        return db
    except Exception as e:
        print(f" Gagal koneksi ke Supabase: {e}")
        return None

def test_fetch_all_data(db):
    """Test fetch semua data"""
    print("\n" + "=" * 60)
    print("TEST 2: Fetch All Data")
    print("=" * 60)
    
    try:
        data = db.fetch_all_data()
        print(f" Berhasil fetch {len(data)} data dari database")
        
        if len(data) > 0:
            print(f"\nContoh data pertama:")
            first_item = data[0]
            for key, value in first_item.items():
                print(f"  - {key}: {value}")
        else:
            print("  Database masih kosong. Lakukan scraping terlebih dahulu.")
        
        return len(data) > 0
    except Exception as e:
        print(f" Error: {e}")
        return False

def test_fetch_7_days(db):
    """Test fetch data 7 hari terakhir"""
    print("\n" + "=" * 60)
    print("TEST 3: Fetch Data 7 Hari Terakhir")
    print("=" * 60)
    
    try:
        data = db.fetch_last_7_days()
        print(f"Berhasil fetch {len(data)} data dari 7 hari terakhir")
        return True
    except Exception as e:
        print(f" Error: {e}")
        print(f" Kemungkinan kolom 'created_at' belum ada di database.")
        print(f"   Jalankan SQL migration script terlebih dahulu!")
        return False

def test_fetch_1_month(db):
    """Test fetch data 1 bulan terakhir"""
    print("\n" + "=" * 60)
    print("TEST 4: Fetch Data 1 Bulan Terakhir")
    print("=" * 60)
    
    try:
        data = db.fetch_last_month()
        print(f" Berhasil fetch {len(data)} data dari 1 bulan terakhir")
        return True
    except Exception as e:
        print(f" Error: {e}")
        return False

def test_fetch_1_year(db):
    """Test fetch data 1 tahun terakhir"""
    print("\n" + "=" * 60)
    print("TEST 5: Fetch Data 1 Tahun Terakhir")
    print("=" * 60)
    
    try:
        data = db.fetch_last_year()
        print(f"Berhasil fetch {len(data)} data dari 1 tahun terakhir")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_fetch_paginated(db):
    """Test fetch data dengan paginasi"""
    print("\n" + "=" * 60)
    print("TEST 6: Fetch Data dengan Paginasi")
    print("=" * 60)
    
    try:
        result = db.fetch_paginated(page=1, page_size=10)
        print(f" Berhasil fetch data dengan paginasi")
        print(f"   - Total data: {result['total']}")
        print(f"   - Data di halaman ini: {len(result['data'])}")
        print(f"   - Total halaman: {result['total_pages']}")
        print(f"   - Halaman saat ini: {result['page']}")
        return True
    except Exception as e:
        print(f" Error: {e}")
        return False

def test_fetch_by_keyword(db):
    """Test fetch data dengan filter keyword"""
    print("\n" + "=" * 60)
    print("TEST 7: Fetch Data dengan Filter Keyword")
    print("=" * 60)
    
    # Ambil keyword dari data yang ada
    all_data = db.fetch_all_data()
    if len(all_data) == 0:
        print("  Tidak ada data untuk di-test")
        return False
    
    keyword = all_data[0].get('keyword', 'test')
    
    try:
        data = db.fetch_last_7_days(keyword=keyword)
        print(f" Berhasil fetch {len(data)} data dengan keyword '{keyword}'")
        return True
    except Exception as e:
        print(f" Error: {e}")
        return False

def main():
    """Main test function"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "DATABASE METHOD TESTING SCRIPT" + " " * 17 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Test 1: Koneksi
    db = test_database_connection()
    if not db:
        print("\n Testing dihentikan karena koneksi gagal")
        return
    
    # Test 2: Fetch all data
    has_data = test_fetch_all_data(db)
    
    # Test 3-7: Method baru (hanya jika ada data)
    if has_data:
        test_fetch_7_days(db)
        test_fetch_1_month(db)
        test_fetch_1_year(db)
        test_fetch_paginated(db)
        test_fetch_by_keyword(db)
    else:
        print("\n  Beberapa test dilewati karena database kosong")
        print("   Lakukan scraping terlebih dahulu untuk test lengkap")
    
    # Summary
    print("\n" + "=" * 60)
    print("TESTING SELESAI")
    print("=" * 60)
    print("\n CATATAN:")
    print("   - Jika ada error 'created_at', jalankan SQL migration script")
    print("   - SQL script ada di: supabase_migration.sql")
    print("   - Copy-paste ke Supabase SQL Editor dan jalankan")
    print("\n")

if __name__ == "__main__":
    main()
