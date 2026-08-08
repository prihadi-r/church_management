# ⛪ Church Management — Installation Guide

Panduan lengkap untuk menginstal dan mengkonfigurasi modul **Church Management**
pada Odoo 18. Dokumen ini menjelaskan semua **persyaratan** (requirements),
**langkah instalasi**, dan **pemecahan masalah** umum.

> Terakhir diperbarui untuk **versi 1.1.0**.

---

## 1. Ringkasan Persyaratan (Requirements)

| Komponen | Persyaratan | Keterangan |
|----------|-------------|------------|
| **Odoo** | **18.0+** | Modul ini dikembangkan dan diuji pada Odoo 18. |
| **Python** | **3.10 – 3.12** | Versi Python yang didukung resmi oleh Odoo 18. |
| **PostgreSQL** | **14, 15, atau 16** | Basis data yang didukung resmi oleh Odoo 18. |
| **Python packages** | `feedparser` | Diperlukan untuk fitur berita / RSS. |
| **Odoo apps (dependencies)** | `base`, `crm`, `event`, `account`, `website` | Modul bawaan Odoo yang harus tersedia & terpasang. |
| **Browser** | Chrome / Edge / Firefox (terbaru) | Untuk mengakses antarmuka Odoo & website publik. |

---

## 2. Persyaratan Sistem

### 2.1 Odoo 18
- Modul membutuhkan **Odoo 18.0 atau lebih baru**.
- Modul **tidak kompatibel** dengan Odoo 17 ke bawah (beberapa API & struktur
  field sudah berubah).

### 2.2 Python
- Odoo 18 resmi mendukung **Python 3.10, 3.11, dan 3.12**.
- Pastikan `python` tersedia di PATH, atau gunakan interpreter Python bawaan
  instalasi Odoo Anda.

### 2.3 PostgreSQL
- Odoo 18 mendukung **PostgreSQL 14, 15, atau 16**.
- Dibutuhkan user basis data dengan hak akses untuk membuat/mengubah database.

> 💡 **Contoh instalasi Windows (all-in-one):** paket *Odoo 18 Community* untuk
> Windows sudah membundel Python, PostgreSQL, dan dependensi Python yang umum —
> termasuk `feedparser`. Anda cukup memastikan paket tambahan sesuai Bagian 4.

---

## 3. Dependensi Modul Odoo (Odoo Apps)

Modul ini bergantung pada **5 modul bawaan Odoo**. Semua sudah tersedia di
instalasi Odoo standar, namun **harus terpasang** (atau setidaknya tersedia)
sebelum modul ini diinstal.

| Modul | Alasan |
|-------|--------|
| **base** | Fondasi Odoo (selalu ada). |
| **crm** | Untuk perluasan **CRM Leads** (`crm.lead`). |
| **event** | Untuk perluasan **Events** (`event.event`) & jadwal ibadah. |
| **account** | Untuk perluasan **Payments/Donasi** (`account.payment`). |
| **website** | Untuk halaman publik (kalender gereja & formulir doa). |

> Jika salah satu modul di atas **belum terpasang**, Odoo akan otomatis
> menginstalnya sebagai dependensi saat Anda menginstal *Church Management*
> (asalkan ada di direktori addons). Modul `website` biasanya perlu diinstal
> terlebih dahulu agar fitur publik berfungsi penuh.

---

## 4. Dependensi Python (pip)

Modul membutuhkan **satu** package Python tambahan:

### `feedparser`
Digunakan oleh fitur **News / Berita** untuk membaca umpan RSS.

```bash
pip install feedparser
```

Pada instalasi Windows all-in-one Odoo, gunakan interpreter Python yang sama
dengan Odoo (bukan Python sistem). Contoh:

```powershell
# Jika Odoo membundel Python-nya sendiri:
& "C:\Program Files\Odoo 18.0.20260806\python\python.exe" -m pip install feedparser
```

> Jika `feedparser` tidak terpasang, modul akan **gagal diinstal** karena
> deklarasi `external_dependencies` di `__manifest__.py`.

---

## 5. Langkah Instalasi

### 5.1 Salin Modul ke Direktori Addons
Salin folder `church_management` ke dalam direktori addons Odoo Anda.
Contoh (Windows all-in-one):

```
C:\Program Files\Odoo 18.0.20260806\server\odoo\addons\church_management
```

atau pada instalasi Linux:

```bash
cp -r church_management /opt/odoo/addons/
```

Pastikan folder berisi `__manifest__.py` (bukan hanya isinya).

### 5.2 (Opsional) Tambahkan ke `addons_path`
Jika addons Anda berada di luar `addons_path` default, tambahkan di file
konfigurasi Odoo (`odoo.conf`):

