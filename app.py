import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Verilerin kaydedileceği dosya
CSV_FILE = "kahin_verileri.csv"

def veri_yukle():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Tarih", "Vize", "Calisma_Saati", "Kafein", "Koltuk", "Tahmini_Final"])

def veri_kaydet(df):
    df.to_csv(CSV_FILE, index=False)

st.set_page_config(page_title="Başarı Kahini", page_icon="🔮")

# Sayfalar arası geçişi sağlamak için bilgisayara "Hangi ekrandayız?" bilgisini tutturuyoruz
if 'asama' not in st.session_state:
    st.session_state.asama = 1

def asama_atla():
    st.session_state.asama = 2

# --- 1. EKRAN: KARŞILAMA VE DERS TUTMA ---
if st.session_state.asama == 1:
    st.title("🔮 Başarı Kahini'ne Hoş Geldin")
    st.write("")
    st.markdown("### 🧠 Şimdi aklından seni en çok zorlayan o dersi tut...")
    st.write("Dersi aklında tuttuğunda aşağıdaki butona bas, sana o dersten geçip geçemeyeceğini söyleyeceğim!")
    st.write("")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.button("✨ Tuttum, Hadi Başlayalım! ✨", on_click=asama_atla, use_container_width=True)
    
    st.divider()
    df = veri_yukle()
    kisi_sayisi = len(df)
    st.info(f"🔥 Şu ana kadar **{kisi_sayisi}** kişi kahine danıştı!")

# --- 2. EKRAN: VERİ GİRİŞİ VE SONUÇ ---
elif st.session_state.asama == 2:
    st.title("🔮 Hazır mısın ? ")
    st.markdown("*Not: Burada girdiğin veriler, bölümümüzün bir sonraki **Makine Öğrenmesi (AI)** modelini eğitmek için anonim olarak kullanılacaktır.*")
    
    st.subheader("O dersle ilgili durumun nedir?")
    vize = st.number_input("Aklındaki o dersin Vize Notu (0-100)", min_value=0, max_value=100, value=50)
    saat = st.slider("Haftalık Genel Çalışma Saatin", min_value=0, max_value=40, value=5)
    kahve = st.selectbox("Kampüste Günlük Kafein Dozun?", ["0-2 Bardak (Sakin)", "3-5 Bardak (Bağımlı)", "10+ Bardak (Ellerim Titriyor)"])
    koltuk = st.selectbox("Derste Genelde Neredesin?", ["En Ön (Notlar benden sorulur)", "Orta Sıra (Göze batmayayım)", "En Arka (Uyku modundayım)"])

    if st.button("Kaderimi Göster!", use_container_width=True):
        if "Sakin" in kahve: k_carpan = 1.0
        elif "Bağımlı" in kahve: k_carpan = 1.1
        else: k_carpan = 0.9
        
        if "En Ön" in koltuk: klt_carpan = 1.15
        elif "Orta" in koltuk: klt_carpan = 1.0
        else: klt_carpan = 0.85

        taban_final = vize * 0.85
        calisma_bonus = saat * 1.5
        sonuc = (taban_final + calisma_bonus) * k_carpan * klt_carpan
        sonuc = min(100, max(0, round(sonuc)))

        yeni_veri = {
            "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Vize": vize,
            "Calisma_Saati": saat,
            "Kafein": kahve,
            "Koltuk": koltuk,
            "Tahmini_Final": sonuc
        }
        df = veri_yukle()
        yeni_df = pd.DataFrame([yeni_veri])
        df = pd.concat([df, yeni_df], ignore_index=True)
        veri_kaydet(df)

        st.divider()
        st.header(f"🎯 Aklındaki O Ders İçin Tahmini Final Notun: {sonuc}")
        
        if sonuc >= 60:
            st.success("Kahin diyor ki: GEÇİYORSUN! Algoritmamız o dersteki potansiyelini gördü.")
            st.balloons()
        else:
            st.error("Kahin diyor ki: RİSKLİ BÖLGE! Durum kritik, acilen kahveyi artırıp en ön sıraya geçmen lazım!")