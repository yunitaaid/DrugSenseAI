import streamlit as st
import requests
import json

# =========================================================
# KONFIGURASI
# =========================================================
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/drug-analysis"

st.set_page_config(
    page_title="DrugSense AI",
    page_icon="💊",
    layout="centered"
)

# =========================================================
# HEADER
# =========================================================
st.title("💊 DrugSense AI")
st.write(
    "Agen pencari informasi obat otomatis yang menganalisis efek samping "
    "dan interaksi antar obat menggunakan AI."
)

# =========================================================
# MENU / TAB
# =========================================================
tab1, tab2 = st.tabs(["🔍 Analisis Obat", "📊 Evaluasi RAG (MRR)"])

# =========================================================
# TAB 1: ANALISIS OBAT
# =========================================================
with tab1:
    st.subheader("🔍 Analisis Informasi Obat")

    nama_obat = st.text_input(
        "Masukkan nama obat:",
        placeholder="contoh: Actos"
    )

    if st.button("🔍 Analisis Obat"):
        if not nama_obat.strip():
            st.warning("Masukkan nama obat terlebih dahulu!")
        else:
            with st.spinner("Sedang memproses analisis obat..."):
                try:
                    payload = {
                        "nama_obat": nama_obat.strip()
                    }

                    response = requests.post(
                        N8N_WEBHOOK_URL,
                        headers={"Content-Type": "application/json"},
                        json=payload,
                        timeout=2000
                    )

                    if response.status_code == 200:
                        try:
                            data = response.json()
                            st.success("✅ Analisis selesai!")

                            st.subheader("📋 Hasil Analisis Obat")
                            st.markdown(
                                f"**Analisis AI (Gemini):**\n\n"
                                f"{data.get('analisis_ai', 'Tidak ada hasil analisis')}"
                            )
                        except json.JSONDecodeError:
                            st.error("❌ Gagal memproses respons AI")
                            st.text(response.text)
                    else:
                        st.error(f"❌ Gagal: Status {response.status_code}")
                        st.text(response.text)

                except requests.exceptions.ConnectionError:
                    st.error(
                        "⚠️ Tidak dapat terhubung ke server n8n. "
                        "Pastikan n8n berjalan di http://localhost:5678"
                    )
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

# =========================================================
# TAB 2: EVALUASI RAG - MRR
# =========================================================
with tab2:
    st.subheader("📊 Evaluasi Retrieval dengan Mean Reciprocal Rank (MRR)")

    st.markdown(
        """
        **Mean Reciprocal Rank (MRR)** digunakan untuk mengukur seberapa cepat
        dokumen relevan pertama muncul pada hasil retrieval sistem RAG.
        """
    )

    # Tombol untuk menghitung MRR
    if st.button("📐 Hitung Nilai MRR"):
        # Data rank hasil pengujian
        ranks = [1, 1, 1, 1, 1, 1, 1, 1, 1, 3]

        reciprocal_ranks = [1 / r for r in ranks]
        mrr_value = sum(reciprocal_ranks) / len(reciprocal_ranks)

        st.success("✅ Perhitungan MRR berhasil")

        st.metric(
            label="Nilai Mean Reciprocal Rank (MRR)",
            value=f"{mrr_value:.3f}"
        )

        st.info(
            "Nilai MRR mendekati 1 menunjukkan bahwa sistem RAG DrugSense AI "
            "mampu menempatkan dokumen relevan pada peringkat teratas."
        )
