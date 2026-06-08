import streamlit as st
from datetime import date


# =====================================
# NODE
# =====================================

class Node:
    def __init__(
        self,
        nama,
        email,
        telepon,
        ktp,
        tanggal_lahir,
        kategori,
        harga,
        jumlah,
        total,
        pembayaran
    ):
        self.nama = nama
        self.email = email
        self.telepon = telepon
        self.ktp = ktp
        self.tanggal_lahir = tanggal_lahir
        self.kategori = kategori
        self.harga = harga
        self.jumlah = jumlah
        self.total = total
        self.pembayaran = pembayaran
        self.next = None


# =====================================
# LINKED LIST
# =====================================

class LinkedList:
    def __init__(self):
        self.head = None

    # Tambah Data
    def tambah(
        self,
        nama,
        email,
        telepon,
        ktp,
        tanggal_lahir,
        kategori,
        harga,
        jumlah,
        total,
        pembayaran
    ):

        node_baru = Node(
            nama,
            email,
            telepon,
            ktp,
            tanggal_lahir,
            kategori,
            harga,
            jumlah,
            total,
            pembayaran
        )

        if self.head is None:
            self.head = node_baru
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node_baru

    # Tampilkan Data
    def tampilkan(self):
        data = []
        current = self.head
        while current:
            data.append({
                "Nama": current.nama,
                "Email": current.email,
                "No Telepon": current.telepon,
                "No KTP": current.ktp,
                "Tanggal Lahir": str(current.tanggal_lahir),
                "Kategori": current.kategori,
                "Harga Tiket": f"Rp {current.harga:,}",
                "Jumlah Tiket": current.jumlah,
                "Total Harga": f"Rp {current.total:,}",
                "Metode Pembayaran": current.pembayaran
            })
            current = current.next
        return data

    # Cari Data berdasarkan Nama
    def cari(self, nama):
        current = self.head
        while current:
            if current.nama.lower() == nama.lower():
                return current
            current = current.next
        return None
    
    # Cetak Tiket by KTP
    def cari_ktp(self, ktp):
        current = self.head
        while current:
            if current.ktp == ktp:
                return current
            current = current.next
        return None

    # Hapus Data
    def hapus(self, nama):
        current = self.head
        prev = None
        while current:
            if current.nama.lower() == nama.lower():
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                return True
            prev = current
            current = current.next
        return False


# =====================================
# SESSION STATE
# =====================================

if "tiket" not in st.session_state:
    st.session_state.tiket = LinkedList()

if "pesan_hapus" not in st.session_state:
    st.session_state.pesan_hapus = ""


# =====================================
# HARGA TIKET
# =====================================

harga_tiket = {
    "VIP": 8000000,
    "CAT 1": 4500000,
    "CAT 2": 3000000,
    "CAT 3": 2000000
}


# =====================================
# HEADER
# =====================================

st.title("🎤 Tiket Konser Justin Bieber")
st.write("Sistem Pemesanan Tiket Konser Justin Bieber Menggunakan Linked List")

# =====================================
# DAFTAR HARGA
# =====================================

st.subheader("🎫 Daftar Harga Tiket")
col1, col2, col3, col4 = st.columns(4)
col1.metric("VIP", "Rp 8.000.000")
col2.metric("CAT 1", "Rp 4.500.000")
col3.metric("CAT 2", "Rp 3.000.000")
col4.metric("CAT 3", "Rp 2.000.000")

st.divider()

# =====================================
# FORM PEMESANAN (REAKTIF / NON-FORM CONTAINER)
# =====================================

st.subheader("📝 Form Pemesanan Tiket")

# Menggunakan input biasa agar perhitungan Harga & Total langsung berubah (Real-time)
nama = st.text_input("Nama Pemesan", key="input_nama")
email = st.text_input("Alamat Email", key="input_email")
telepon = st.text_input("Nomor Telepon", key="input_telepon")
ktp = st.text_input("Nomor KTP", key="input_ktp")

tanggal_lahir = st.date_input(
    "Tanggal Lahir",
    min_value=date(1980, 1, 1),
    max_value=date(2007, 12, 31),
    value=date(2000, 1, 1)
)

kategori = st.selectbox(
    "Kategori Tiket",
    ["Pilih Kategori Tiket", "VIP", "CAT 1", "CAT 2", "CAT 3"]
)

jumlah = st.number_input(
    "Jumlah Tiket",
    min_value=0,
    max_value=4,
    value=0,
    step=1
)

metode_pembayaran = st.selectbox(
    "Metode Pembayaran",
    ["Pilih Metode Pembayaran", "Debit", "QRIS", "GoPay", "DANA"]
)

# Hitung otomatis secara realtime
if kategori == "Pilih Kategori Tiket":
    harga = 0
else:
    harga = harga_tiket[kategori]

total = harga * jumlah

# Tampilkan Ringkasan Harga
st.info(f"**Harga Tiket per Satuan:** Rp {harga:,} | **Total Harga:** Rp {total:,}")

submit = st.button("🚀 Tambah Pemesan & Cetak Tiket")


# =====================================
# PROSES TAMBAH DATA
# =====================================