```ini
[options]
addons_path = /path/ke/addons,/path/ke/addons/lain
```

### 5.3 Restart Layanan Odoo
Setelah menyalin modul (terutama pada Windows), **restart layanan Odoo** agar
direktori addons dan registri modul terbaru terbaca.

```powershell
Restart-Service odoo-server-18.0
```

### 5.4 Perbarui Daftar Aplikasi
1. Masuk ke Odoo sebagai administrator.
2. Aktifkan **Developer Mode** (Settings → *Activate Developer Mode*) jika perlu.
3. Buka **Apps** → klik **Update Apps List** (pada Odoo 18 cukup klik menu Apps).

### 5.5 Cari & Instal Modul
1. Di **Apps**, hapus filter dan cari **"Church Management"**.
2. Klik **Install**.
3. Odoo akan otomatis menginstal dependensi (`crm`, `event`, `account`,
   `website`) bila belum terpasang.

### 5.6 Verifikasi Instalasi
- Menu **Church Management** muncul di bar aplikasi utama.
- **Dashboard** menampilkan kartu statistik.
- **Operations → Pray Requests** dan **Operations → Church Calendar** tersedia.
- Halaman publik **`/church-calendar`** dan **`/church-pray`** dapat diakses.

---

## 6. Konfigurasi Setelah Instalasi

### 6.1 Grup Pengguna / Hak Akses
Modul mendefinisikan 3 grup keamanan:

| Grup | Hak |
|------|-----|
| **Read Only** | Hanya bisa melihat data. |
| **Write Only** | Bisa melihat & mengubah data. |
| **Full Access** | Akses penuh (lihat, ubah, buat, hapus). |

Berikan hak akses yang sesuai kepada pengguna melalui **Settings → Users →
Access Rights** (kategori **Church Management**).

### 6.2 Website Publik
- Pastikan modul **website** aktif.
- Menu website **Church Calendar** dan **Prayer Request** otomatis dibuat.
- Untuk akses tanpa login, kunjungi `/church-calendar` dan `/church-pray`.

### 6.3 Data Sampel
Modul menyediakan **data sampel** (member types, kontak, baptis, pernikahan,
permohonan doa, dll.) yang dimuat saat instalasi untuk memudahkan latihan.

---

## 7. Memperbarui / Upgrade Modul

Setiap perubahan pada model/field membutuhkan **restart** + **upgrade**:

1. **Restart layanan Odoo** agar kode model terbaru dimuat ke registry:

   ```powershell
   Restart-Service odoo-server-18.0
   ```

2. **Upgrade modul** di UI: **Apps → Church Management → Upgrade**.

> ⚠️ Odoo **tidak memuat ulang modul Python yang sudah dimuat** hanya dengan
> restart *registry*; oleh karena itu selalu restart layanan **sebelum** upgrade
> setelah menambah/mengubah model.

---

## 8. Pemecahan Masalah (Troubleshooting)

| Gejala | Kemungkinan Penyebab | Solusi |
|--------|----------------------|--------|
| `No module named 'feedparser'` | Package Python belum terpasang. | `pip install feedparser` (gunakan interpreter Python Odoo). |
| `No matching record found for external id 'model_...'` saat upgrade | Layanan Odoo berjalan dengan kode lama (model baru belum dimuat). | Restart layanan Odoo, lalu **upgrade** modul lagi. |
| `Warning: Field ... unknown parameter 'tracking'` | Parameter field tidak dikenal di Odoo 18. | Hapus parameter `tracking=True` pada definisi field. |
| Halaman publik 404 | Modul `website` belum aktif / route belum didaftarkan. | Instal `website`, restart Odoo. |
| Menu tidak muncul | Hak akses grup belum diberikan. | Beri akses grup **Church Management** pada pengguna. |
| Perubahan kode tidak berefek | Layanan masih memuat registry lama. | `Restart-Service odoo-server-18.0` lalu upgrade. |

---

## 9. File Penting

| File | Fungsi |
|------|--------|
| `__manifest__.py` | Deklarasi modul: nama, versi, dependensi, data, hooks. |
| `hooks.py` | `post_init_hook` (inisialisasi data awal). |
| `security/church_security.xml` | Definisi grup pengguna. |
| `security/ir.model.access.csv` | Aturan akses per model. |
| `data/*.xml` | Data sampel & data master. |
| `models/*.py` | Definisi model (logika bisnis). |
| `views/*.xml` | Antarmuka (menu, action, view). |
| `controllers/*.py` | Route website publik. |

---

## 10. Lisensi

Modul dirilis di bawah lisensi **LGPL-3** — bebas digunakan dan dimodifikasi.
