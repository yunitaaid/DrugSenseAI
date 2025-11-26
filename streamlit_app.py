import streamlit as st
import requests
import json

# URL webhook n8n kamu
N8N_WEBHOOK_URL = "https://drugsenseai.app.n8n.cloud/webhook/drug-analysis"
#N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/drug-analysis"


# Konfigurasi halaman Streamlit
st.set_page_config(page_title="DrugSense AI", page_icon="💊", layout="centered")

st.title("💊 DrugSense AI")
st.write("Agen pencari informasi obat otomatis yang menganalisis efek samping dan interaksi antar obat menggunakan AI.")

# Input dari user
nama_obat = st.text_input("Masukkan nama obat:", placeholder="contoh: ibuprofen")
# catatan = st.text_area("Catatan tambahan (opsional):", placeholder="contoh: digunakan untuk sakit kepala")

# Tombol kirim ke n8n
if st.button("🔍 Analisis Obat"):
    if not nama_obat.strip():
        st.warning("Masukkan nama obat terlebih dahulu!")
    else:
        with st.spinner("Sedang memproses hasil analisis..."):
            try:
                # Data yang dikirim ke webhook n8n
                payload = {
                    "nama_obat": nama_obat.strip(),
                #    "catatan": catatan.strip()
                }

                # Kirim request POST ke n8n
                response = requests.post(
                    N8N_WEBHOOK_URL,
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    timeout=30
                )

                # Tangani respons dari n8n
                if response.status_code == 200:
                    try:
                        data = response.json()
                    except json.JSONDecodeError:
                        st.write("🧾 Response :")
                        st.code(response.text, language="json")

                        st.error("❌ Data Obat Tidak Ditemukan di Database FDA")
                        st.text(response.text)
                    else:
                        st.success("✅ Analisis selesai!")

                        st.subheader("📋 Hasil Analisis Obat")
                    #    st.markdown(f"**Nama Obat:** {data.get('obat', 'Tidak diketahui')}")
                    #    st.markdown(f"**Efek Samping:** {data.get('efek_samping', 'Tidak ada data')}")
                    #    st.markdown(f"**Interaksi Obat:** {data.get('interaksi', 'Tidak ada data')}")
                        st.markdown(f"**Analisis AI (Gemini):** {data.get('analisis_ai', 'Belum ada hasil AI')}")

                else:
                    st.error(f"❌ Gagal: Status {response.status_code}")
                    st.text(response.text)

            except requests.exceptions.ConnectionError:
                st.error("⚠️ Tidak dapat terhubung ke server n8n. Pastikan n8n sedang berjalan di localhost:5678.")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
