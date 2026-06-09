import streamlit as st
import smtplib
from email.mime.text import MIMEText
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
                "Tanggal Lahir": current.tanggal_lahir,
                "Kategori": current.kategori,
                "Harga Tiket": f"Rp {current.harga:,}",
                "Jumlah Tiket": current.jumlah,
                "Total Harga": f"Rp {current.total:,}",
                "Metode Pembayaran": current.pembayaran
            })

            current = current.next

        return data
    
    def kirim_email(penerima, isi_tiket):

        pengirim = "emailanda@gmail.com"
        password = "password_aplikasi_gmail"

        msg = MIMEText(isi_tiket)
        msg["Subject"] = "E-Ticket Konser Justin Bieber"
        msg["From"] = pengirim
        msg["To"] = penerima

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(pengirim, password)
            server.send_message(msg)
            server.quit()

            return True

        except Exception as e:
            st.error(f"Gagal mengirim email: {e}")
            return False

    # Cari Data
    def cari(self, nama):

        current = self.head

        while current:

            if current.nama.lower() == nama.lower():
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

st.write(
    "Sistem Pemesanan Tiket Konser Justin Bieber Menggunakan Linked List"
)


# =====================================
# DAFTAR HARGA
# =====================================

st.subheader("🎫 Daftar Harga Tiket")

st.info("""
VIP    : Rp 8.000.000

CAT 1  : Rp 4.500.000

CAT 2  : Rp 3.000.000

CAT 3  : Rp 2.000.000
""")


# =====================================
# FORM PEMESANAN
# =====================================

# =====================================
# FORM PEMESANAN
# =====================================

st.subheader("📝 Form Pemesanan Tiket")

with st.form("form_pemesanan", clear_on_submit=True):

    nama = st.text_input("Nama Pemesan")

    email = st.text_input("Alamat Email")

    telepon = st.text_input("Nomor Telepon")

    ktp = st.text_input("Nomor KTP")

    tanggal_lahir = st.date_input(
    "Tanggal Lahir",
    min_value=date(0, 1, 1),
    max_value=date(2008, 12, 31),
    value=date(0, 1, 1)

)

    # Kategori awal kosong
    kategori = st.selectbox(
        "Kategori Tiket",
        [
            "Pilih Kategori Tiket",
            "VIP",
            "CAT 1",
            "CAT 2",
            "CAT 3"
        ]
    )

    # Jumlah tiket awal 0
    jumlah = st.number_input(
        "Jumlah Tiket",
        min_value=0,
        max_value=4,
        value=0,
        step=1
    )

    # Metode pembayaran awal kosong
    metode_pembayaran = st.selectbox(
        "Metode Pembayaran",
        [
            "Pilih Metode Pembayaran",
            "Debit",
            "QRIS",
            "GoPay",
            "DANA"
        ]
    )

    # Harga otomatis 0 jika kategori belum dipilih
    harga = harga_tiket.get(kategori, 0)

    if kategori == "Pilih Kategori Tiket":
        harga = 0

    total = harga * jumlah

    st.write(f"### Harga Tiket : Rp {harga:,}")
    st.write(f"### Total Harga : Rp {total:,}")

    submit = st.form_submit_button("Tambah Pemesan")


# =====================================
# PROSES TAMBAH DATA
# =====================================

# =====================================
# PROSES TAMBAH DATA + CETAK TIKET
# =====================================

if submit:

    if (
        nama.strip() == ""
        or email.strip() == ""
        or telepon.strip() == ""
        or ktp.strip() == ""
    ):
        st.warning("⚠️ Lengkapi data terlebih dahulu!")

    elif tanggal_lahir.year < 1999 or tanggal_lahir.year > 2008:
        st.warning("⚠️ Tahun lahir harus antara 1999 - 2008!")

    elif kategori == "Pilih Kategori Tiket":
        st.warning("⚠️ Silakan pilih kategori tiket!")

    elif jumlah == 0:
        st.warning("⚠️ Jumlah tiket harus lebih dari 0!")

    elif metode_pembayaran == "Pilih Metode Pembayaran":
        st.warning("⚠️ Silakan pilih metode pembayaran!")
    
    elif not ktp.isdigit() or len(ktp) != 16:
        st.warning("⚠️ Nomor KTP harus 16 digit angka!")

    else:

        # Simpan ke Linked List
        st.session_state.tiket.tambah(
            nama,
            email,
            telepon,
            ktp,
            tanggal_lahir,
            kategori,
            harga,
            jumlah,
            total,
            metode_pembayaran
        )

        st.success("✅ Pemesan berhasil ditambahkan")
        st.success("💳 Pembayaran Berhasil")
        st.success("🎟 Tiket Akan Dikirim ke Email")
        st.rerun()

        # Kode Tiket Otomatis
        kode_tiket = f"JB-{nama[:3].upper()}-{ktp[-4:]}"

        tiket_text = f"""
        if kirim_email(email, tiket_text):
    st.success(f"📧 Tiket berhasil dikirim ke {email}")
else:
    st.error("❌ Tiket gagal dikirim")
    
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

# =====================================
# DAFTAR PEMESAN
# =====================================

st.subheader("📋 Daftar Pemesan")

data = st.session_state.tiket.tampilkan()

if data:
    st.table(data)

else:
    st.info("Belum ada data pemesan.")


# =====================================
# CARI PEMESAN
# =====================================

st.subheader("🔍 Cari Pemesan")

nama_cari = st.text_input(
    "Masukkan nama pemesan yang dicari"
)

if st.button("Cari Pemesan"):

    hasil = st.session_state.tiket.cari(
        nama_cari
    )

    if hasil:

        st.success("✅ Data ditemukan")

        st.write(f"Nama : {hasil.nama}")
        st.write(f"Email : {hasil.email}")
        st.write(f"No Telepon : {hasil.telepon}")
        st.write(f"No KTP : {hasil.ktp}")
        st.write(f"Tanggal Lahir : {hasil.tanggal_lahir}")
        st.write(f"Kategori : {hasil.kategori}")
        st.write(f"Harga Tiket : Rp {hasil.harga:,}")
        st.write(f"Jumlah Tiket : {hasil.jumlah}")
        st.write(f"Total Harga : Rp {hasil.total:,}")
        st.write(f"Metode Pembayaran : {hasil.pembayaran}")

    else:
        st.error("❌ Data tidak ditemukan")



# =====================================
# HAPUS PEMESAN
# =====================================

st.subheader("🗑 Hapus Pemesan")

if st.session_state.pesan_hapus != "":
    st.success(st.session_state.pesan_hapus)
    st.session_state.pesan_hapus = ""

nama_hapus = st.text_input(
    "Masukkan nama pemesan yang akan dihapus"
)

if st.button("Hapus Pemesan"):

    berhasil = st.session_state.tiket.hapus(
        nama_hapus
    )

    if berhasil:

        st.session_state.pesan_hapus = "✅ Pesanan sudah dihapus"
        st.rerun()

    else:

        st.error("❌ Data tidak ditemukan")
