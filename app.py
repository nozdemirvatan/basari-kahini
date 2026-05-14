import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

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

# --- HAYALET YÖNETİCİ MENÜSÜ (URL'ye /?admin=fsm yazılırsa açılır) ---
if "admin" in st.query_params and st.query_params["admin"] == "fsm":
    with st.sidebar:
        st.success("🕵️‍♂️ Yönetici Modu Aktif!")
        st.write("Hoş geldiniz. Toplanan verileri aşağıdan yönetebilirsiniz.")
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, "rb") as file:
                st.download_button(label="📥 Tüm Verileri İndir", data=file, file_name="kahin_verileri.csv", mime="text/csv", use_container_width=True)
            
            st.divider()
            if st.button("🗑️ Verileri Sıfırla", use_container_width=True):
                os.remove(CSV_FILE)
                st.success("Tüm veriler silindi! Sayfayı yenileyin.")
        else:
            st.warning("Henüz veri toplanmadı.")

# --- HAFIZA TEMİZLEYİCİ VE BAŞA DÖNME FONKSİYONU ---
def basa_don():
    st.session_state.clear() # Tüm hafızayı (önceki hesaplamaları) siler
    st.session_state.asama = 1

# İlk giriş kontrolü
if 'asama' not in st.session_state:
    st.session_state.asama = 1

def asama_atla():
    st.session_state.asama = 2

# --- 1. EKRAN: KARŞILAMA VE DERS TUTMA ---
if st.session_state.asama == 1:
    st.title("🔮 Başarı Kahini'ne Hoş Geldin")
    st.write("")
    st.markdown("### 🧠 Şimdi aklından seni en çok zorlayan o dersi tut...")
    st.write("Ve aşağıdaki butona bas, sana o dersten geçip geçemeyeceğini söyleyeceğim!")
    st.write("")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.button("✨ Tuttum, Hadi Başlayalım! ✨", on_click=asama_atla, use_container_width=True)
    
    st.divider()
    df = veri_yukle()
    kisi_sayisi = len(df)
    st.info(f"🔥 Şu ana kadar **{kisi_sayisi}** kişi kahine danıştı!")

# --- 2. EKRAN: VERİ GİRİŞİ ---
elif st.session_state.asama == 2:
    st.title("🔮 Hazır mısın?")
    st.markdown("*Not: Burada girdiğin veriler, bölümümüzün bir sonraki **Makine Öğrenmesi (AI)** modelini eğitmek için anonim olarak kullanılacaktır.*")
    
    st.subheader("O dersle ilgili durumun nedir?")
    
    vize = st.number_input("Aklındaki o dersin Vize Notu (0-100)", min_value=0, max_value=100, value=None, placeholder="Buraya tıkla ve notunu klavyeden yaz...", step=1)
    saat = st.slider("Haftalık Genel Çalışma Saatin", min_value=0, max_value=40, value=5)
    kahve = st.selectbox("Kampüste Günlük Kafein Dozun?", ["0-2 Bardak (Sakin)", "3-5 Bardak (Bağımlı)", "10+ Bardak (Ellerim Titriyor)"])
    koltuk = st.selectbox("Derste Genelde Neredesin?", ["En Ön (Notlar benden sorulur)", "Orta Sıra (Göze batmayayım)", "En Arka (Uyku modundayım)"])

    if st.button("Kaderimi Göster!", use_container_width=True):
        if vize is None:
            st.warning("⚠️ Kahin diyor ki: Kaderini görebilmem için önce vize notunu kutucuğa yazmalısın!")
        else:
            # Kullanıcının verilerini hafızaya alıp 3. ekrana yolluyoruz
            st.session_state.vize = vize
            st.session_state.saat = saat
            st.session_state.kahve = kahve
            st.session_state.koltuk = koltuk
            st.session_state.asama = 3
            st.rerun()

# --- 3. EKRAN: SİHİRLİ BEKLEME VE SONUÇ ---
elif st.session_state.asama == 3:
    st.title("🔮 Kahin Gelecekle Bağlantı Kuruyor...")
    st.divider()
    
    # EĞER ANİMASYON HENÜZ YAPILMADIYSA YAP VE KAYDET
    if "animasyon_bitti" not in st.session_state:
        mesaj_kutusu = st.empty()
        
        mesaj_kutusu.info("🧿 Kristal küre ısınıyor...")
        time.sleep(2)
        
        mesaj_kutusu.warning("📜 Kadim algoritmalar hesaplanıyor...")
        time.sleep(2.5)
        
        mesaj_kutusu.error("⚡ O ders için kaderin yazılıyor...")
        time.sleep(2)
        
        mesaj_kutusu.empty() # Ekrandaki bekletme yazılarını temizle
        
        # --- ARKA PLAN HESAPLAMALARI ---
        vize = st.session_state.vize
        saat = st.session_state.saat
        kahve = st.session_state.kahve
        koltuk = st.session_state.koltuk
        
        if "Sakin" in kahve: k_carpan = 1.0
        elif "Bağımlı" in kahve: k_carpan = 1.1
        else: k_carpan = 0.9
        
        if "En Ön" in koltuk: klt_carpan = 1.15
        elif "Orta" in koltuk: klt_carpan = 1.0
        else: klt_carpan = 0.85

        taban_final = vize * 0.85
        calisma_bonus = saat * 1.5
        sonuc = (taban_final + calisma_bonus) * k_carpan * klt_carpan
        st.session_state.final_sonucu = min(100, max(0, round(sonuc)))

        # Veriyi Kaydet
        yeni_veri = {
            "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Vize": vize,
            "Calisma_Saati": saat,
            "Kafein": kahve,
            "Koltuk": koltuk,
            "Tahmini_Final": st.session_state.final_sonucu
        }
        df = veri_yukle()
        yeni_df = pd.DataFrame([yeni_veri])
        df = pd.concat([df, yeni_df], ignore_index=True)
        veri_kaydet(df)

        # Animasyonun bittiğini hafızaya kazı ve sayfayı yenile ki statik sonuca geçsin
        st.session_state.animasyon_bitti = True
        st.rerun()

    # ANİMASYON BİTTİYSE (VEYA DAHA ÖNCE YAPILDIYSA) SADECE SONUCU GÖSTER
    if "animasyon_bitti" in st.session_state:
        sonuc = st.session_state.final_sonucu
        
        st.markdown(f"<h1 style='text-align: center;'>🎯 Tahmini Final Notun: {sonuc}</h1>", unsafe_allow_html=True)
        st.write("")
        
        if sonuc >= 60:
            st.success("✨ Kahin diyor ki: Işık görüyorum! Geçiyorsun... Algoritmamız o dersteki potansiyelini hissetti.")
            st.snow()
        else:
            st.error("🌑 Kahin diyor ki:  Kürem karardı ! Acilen kahveyi artırıp en ön sıraya geçmen lazım!")
        
        