if submit:
    if (
        nama.strip() == ""
        or email.strip() == ""
        or telepon.strip() == ""
        or ktp.strip() == ""
    ):
        st.warning("⚠️ Lengkapi data terlebih dahulu!")

    elif tanggal_lahir is None:
        st.warning("⚠️ Silakan isi tanggal lahir terlebih dahulu!")

    elif kategori == "Pilih Kategori Tiket":
        st.warning("⚠️ Silakan pilih kategori tiket!")

    elif jumlah == 0:
        st.warning("⚠️ Jumlah tiket harus lebih dari 0!")
    
    elif metode_pembayaran == "Pilih Metode Pembayaran":
        st.warning("⚠️ Silakan pilih metode pembayaran!")

    else:
        # Simpan ke Linked List
        st.session_state.tiket.tambah(
            nama, email, telepon, ktp, tanggal_lahir,
            kategori, harga, jumlah, total, metode_pembayaran
        )

        st.success("✅ Pemesan berhasil ditambahkan & Pembayaran Sukses!")

        # Kode Tiket Otomatis
        kode_tiket = f"JB-{nama[:3].upper()}-{ktp[-4:]}"

        tiket_text = f"""
=====================================
      TIKET KONSER JUSTIN BIEBER
=====================================

Kode Tiket      : {kode_tiket}

Nama            : {nama}
Email           : {email}
No Telepon      : {telepon}
No KTP          : {ktp}
Tanggal Lahir   : {tanggal_lahir}

Kategori Tiket  : {kategori}
Jumlah Tiket    : {jumlah}

Harga Tiket     : Rp {harga:,}
Total Bayar     : Rp {total:,}

Metode Bayar    : {metode_pembayaran}

STATUS          : LUNAS

=====================================
      SELAMAT MENIKMATI KONSER
=====================================
"""
        st.subheader("🎟 Tiket Konser Anda")
        st.code(tiket_text)
        st.download_button(
            label="📥 Download Tiket Ini",
            data=tiket_text,
            file_name=f"{kode_tiket}.txt",
            mime="text/plain"
        )

st.divider()

# =====================================
# DAFTAR PEMESAN
# =====================================

st.subheader("📋 Daftar Pemesan (Database Linked List)")
data = st.session_state.tiket.tampilkan()

if data:
    st.dataframe(data, use_container_width=True) # Menggunakan dataframe agar UI lebih rapi dibanding table kaku
else:
    st.info("Belum ada data pemesan.")

st.divider()

# =====================================
# CARI PEMESAN
# =====================================

st.subheader("🔍 Cari Pemesan")
nama_cari = st.text_input("Masukkan nama pemesan yang dicari")

if st.button("Cari Pemesan"):
    hasil = st.session_state.tiket.cari(nama_cari)
    if hasil:
        st.success("✅ Data ditemukan")
        st.write(f"**Nama :** {hasil.nama}")
        st.write(f"**Email :** {hasil.email}")
        st.write(f"**No KTP :** {hasil.ktp}")
        st.write(f"**Kategori :** {hasil.kategori} ({hasil.jumlah} Tiket)")
        st.write(f"**Total Harga :** Rp {hasil.total:,}")
        st.write(f"**Metode Pembayaran :** {hasil.pembayaran}")
    else:
        st.error("❌ Data tidak ditemukan")

st.divider()

# =====================================
# CETAK ULANG TIKET
# =====================================

st.subheader("🎟 Cetak Ulang Tiket")
ktp_cetak = st.text_input("Masukkan Nomor KTP yang Terdaftar")

if st.button("Cetak Ulang Tiket"):
    data_tiket = st.session_state.tiket.cari_ktp(ktp_cetak)
    if data_tiket:
        kode_tiket = f"JB-{data_tiket.nama[:3].upper()}-{data_tiket.ktp[-4:]}"
        tiket_text = f"""
=====================================
      TIKET KONSER JUSTIN BIEBER
=====================================
Kode Tiket      : {kode_tiket}
Nama            : {data_tiket.nama}
No KTP          : {data_tiket.ktp}
Kategori Tiket  : {data_tiket.kategori}
Jumlah Tiket    : {data_tiket.jumlah}
Total Bayar     : Rp {data_tiket.total:,}
Metode Bayar    : {data_tiket.pembayaran}
STATUS          : LUNAS
=====================================
"""
        st.success("✅ Tiket ditemukan")
        st.code(tiket_text)
        st.download_button(
            label="📥 Download Tiket",
            data=tiket_text,
            file_name=f"{kode_tiket}.txt",
            mime="text/plain"
        )
    else:
        st.error("❌ Nomor KTP tidak terdaftar")

st.divider()

# =====================================
# HAPUS PEMESAN
# =====================================

st.subheader("🗑 Hapus Pemesan")
if st.session_state.pesan_hapus != "":
    st.success(st.session_state.pesan_hapus)
    st.session_state.pesan_hapus = ""

nama_hapus = st.text_input("Masukkan nama pemesan yang akan dihapus")

if st.button("Hapus Pemesan"):
    berhasil = st.session_state.tiket.hapus(nama_hapus)
    if berhasil:
        st.session_state.pesan_hapus = f"✅ Pesanan atas nama '{nama_hapus}' sudah dihapus"
        st.rerun()
    else:
        st.error("❌ Data tidak ditemukan")