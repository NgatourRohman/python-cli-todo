import json
import os

FILENAME = "tugas_saya.json"


# --- HELPER FUNCTIONS ---

def simpan_ke_file(daftar_tugas):
    try:
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(daftar_tugas, f, indent=4)
    except IOError as e:
        print(f"⚠️ Gagal menyimpan data: {e}")


def muat_dari_file():
    if not os.path.exists(FILENAME):
        return []

    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            if os.path.getsize(FILENAME) == 0:
                return []
            return json.load(f)
    except json.JSONDecodeError:
        print("\n" + "!" * 50)
        print("⚠️ PERINGATAN: File 'tugas_saya.json' rusak atau formatnya salah.")
        print("Sangat disarankan untuk mengecek file tersebut secara manual.")
        print("!" * 50)
        # input(
        #     "Tekan Enter untuk melanjutkan dengan daftar kosong (Data lama tidak akan hilang sampai Anda menyimpan data baru)...")
        return []
    except Exception as e:
        print(f"⚠️ Terjadi kesalahan sistem: {e}")
        return []


def cari_tugas_by_id(daftar_tugas, id_target):
    return next((t for t in daftar_tugas if t["id"] == id_target), None)


# --- CORE FUNCTIONS ---

def tampilkan_statistik(daftar_tugas):
    if not daftar_tugas:
        print("\n📊 Statistik: Belum ada data tugas.")
        return
    total = len(daftar_tugas)
    selesai = sum(t["status"] for t in daftar_tugas)
    persen = (selesai / total) * 100
    sisa_waktu = sum(t["estimasi_waktu"] for t in daftar_tugas if not t["status"])

    print(f"\n📊 PROGRESS: {selesai}/{total} Selesai ({persen:.1f}%) | ⏳ Sisa Waktu: {sisa_waktu} mnt")


def tampilkan_tugas(daftar_tugas, filter_status=None):
    print("\n" + "=" * 50)
    label = "SEMUA TUGAS" if filter_status is None else ("SELESAI" if filter_status else "BELUM SELESAI")
    print(f"📋 {label}")
    print("=" * 50)

    tugas_tampil = [t for t in daftar_tugas if filter_status is None or t["status"] == filter_status]

    if not tugas_tampil:
        print("Kategori ini masih kosong.")
    else:
        for t in tugas_tampil:
            simbol = "[✓]" if t["status"] else "[ ]"
            print(f"{simbol} ID: {t['id']} | {t['judul']} ({t['estimasi_waktu']} mnt)")
            print(f"    Detail: {t['deskripsi']}")
    print("-" * 50)


def tambah_tugas(daftar_tugas):
    print("\n--- ➕ TAMBAH TUGAS ---")

    while True:
        judul = input("Judul: ").strip()
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

    id_baru = max([t["id"] for t in daftar_tugas], default=0) + 1
    daftar_tugas.append({
        "id": id_baru,
        "judul": judul,
        "deskripsi": deskripsi,
        "status": False,
        "estimasi_waktu": waktu
    })
    simpan_ke_file(daftar_tugas)
    print(f"✅ Tugas '{judul}' berhasil disimpan!")


def edit_tugas(daftar_tugas):
    tampilkan_tugas(daftar_tugas)
    try:
        id_target = int(input("\nMasukkan ID untuk edit: "))
        tugas = cari_tugas_by_id(daftar_tugas, id_target)

        if tugas:
            print(f"Mengedit: {tugas['judul']} (Tekan Enter untuk lewati)")
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


# --- MAIN APP ---

def main():
    daftar_tugas = muat_dari_file()

    menu_teks = (
        "\n1. Lihat Semua \n2. Tambah \n3. Selesaikan\n4. Edit \n5. Hapus \n6. Filter \n7. Keluar"
    )

    while True:
        tampilkan_statistik(daftar_tugas)
        print(menu_teks)
        pilihan = input("\nPilih menu: ")

        if pilihan == '1':
            tampilkan_tugas(daftar_tugas)
        elif pilihan == '2':
            tambah_tugas(daftar_tugas)
        elif pilihan == '3':
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
            break


if __name__ == "__main__":
    main()