import os
import json
import pytest
from app_todo import (
    simpan_ke_file, muat_dari_file, cari_tugas_by_id,
    FILENAME as ORIGINAL_FILENAME
)


# FIXTURE: Menyiapkan file JSON sementara untuk setiap test case
@pytest.fixture
def temp_db(tmp_path):
    # Membuat path file sementara
    temp_file = tmp_path / "test_tugas.json"

    # Teknik 'Monkeypatching' sederhana: Ganti variable FILENAME di modul app_todo
    import app_todo
    app_todo.FILENAME = str(temp_file)

    yield str(temp_file)

    # Cleanup: Kembalikan variable FILENAME ke semula setelah tes selesai
    app_todo.FILENAME = ORIGINAL_FILENAME


# --- 1. PENGUJIAN LOGIKA FILE (JSON) ---

def test_muat_dari_file_kosong(temp_db):
    """Skenario: File belum ada, harus return list kosong."""
    if os.path.exists(temp_db):
        os.remove(temp_db)
    assert muat_dari_file() == []


def test_simpan_dan_muat_valid(temp_db):
    """Skenario: Simpan data dan pastikan data yang dimuat sama."""
    data = [{"id": 1, "judul": "Tes", "status": False, "estimasi_waktu": 10}]
    simpan_ke_file(data)

    hasil = muat_dari_file()
    assert len(hasil) == 1
    assert hasil[0]["judul"] == "Tes"


def test_muat_file_rusak(temp_db):
    """Skenario: File berisi teks rusak (bukan JSON)."""
    with open(temp_db, "w") as f:
        f.write("INI BUKAN JSON FORMAT")
    # Logika kita di muat_dari_file akan return [] jika JSONDecodeError
    assert muat_dari_file() == []


# --- 2. PENGUJIAN LOGIKA PENCARIAN (HELPER) ---

def test_cari_tugas_by_id_ditemukan():
    daftar = [{"id": 1, "judul": "A"}, {"id": 2, "judul": "B"}]
    hasil = cari_tugas_by_id(daftar, 2)
    assert hasil is not None
    assert hasil["judul"] == "B"


def test_cari_tugas_by_id_tidak_ada():
    daftar = [{"id": 1, "judul": "A"}]
    hasil = cari_tugas_by_id(daftar, 99)
    assert hasil is None


# --- 3. PENGUJIAN LOGIKA CORE (STATISTIK & MANIPULASI) ---

def test_logika_statistik():
    """Menguji perhitungan persentase dan sisa waktu."""
    daftar = [
        {"id": 1, "status": True, "estimasi_waktu": 30},  # Selesai
        {"id": 2, "status": False, "estimasi_waktu": 45}  # Belum
    ]
    total = len(daftar)
    selesai = sum(t["status"] for t in daftar)
    sisa_waktu = sum(t["estimasi_waktu"] for t in daftar if not t["status"])

    assert total == 2
    assert selesai == 1
    assert sisa_waktu == 45


def test_logika_hapus_data():
    """Menguji logika list comprehension untuk menghapus data."""
    daftar = [{"id": 1}, {"id": 2}, {"id": 3}]
    id_hapus = 2

    # Simulasi logika di main()
    daftar[:] = [t for t in daftar if t["id"] != id_hapus]

    assert len(daftar) == 2
    assert not any(t["id"] == 2 for t in daftar)


def test_logika_id_otomatis():
    """Menguji pembuatan ID baru (max + 1)."""
    # Kasus daftar tidak kosong
    daftar = [{"id": 1}, {"id": 10}]
    id_baru = max([t["id"] for t in daftar], default=0) + 1
    assert id_baru == 11

    # Kasus daftar kosong
    daftar_kosong = []
    id_baru_kosong = max([t["id"] for t in daftar_kosong], default=0) + 1
    assert id_baru_kosong == 1