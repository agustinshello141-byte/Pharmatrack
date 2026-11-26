import pandas as pd
import streamlit as st

st.set_page_config(page_title="PharmaTrack", layout="wide")
st.title("💊 PharmaTrack - Sistem Pemantauan Stok Obat")

if "obat_df" not in st.session_state:
  st.session_state.obat_df = pd.DataFrame([
      {
          "Kode Obat": "OBT001",
          "Nama Obat": "Paracetamol 500 mg",
          "Satuan": "Tablet",
          "Stok Awal": 100,
          "Masuk": 50,
          "Keluar": 138,
          "Min Stok": 20,
      },
      {
          "Kode Obat": "OBT002",
          "Nama Obat": "Amoxicillin 500 mg",
          "Satuan": "Kapsul",
          "Stok Awal": 80,
          "Masuk": 40,
          "Keluar": 65,
          "Min Stok": 20,
      },
      {
          "Kode Obat": "OBT003",
          "Nama Obat": "Antasida DOEN",
          "Satuan": "Tablet",
          "Stok Awal": 60,
          "Masuk": 20,
          "Keluar": 70,
          "Min Stok": 15,
      },
      {
          "Kode Obat": "OBT004",
          "Nama Obat": "Cetirizine 10 mg",
          "Satuan": "Tablet",
          "Stok Awal": 50,
          "Masuk": 0,
          "Keluar": 32,
          "Min Stok": 15,
      },
      {
          "Kode Obat": "OBT005",
          "Nama Obat": "Ibuprofen 400 mg",
          "Satuan": "Tablet",
          "Stok Awal": 75,
          "Masuk": 25,
          "Keluar": 88,
          "Min Stok": 15,
      },
      {
          "Kode Obat": "OBT006",
          "Nama Obat": "Omeprazole 20 mg",
          "Satuan": "Kapsul",
          "Stok Awal": 40,
          "Masuk": 30,
          "Keluar": 25,
          "Min Stok": 15,
      },
      {
          "Kode Obat": "OBT007",
          "Nama Obat": "Metformin 500 mg",
          "Satuan": "Tablet",
          "Stok Awal": 90,
          "Masuk": 0,
          "Keluar": 45,
          "Min Stok": 25,
      },
      {
          "Kode Obat": "OBT008",
          "Nama Obat": "Amlodipine 5 mg",
          "Satuan": "Tablet",
          "Stok Awal": 100,
          "Masuk": 50,
          "Keluar": 132,
          "Min Stok": 25,
      },
      {
          "Kode Obat": "OBT009",
          "Nama Obat": "Salbutamol 2 mg",
          "Satuan": "Tablet",
          "Stok Awal": 45,
          "Masuk": 15,
          "Keluar": 20,
          "Min Stok": 15,
      },
      {
          "Kode Obat": "OBT010",
          "Nama Obat": "Dexamethasone 0,5 mg",
          "Satuan": "Tablet",
          "Stok Awal": 60,
          "Masuk": 30,
          "Keluar": 78,
          "Min Stok": 15,
      },
  ])

df = st.session_state.obat_df.copy()
df["Stok Akhir"] = df["Stok Awal"] + df["Masuk"] - df["Keluar"]
df["Status"] = df.apply(
    lambda r: (
        "⚠️ Stok Menipis" if r["Stok Akhir"] < r["Min Stok"] else "✅ Aman"
    ),
    axis=1,
)

menipis = df[df["Stok Akhir"] < df["Min Stok"]]
if not menipis.empty:
  daftar_obat = ", ".join(
      [f"{row['Nama Obat']} ({row['Stok Akhir']})" for _, row in menipis.iterrows()]
  )
  st.warning(f"⚠️ Peringatan Stok Menipis: {daftar_obat}")

col1, col2 = st.columns(2)
daftar_nama = st.session_state.obat_df["Nama Obat"].tolist()

with col1:
  st.subheader("Form Obat Masuk")
  with st.form("form_masuk"):
    tgl_masuk = st.date_input("Tanggal Masuk")
    obat_masuk = st.selectbox("Nama Obat", daftar_nama, key="in_obat")
    jml_masuk = st.number_input("Jumlah Masuk", min_value=1, step=1)
    pemasok = st.text_input("Sumber Pemasok")
    submit_masuk = st.form_submit_button("Simpan Obat Masuk")
    if submit_masuk:
      idx = st.session_state.obat_df.index[
          st.session_state.obat_df["Nama Obat"] == obat_masuk
      ][0]
      st.session_state.obat_df.loc[idx, "Masuk"] += jml_masuk
      st.success(
          f"Tercatat +{jml_masuk} {obat_masuk} ({tgl_masuk}, {pemasok})"
      )
      st.rerun()

with col2:
  st.subheader("Form Obat Keluar")
  with st.form("form_keluar"):
    tgl_keluar = st.date_input("Tanggal Keluar")
    obat_keluar = st.selectbox("Nama Obat", daftar_nama, key="out_obat")
    jml_keluar = st.number_input("Jumlah Keluar", min_value=1, step=1)
    ket = st.text_input("Keterangan Penggunaan")
    submit_keluar = st.form_submit_button("Simpan Obat Keluar")
    if submit_keluar:
      idx = st.session_state.obat_df.index[
          st.session_state.obat_df["Nama Obat"] == obat_keluar
      ][0]
      stok_sekarang = (
          st.session_state.obat_df.loc[idx, "Stok Awal"]
          + st.session_state.obat_df.loc[idx, "Masuk"]
          - st.session_state.obat_df.loc[idx, "Keluar"]
      )
      if jml_keluar > stok_sekarang:
        st.error("Jumlah keluar melebihi stok tersedia!")
      else:
        st.session_state.obat_df.loc[idx, "Keluar"] += jml_keluar
        st.success(f"Tercatat -{jml_keluar} {obat_keluar} ({tgl_keluar}, {ket})")
        st.rerun()

st.subheader("Dashboard Data Obat")
st.dataframe(
    df[[
        "Kode Obat",
        "Nama Obat",
        "Satuan",
        "Stok Awal",
        "Masuk",
        "Keluar",
        "Stok Akhir",
        "Min Stok",
        "Status",
    ]],
    use_container_width=True,
)
