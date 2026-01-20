import sqlite3
class SentimentDatabase:
    def __init__(self, db_name='sentiments.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
    def hapus_semua_data(self):
        query = "DELETE FROM sentiments"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            print("all data deleted successfully from database")
        except Exception as e:
            print(f"error deleting data: {e}")
            
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS sentiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT,
            label TEXT,
            platform TEXT,
            engagement INTEGER,
            username TEXT,
            score REAL,
            tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        self.conn.execute(query)
        self.conn.commit()
    def save_result(self, judul, label, score, platform):
        query = "INSERT INTO sentiments (judul, label, score, platform) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (judul, label, score, platform))
        self.conn.commit()
        print("data berhasil disimpan ke database")
    
    def ambil_semua(self):
        return self.conn.execute("SELECT * FROM sentiments").fetchall()
    def tutup_koneksi(self):
        self.conn.close()

    
        
