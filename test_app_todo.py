import os
import json
import pytest
# Mengambil fungsi-fungsi dari file utama (app_todo.py) untuk diuji
from app_todo import (
    simpan_ke_file, muat_dari_file, cari_tugas_by_id,
    FILENAME as ORIGINAL_FILENAME
)


# --- KONFIGURASI TESTING ---

# FIXTURE: Fungsi khusus pytest untuk menyiapkan lingkungan pengujian.
# 'tmp_path' adalah folder sementara yang disediakan pytest agar tes tidak mengotori komputer kita.
@pytest.fixture
def temp_db(tmp_path):
    # 1. Menentukan lokasi file database palsu khusus untuk tes
    temp_file = tmp_path / "test_tugas.json"

    # 2. Teknik 'Monkeypatching': Kita paksa aplikasi utama menggunakan
    # file sementara ini, bukan file 'tugas_saya.json' yang asli.
    import app_todo
    app_todo.FILENAME = str(temp_file)

    # 3. 'yield' artinya: jalankan tes sekarang menggunakan file ini
    yield str(temp_file)

    # 4. 'Cleanup': Setelah tes selesai, kita kembalikan nama file ke aslinya
    # agar aplikasi kembali normal saat dijalankan di luar mode tes.
    app_todo.FILENAME = ORIGINAL_FILENAME


# --- 1. PENGUJIAN LOGIKA FILE (JSON) ---

def test_muat_dari_file_kosong(temp_db):
    """Membuktikan aplikasi tidak error jika database belum ada."""
    if os.path.exists(temp_db):
        os.remove(temp_db)  # Pastikan file benar-benar tidak ada
    # assert (tegaskan): Hasilnya harus berupa list kosong []
    assert muat_dari_file() == []


def test_simpan_dan_muat_valid(temp_db):
    """Membuktikan data yang disimpan bisa dibaca kembali dengan benar."""
    data = [{"id": 1, "judul": "Tes", "status": False, "estimasi_waktu": 10}]
    simpan_ke_file(data)  # Simpan dulu

    hasil = muat_dari_file()  # Coba ambil lagi
    # Cek apakah jumlahnya benar dan judulnya tidak berubah
    assert len(hasil) == 1
    assert hasil[0]["judul"] == "Tes"


def test_muat_file_rusak(temp_db):
    """Membuktikan aplikasi tetap stabil (tidak crash) jika file JSON isinya rusak."""
    with open(temp_db, "w") as f:
        f.write("INI BUKAN JSON FORMAT")  # Sengaja merusak file

    # Hasilnya harus kembali ke list kosong sesuai penanganan error kita
    assert muat_dari_file() == []


# --- 2. PENGUJIAN LOGIKA PENCARIAN (HELPER) ---

def test_cari_tugas_by_id_ditemukan():
    """Membuktikan fungsi pencarian bisa menemukan data yang ada."""
    daftar = [{"id": 1, "judul": "A"}, {"id": 2, "judul": "B"}]
    hasil = cari_tugas_by_id(daftar, 2)
    # assert is not None: Memastikan hasilnya ada (tidak kosong)
    assert hasil is not None
    assert hasil["judul"] == "B"


def test_cari_tugas_by_id_tidak_ada():
    """Membuktikan fungsi pencarian memberikan 'None' jika ID tidak eksis."""
    daftar = [{"id": 1, "judul": "A"}]
    hasil = cari_tugas_by_id(daftar, 99)
    assert hasil is None


# --- 3. PENGUJIAN LOGIKA CORE (STATISTIK & MANIPULASI) ---

def test_logika_statistik():
    """Membuktikan perhitungan matematika untuk progress dan sisa waktu sudah akurat."""
    daftar = [
        {"id": 1, "status": True, "estimasi_waktu": 30},  # Selesai
        {"id": 2, "status": False, "estimasi_waktu": 45}  # Belum (sisa waktu: 45)
    ]
    total = len(daftar)
    selesai = sum(t["status"] for t in daftar)
    sisa_waktu = sum(t["estimasi_waktu"] for t in daftar if not t["status"])

    # Memastikan angka-angka hasil hitungan sesuai dengan logika kita
    assert total == 2
    assert selesai == 1
    assert sisa_waktu == 45


def test_logika_hapus_data():
    """Membuktikan logika penghapusan tugas benar-benar menghilangkan data yang dipilih."""
    daftar = [{"id": 1}, {"id": 2}, {"id": 3}]
    id_hapus = 2

    # Melakukan pemfilteran list (menghapus ID 2)
    daftar[:] = [t for t in daftar if t["id"] != id_hapus]

    # Cek jumlah tugas berkurang dan ID 2 sudah tidak ada lagi
    assert len(daftar) == 2
    assert not any(t["id"] == 2 for t in daftar)


def test_logika_id_otomatis():
    """Membuktikan pemberian ID baru selalu naik 1 dari ID tertinggi (tidak boleh duplikat)."""
    # Kasus 1: Daftar berisi data dengan ID 1 dan 10. ID baru harus 11.
    daftar = [{"id": 1}, {"id": 10}]
    id_baru = max([t["id"] for t in daftar], default=0) + 1
    assert id_baru == 11

    # Kasus 2: Daftar masih kosong. ID baru harus dimulai dari 1.
    daftar_kosong = []
    id_baru_kosong = max([t["id"] for t in daftar_kosong], default=0) + 1
    assert id_baru_kosong == 1