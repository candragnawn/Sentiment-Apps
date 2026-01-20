import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# 1. Konfigurasi Halaman & Styling
st.set_page_config(page_title="Sentimen AI Pro", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    conn = sqlite3.connect('sentiments.db')
    df = pd.read_sql_query("SELECT * FROM sentiments", conn)
    conn.close()
    return df

# 2. SIDEBAR - Search & Filter
st.sidebar.title("Control Panel")
keyword_search = st.sidebar.text_input("Cari Keyword (Misal: Raditya Dika)", "")
sort_order = st.sidebar.selectbox("Urutkan Tanggal", ["Terbaru", "Terlama"])

try:
    df = load_data()
    
    # Filtering Data Berdasarkan Search Bar
    if keyword_search:
        df_display = df[df['judul'].str.contains(keyword_search, case=False)]
        title_text = f"Analisis Sentimen: {keyword_search}"
    else:
        df_display = df
        title_text = "Dashboard Analisis Sentimen Global"

    # 3. HEADER
    st.title(f"{title_text}")
    st.info(f"Ditemukan {len(df_display)} berita yang relevan di database.")

    if not df_display.empty:
        # 4. METRICS ROW
        col1, col2, col3, col4 = st.columns(4)
        
        pos_pct = len(df_display[df_display['label'] == 'positive'])
        neg_pct = len(df_display[df_display['label'] == 'negative'])
        avg_score = df_display['score'].mean()

        col1.metric("Total Berita", len(df_display))
        col2.metric("Positif ", f"{pos_pct}")
        col3.metric("Negatif ", f"{neg_pct}")
        col4.metric("Avg Confidence", f"{avg_score:.1f}%")

        st.divider()

        # 5. GRAPHIC SECTION
        c1, c2 = st.columns([1, 1.5]) # Kolom 2 lebih lebar untuk tabel

        with c1:
            st.subheader("Persentase Sentimen")
            fig = px.pie(df_display, names='label', hole=0.8,
                         color='label',
                         color_discrete_map={'positive':'#00EAAB', 'negative':'#BA1C00', 'neutral':'#636EFA'})
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("Daftar Berita Terkait")
            # Sortir data
            order = False if sort_order == "Terbaru" else True
            df_display = df_display.sort_values(by='tanggal', ascending=order)
            
            # Styling Tabel
            st.dataframe(df_display[['tanggal', 'judul', 'label', 'score']], 
                         use_container_width=True, height=400)

        # 6. DOWNLOAD FEATURE
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Hasil Analisis (CSV)", csv, "sentimen_report.csv", "text/csv")

    else:
        st.warning("Tidak ada data ditemukan untuk keyword tersebut. Coba jalankan main.py dengan keyword baru!")

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")