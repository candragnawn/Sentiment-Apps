from backend.src.database.database_supabase import SentimentDatabase
import sys
import os

# Add backend/src to path for imports
sys.path.append(os.path.join(os.getcwd(), 'backend', 'src'))

def reset():
    print("🧹 Menghapus semua data di database Supabase...", flush=True)
    db = SentimentDatabase()
    try:
        db.hapus_semua_data()
        print("✅ Database berhasil dikosongkan!", flush=True)
    except Exception as e:
        print(f"❌ Gagal menghapus data: {e}", flush=True)

if __name__ == "__main__":
    reset()
