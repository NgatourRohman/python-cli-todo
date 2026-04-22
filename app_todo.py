import json  # Mengimpor library untuk mengolah data format JSON (simpan/buka file)
import os  # Mengimpor library untuk berinteraksi dengan sistem operasi (cek file)

# Nama file tempat kita menyimpan data secara permanen
FILENAME = "tugas_saya.json"


# --- HELPER FUNCTIONS (Fungsi Pembantu) ---

def simpan_ke_file(daftar_tugas):
    """Mengubah list daftar_tugas menjadi format JSON dan menyimpannya ke hardisk."""
    try:
        # 'w' artinya write (tulis ulang). encoding utf-8 agar mendukung karakter spesial/emoji.
        with open(FILENAME, "w", encoding="utf-8") as f:
            # indent=4 membuat tampilan file JSON rapi (bertingkat) saat dibaca manusia
            json.dump(daftar_tugas, f, indent=4)
    except IOError as e:
        # Menangani error jika file tidak bisa diakses (misal: memori penuh/masalah izin)
        print(f"⚠️ Gagal menyimpan data: {e}")


def muat_dari_file():
    """Mengambil data dari file JSON kembali ke dalam aplikasi saat dijalankan."""
    # Jika file belum ada (aplikasi baru pertama kali dijalankan), kembalikan list kosong []
    if not os.path.exists(FILENAME):
        return []

    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            # Cek jika file ada tapi isinya kosong (0 byte), kembalikan list kosong
            if os.path.getsize(FILENAME) == 0:
                return []
            return json.load(f)
    except json.JSONDecodeError:
        # Terjadi jika isi file JSON rusak atau tidak sengaja terhapus sebagian
        print("\n" + "!" * 50)
        print("⚠️ PERINGATAN: File 'tugas_saya.json' rusak atau formatnya salah.")
        print("Sangat disarankan untuk mengecek file tersebut secara manual.")
        print("!" * 50)

        # BAGIAN INTERAKSI USER (Dinonaktifkan untuk Automated Testing)
        # Jika ingin mengaktifkan jeda agar user bisa membaca peringatan sebelum lanjut,
        # silakan hapus tanda pagar (#) pada baris di bawah ini:

        # input("Tekan Enter untuk melanjutkan dengan daftar kosong (Data lama tidak akan hilang sampai Anda menyimpan data baru)...")

        return []
    except Exception as e:
        print(f"⚠️ Terjadi kesalahan sistem: {e}")
        return []


def cari_tugas_by_id(daftar_tugas, id_target):
    """
    Fungsi cerdas untuk mencari satu tugas di dalam list menggunakan ID.
    Menggunakan 'next' agar pencarian berhenti tepat saat data ditemukan (efisien).
    """
    return next((t for t in daftar_tugas if t["id"] == id_target), None)


# --- CORE FUNCTIONS (Fungsi Utama) ---

def tampilkan_statistik(daftar_tugas):
    """Menampilkan ringkasan kemajuan tugas pengguna."""
    if not daftar_tugas:
        print("\n📊 Statistik: Belum ada data tugas.")
        return

    total = len(daftar_tugas)
    # sum(1 for t...) menghitung jumlah elemen yang statusnya True
    selesai = sum(t["status"] for t in daftar_tugas)
    persen = (selesai / total) * 100
    # Menghitung estimasi waktu hanya untuk tugas yang statusnya masih False (belum selesai)
    sisa_waktu = sum(t["estimasi_waktu"] for t in daftar_tugas if not t["status"])

    print(f"\n📊 PROGRESS: {selesai}/{total} Selesai ({persen:.1f}%) | ⏳ Sisa Waktu: {sisa_waktu} mnt")


def tampilkan_tugas(daftar_tugas, filter_status=None):
    """Menampilkan daftar tugas dengan pilihan filter (Semua, Selesai, atau Belum)."""
    print("\n" + "=" * 50)
    # Logika label judul tabel
    label = "SEMUA TUGAS" if filter_status is None else ("SELESAI" if filter_status else "BELUM SELESAI")
    print(f"📋 {label}")
    print("=" * 50)

    # List Comprehension untuk menyaring tugas berdasarkan status
    tugas_tampil = [t for t in daftar_tugas if filter_status is None or t["status"] == filter_status]

    if not tugas_tampil:
        print("Kategori ini masih kosong.")
    else:
        for t in tugas_tampil:
            # Jika status True tampilkan centang, jika False tampilkan kotak kosong
            simbol = "[✓]" if t["status"] else "[ ]"
            print(f"{simbol} ID: {t['id']} | {t['judul']} ({t['estimasi_waktu']} mnt)")
            print(f"    Detail: {t['deskripsi']}")
    print("-" * 50)


