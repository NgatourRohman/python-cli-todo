# 📝 Python CLI To-Do List

Aplikasi To-Do List interaktif berbasis **Command Line Interface (CLI)** yang dibangun menggunakan Python. Proyek ini dirancang untuk membantu pengelolaan tugas harian dengan fitur statistik kemajuan dan penyimpanan data permanen.

Tujuan utama proyek ini adalah menerapkan prinsip *Clean Code*, *Unit Testing*, dan *Data Persistence* dalam siklus pengembangan perangkat lunak sederhana.

---

## ✨ Fitur Utama

* 📊 **Dashboard Statistik**
  Menampilkan persentase penyelesaian tugas dan total sisa waktu pengerjaan secara otomatis di menu utama.

* 📂 **Penyimpanan Permanen**
  Data disimpan dalam format JSON (`tugas_saya.json`) sehingga tidak hilang saat aplikasi ditutup.

* 🛠️ **Operasi CRUD Lengkap**

  * **Tambah:** Menambahkan tugas dengan validasi judul dan estimasi waktu
  * **Lihat:** Menampilkan daftar tugas dengan tampilan rapi
  * **Edit:** Mengubah detail tugas tanpa harus menghapus
  * **Hapus:** Menghapus tugas berdasarkan ID unik

* 🔍 **Filter Tugas**
  Memfilter tugas berdasarkan status:

  * Semua
  * Selesai
  * Belum Selesai

* 🛡️ **Penanganan Error**

  * Validasi input (tidak boleh kosong atau negatif)
  * Penanganan file JSON yang rusak (*corrupted*)

* 🧪 **Unit Testing**
  Menggunakan `pytest` untuk memastikan stabilitas logika aplikasi.

---

## 🚀 Cara Menjalankan Aplikasi

### Prasyarat

* Python **3.10** atau lebih baru
* `pytest` (opsional, hanya untuk testing)

### Instalasi & Penggunaan

```bash
git clone https://github.com/NgatourRohman/python-cli-todo.git
cd python-cli-todo
python app_todo.py
```

---

## 🧪 Pengujian (Unit Testing)

Proyek ini menggunakan **pytest** untuk menguji logika aplikasi. Pengujian menggunakan *temporary file database* sehingga tidak akan mengganggu data asli.

### Instalasi pytest

```bash
pip install pytest
```

### Menjalankan Test

```bash
pytest test_app_todo.py
```

---

## 📂 Struktur Proyek

```
To-DoListCLI/
│
├── app_todo.py        # Logika utama aplikasi & CLI
├── test_app_todo.py   # Unit testing
├── .gitignore         # File yang diabaikan Git
└── README.md          # Dokumentasi proyek
```

---

## 🛠️ Detail Teknis

* **Struktur Data:**
  Menggunakan *List of Dictionaries* untuk fleksibilitas data

* **Data Persistence:**
  Menggunakan modul `json` bawaan Python (UTF-8)

* **Algoritma:**
  Menggunakan *Generator Expression* dan `next()` untuk pencarian ID yang efisien

* **Arsitektur:**
  Pemisahan fungsi *helper* dan *core logic* untuk maintainability