import streamlit as st
from datetime import date

# =========================
# NODE
# =========================
class Node:
    def __init__(self, nama, ktp, hp, email, tgl_lahir,
                 kategori, harga, jumlah, total, pembayaran):
        self.nama = nama
        self.ktp = ktp
        self.hp = hp
        self.email = email
        self.tgl_lahir = tgl_lahir
        self.kategori = kategori
        self.harga = harga
        self.jumlah = jumlah
        self.total = total
        self.pembayaran = pembayaran
        self.next = None

# =========================
# LINKED LIST
# =========================
class LinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, *data):
        node = Node(*data)
        if self.head is None:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node

    def tampilkan(self):
        data = []
        cur = self.head
        while cur:
            data.append({
                "Nama": cur.nama,
                "No KTP": cur.ktp,
                "No HP": cur.hp,
                "Email": cur.email,
                "Tanggal Lahir": cur.tgl_lahir,
                "Kategori": cur.kategori,
                "Jumlah": cur.jumlah,
                "Total": f"Rp {cur.total:,}"
            })
            cur = cur.next
        return data

    def cari(self, nama):
        cur = self.head
        while cur:
            if cur.nama.lower() == nama.lower():
                return cur
            cur = cur.next
        return None

    def hapus(self, nama):
        cur = self.head
        prev = None
        while cur:
            if cur.nama.lower() == nama.lower():
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                return True
            prev = cur
            cur = cur.next
        return False

if "tiket" not in st.session_state:
    st.session_state.tiket = LinkedList()

harga_tiket = {
    "VIP": 8000000,
    "CAT 1": 4500000,
    "CAT 2": 3000000,
    "CAT 3": 2000000
}

st.title("🎤 Tiket Konser Justin Bieber")
st.subheader("12 Desember 2026")

st.info("""
VIP : Rp 8.000.000
CAT 1 : Rp 4.500.000
CAT 2 : Rp 3.000.000
CAT 3 : Rp 2.000.000
""")

with st.form("form", clear_on_submit=True):
    nama = st.text_input("Nama")
    ktp = st.text_input("No KTP")
    hp = st.text_input("No HP")
    email = st.text_input("Alamat Email")

    tgl_lahir = st.date_input(
        "Tanggal Lahir",
        min_value=date(1900,1,1),
        max_value=date(2008,12,31),
        value=date(2000,1,1)
    )

    kategori = st.selectbox(
        "Kategori Tiket",
        ["Pilih","VIP","CAT 1","CAT 2","CAT 3"]
    )

    jumlah = st.number_input(
        "Jumlah Tiket",
        min_value=0,
        max_value=10,
        value=0
    )

    pembayaran = st.selectbox(
        "Metode Pembayaran",
        ["Pilih","Transfer Bank","QRIS","DANA","GoPay"]
    )

    harga = 0 if kategori == "Pilih" else harga_tiket[kategori]
    total = harga * jumlah

    st.write(f"Harga Tiket : Rp {harga:,}")
    st.write(f"Total Harga : Rp {total:,}")

    submit = st.form_submit_button("Tambah Pemesanan")

if submit:
    if not nama or not ktp or not hp or not email:
        st.warning("Lengkapi data terlebih dahulu.")
    elif kategori == "Pilih":
        st.warning("Pilih kategori tiket.")
    elif pembayaran == "Pilih":
        st.warning("Pilih metode pembayaran.")
    elif jumlah <= 0:
        st.warning("Jumlah tiket harus lebih dari 0.")
    else:
        st.session_state.tiket.tambah(
            nama, ktp, hp, email, tgl_lahir,
            kategori, harga, jumlah, total, pembayaran
        )

        kode = f"JB-{nama[:3].upper()}-{ktp[-4:]}"
        tiket = f"""
TIKET KONSER JUSTIN BIEBER
Tanggal Konser : 12 Desember 2026
Kode Tiket : {kode}

Nama : {nama}
Kategori : {kategori}
Jumlah Tiket : {jumlah}
Total Bayar : Rp {total:,}

Penukaran Tiket:
12 Desember 2026 (H-0)
3 Jam Sebelum Konser Dimulai
"""
        st.success("Pemesanan berhasil.")
        st.download_button(
            "📥 Download Tiket",
            tiket,
            file_name=f"{kode}.txt",
            mime="text/plain"
        )

st.subheader("📋 Daftar Pemesan")
data = st.session_state.tiket.tampilkan()
if data:
    st.table(data)
else:
    st.info("Belum ada data pemesan.")

st.subheader("🔍 Cari Pemesan")
cari = st.text_input("Nama Pemesan")
if st.button("Cari"):
    hasil = st.session_state.tiket.cari(cari)
    if hasil:
        st.success("✅ Data Ditemukan")

    st.table([
        {
            "Nama": hasil.nama,
            "No KTP": hasil.ktp,
            "No HP": hasil.hp,
            "Email": hasil.email,
            "Tanggal Lahir": hasil.tgl_lahir,
            "Kategori": hasil.kategori,
            "Harga Tiket": f"Rp {hasil.harga:,}",
            "Jumlah Tiket": hasil.jumlah,
            "Total Bayar": f"Rp {hasil.total:,}",
            "Metode Pembayaran": hasil.pembayaran
        }
    ])
else:
    st.error("❌ Data tidak ditemukan")

    st.subheader("🗑 Hapus / Retur Pembelian")
hapus = st.text_input("Nama yang akan dihapus")
if st.button("Hapus Pemesanan"):
    if st.session_state.tiket.hapus(hapus):
        st.success("Pemesanan berhasil dihapus")
        st.rerun()
    else:
        st.error("Data tidak ditemukan")
