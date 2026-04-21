import json
import os

FILENAME = "tugas_saya.json"


def simpan_ke_file(daftar_tugas):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(daftar_tugas, f, indent=4)


def muat_dari_file():
    if not os.path.exists(FILENAME):
        return [
            {"id": 1, "judul": "Review Materi MLOps", "deskripsi": "Mempelajari agentic workflows.", "status": True,
             "estimasi_waktu": 60},
            {"id": 2, "judul": "Kerjakan Fitur ArtBuddy", "deskripsi": "Sesuaikan prompt ArtStar.", "status": False,
             "estimasi_waktu": 60}
        ]
    with open(FILENAME, "r", encoding="utf-8") as f:
        return json.load(f)


def tampilkan_statistik(daftar_tugas):
    if not daftar_tugas:
        return
    total = len(daftar_tugas)
    selesai = sum(1 for t in daftar_tugas if t["status"])
    persen = (selesai / total) * 100
    total_waktu = sum(t["estimasi_waktu"] for t in daftar_tugas if not t["status"])

    print(f"\n📊 STATISTIK: {selesai}/{total} Tugas Selesai ({persen:.1f}%)")
    print(f"⏳ Sisa waktu pengerjaan: {total_waktu} menit")


def tampilkan_tugas(daftar_tugas, filter_status=None):
    print("\n" + "=" * 50)
    label = "SEMUA TUGAS" if filter_status is None else ("SELESAI" if filter_status else "BELUM SELESAI")
    print(f"📋 DAFTAR TUGAS ({label})")
    print("=" * 50)

    tugas_tampil = daftar_tugas if filter_status is None else [t for t in daftar_tugas if t["status"] == filter_status]

    if not tugas_tampil:
        print("Tidak ada tugas dalam kategori ini.")
    else:
        for tugas in tugas_tampil:
            simbol = "[✓]" if tugas["status"] else "[ ]"
            print(f"{simbol} ID: {tugas['id']} | {tugas['judul']} ({tugas['estimasi_waktu']} menit)")
            print(f"    Detail: {tugas['deskripsi']}")
            print("-" * 50)


def tambah_tugas(daftar_tugas):
    print("\n--- ➕ TAMBAH TUGAS BARU ---")
    judul = input("Judul: ")
    deskripsi = input("Deskripsi: ")
    while True:
        try:
            waktu = int(input("Estimasi waktu (menit): "))
            break
        except ValueError:
            print("⚠️ Masukkan angka!")

    id_baru = max([t["id"] for t in daftar_tugas], default=0) + 1
    daftar_tugas.append(
        {"id": id_baru, "judul": judul, "deskripsi": deskripsi, "status": False, "estimasi_waktu": waktu})
    simpan_ke_file(daftar_tugas)
    print("✅ Tersimpan!")


def edit_tugas(daftar_tugas):
    tampilkan_tugas(daftar_tugas)
    try:
        id_target = int(input("\nID tugas yang ingin diedit: "))
        for t in daftar_tugas:
            if t["id"] == id_target:
                print(f"Edit: {t['judul']}. Kosongkan jika tidak ingin mengubah.")
                judul = input(f"Judul baru [{t['judul']}]: ") or t['judul']
                desk = input(f"Deskripsi baru [{t['deskripsi']}]: ") or t['deskripsi']
                waktu_inp = input(f"Waktu baru [{t['estimasi_waktu']}]: ")
                waktu = int(waktu_inp) if waktu_inp else t['estimasi_waktu']

                t.update({"judul": judul, "deskripsi": desk, "estimasi_waktu": waktu})
                simpan_ke_file(daftar_tugas)
                print("✅ Berhasil diupdate!")
                return
        print("⚠️ ID tidak ditemukan.")
    except ValueError:
        print("⚠️ Input tidak valid.")


def hapus_tugas(daftar_tugas):
    tampilkan_tugas(daftar_tugas)
    try:
        id_target = int(input("\nID tugas yang akan dihapus: "))
        for i, t in enumerate(daftar_tugas):
            if t["id"] == id_target:
                daftar_tugas.pop(i)
                simpan_ke_file(daftar_tugas)
                print("🗑️ Berhasil dihapus.")
                return
        print("⚠️ ID tidak ditemukan.")
    except ValueError:
        print("⚠️ Input tidak valid.")


def main():
    daftar_tugas = muat_dari_file()

    while True:
        tampilkan_statistik(daftar_tugas)
        print("\n=== MENU UTAMA ===")
        print("1. Lihat Semua \n2. Tambah \n3. Tandai Selesai \n4. Edit \n5. Hapus \n6. Filter \n7. Keluar")

        p = input("\nPilih menu: ")
        if p == '1':
            tampilkan_tugas(daftar_tugas)
        elif p == '2':
            tambah_tugas(daftar_tugas)
        elif p == '3':
            tampilkan_tugas(daftar_tugas, False)
            try:
                id_s = int(input("ID yang selesai: "))
                for t in daftar_tugas:
                    if t["id"] == id_s: t["status"] = True; break
                simpan_ke_file(daftar_tugas)
            except:
                print("Gagal.")
        elif p == '4':
            edit_tugas(daftar_tugas)
        elif p == '5':
            hapus_tugas(daftar_tugas)
        elif p == '6':
            f = input("Filter (1: Selesai, 2: Belum): ")
            tampilkan_tugas(daftar_tugas, f == '1')
        elif p == '7':
            break


if __name__ == "__main__":
    main()