def tambah_tugas(daftar_tugas):
    """Proses mengambil input dari user dan menambahkannya ke list."""
    print("\n--- ➕ TAMBAH TUGAS ---")

    # Perulangan while True memastikan user mengisi teks (tidak boleh kosong)
    while True:
        judul = input("Judul: ").strip()  # .strip() membuang spasi di awal/akhir
        if judul:
            break
        print("⚠️ Judul tidak boleh kosong. Silakan masukkan nama tugas.")

    deskripsi = input("Deskripsi: ").strip() or "-"

    while True:
        try:
            waktu_raw = input("Estimasi waktu (menit): ").strip()
            waktu = int(waktu_raw)
            if waktu < 0:
                print("⚠️ Waktu tidak bisa negatif!")
                continue
            break
        except ValueError:
            print("⚠️ Masukkan angka yang valid untuk waktu!")

    # Mencari ID terbesar yang sudah ada, lalu ditambah 1 agar selalu unik
    id_baru = max([t["id"] for t in daftar_tugas], default=0) + 1
    daftar_tugas.append({
        "id": id_baru,
        "judul": judul,
        "deskripsi": deskripsi,
        "status": False,
        "estimasi_waktu": waktu
    })
    simpan_ke_file(daftar_tugas)  # Langsung simpan ke hardisk setelah menambah
    print(f"✅ Tugas '{judul}' berhasil disimpan!")


def edit_tugas(daftar_tugas):
    """Memperbarui informasi tugas yang sudah ada berdasarkan ID."""
    tampilkan_tugas(daftar_tugas)
    try:
        id_target = int(input("\nMasukkan ID untuk edit: "))
        tugas = cari_tugas_by_id(daftar_tugas, id_target)

        if tugas:
            print(f"Mengedit: {tugas['judul']} (Tekan Enter untuk lewati)")
            # Logika 'or': Jika user hanya tekan Enter (input kosong), gunakan nilai lama
            tugas['judul'] = input(f"Judul [{tugas['judul']}]: ") or tugas['judul']
            tugas['deskripsi'] = input(f"Deskripsi [{tugas['deskripsi']}]: ") or tugas['deskripsi']
            waktu_raw = input(f"Waktu [{tugas['estimasi_waktu']}]: ")
            tugas['estimasi_waktu'] = int(waktu_raw) if waktu_raw else tugas['estimasi_waktu']

            simpan_ke_file(daftar_tugas)
            print("✅ Update berhasil!")
        else:
            print("⚠️ ID tidak ditemukan.")
    except ValueError:
        print("⚠️ Input tidak valid.")


# --- MAIN APP (Jantung Aplikasi) ---

def main():
    """Fungsi utama yang mengatur alur jalannya program."""
    # 1. Muat data dari file saat pertama kali dibuka
    daftar_tugas = muat_dari_file()

    menu_teks = (
        "\n1. Lihat Semua \n2. Tambah \n3. Selesaikan\n4. Edit \n5. Hapus \n6. Filter \n7. Keluar"
    )

    # Perulangan abadi agar program tidak mati sebelum user memilih 'Keluar'
    while True:
        tampilkan_statistik(daftar_tugas)
        print(menu_teks)
        pilihan = input("\nPilih menu: ")

        if pilihan == '1':
            tampilkan_tugas(daftar_tugas)
        elif pilihan == '2':
            tambah_tugas(daftar_tugas)
        elif pilihan == '3':
            # Hanya tampilkan tugas yang BELUM selesai untuk memudahkan user memilih
            tampilkan_tugas(daftar_tugas, filter_status=False)
            try:
                id_s = int(input("ID yang selesai: "))
                tugas = cari_tugas_by_id(daftar_tugas, id_s)
                if tugas:
                    tugas["status"] = True
                    simpan_ke_file(daftar_tugas)
                    print(f"🎉 '{tugas['judul']}' selesai!")
                else:
                    print("⚠️ ID tidak ditemukan.")
            except ValueError:
                print("⚠️ Masukkan angka ID!")
        elif pilihan == '4':
            edit_tugas(daftar_tugas)
        elif pilihan == '5':
            tampilkan_tugas(daftar_tugas)
            try:
                id_h = int(input("ID yang dihapus: "))
                tugas_awal = len(daftar_tugas)
                # Menyaring list: Simpan semua tugas KECUALI yang ID-nya dipilih untuk dihapus
                daftar_tugas[:] = [t for t in daftar_tugas if t["id"] != id_h]
                if len(daftar_tugas) < tugas_awal:
                    simpan_ke_file(daftar_tugas)
                    print("🗑️ Berhasil dihapus.")
                else:
                    print("⚠️ ID tidak ditemukan.")
            except ValueError:
                print("⚠️ Masukkan angka ID!")
        elif pilihan == '6':
            f = input("Filter (1: Selesai, 2: Belum Selesai): ")
            tampilkan_tugas(daftar_tugas, filter_status=(f == '1'))
        elif pilihan == '7':
            print("🚀 Tetap produktif! Sampai jumpa.")
            break  # Berhenti dari perulangan while, menutup program


# Memastikan fungsi main() hanya terpanggil jika file ini dijalankan secara langsung
if __name__ == "__main__":
    main()