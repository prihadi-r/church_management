# ⛪ Church Management — Installation Guide

Panduan lengkap untuk menginstal dan mengkonfigurasi modul **Church Management**
pada Odoo 18. Dokumen ini menjelaskan semua **persyaratan** (requirements),
**langkah instalasi**, dan **pemecahan masalah** umum.

> Terakhir diperbarui untuk **versi 1.1.1**.

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
> (asalkan ada di direktori addons).
>
> ⚠️ **`website` wajib terpasang.** Jika belum, instalasi akan berhenti dengan
> `module church_management: Unmet dependencies: website` dan modul tertahan di
> status `to install`. Instal `website` terlebih dahulu, misalnya via CLI:
>
> ```bash
> odoo -i website,church_management -d <nama_db> --stop-after-init
> ```

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

> 💡 **Alternatif (CLI):** untuk menginstal sekaligus semua dependensi yang
> hilang, jalankan dari terminal:
>
> ```bash
> odoo -i website,church_management -d <nama_db> --stop-after-init
> ```

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
- Menu website **Church Calendar**, **Prayer Request**, dan **Christianity News** otomatis dibuat.
- Untuk akses tanpa login, kunjungi:
  - `/church-calendar` — kalender kegiatan publik.
  - `/church-pray` — formulir permohonan doa.
  - `/christianity-news` — halaman berita Kristen.
- Halaman beranda memiliki **SEO** (title, meta description, keywords).
- Desain beranda disediakan oleh tema pendamping opsional **`church_theme`** (lihat **Bagian 11**).

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

> 🐳 **Deployment Docker Compose:** upgrade modul dari dalam container (ganti
> `<db>` dengan nama database):
>
> ```bash
> docker compose stop web \
>   && docker compose run --rm -T web odoo -d <db> -c /etc/odoo/odoo.conf -u church_management --stop-after-init \
>   && docker compose start web
> ```

---

## 8. Pemecahan Masalah (Troubleshooting)

| Gejala | Kemungkinan Penyebab | Solusi |
|--------|----------------------|--------|
| `No module named 'feedparser'` | Package Python belum terpasang. | `pip install feedparser` (gunakan interpreter Python Odoo). |
| `No matching record found for external id 'model_...'` saat upgrade | Layanan Odoo berjalan dengan kode lama (model baru belum dimuat). | Restart layanan Odoo, lalu **upgrade** modul lagi. |
| `Warning: Field ... unknown parameter 'tracking'` | Parameter field tidak dikenal di Odoo 18. | Hapus parameter `tracking=True` pada definisi field. |
| Halaman publik 404 | Modul `website` belum aktif / route belum didaftarkan. | Instal `website`, restart Odoo. |
| Menu tidak muncul | Hak akses grup belum diberikan. | Beri akses grup **Church Management** (Read Only / Write Only / Full Access) pada pengguna di **Settings → Users → Access Rights**. |
| `Unmet dependencies: website` | Modul **`website`** belum terpasang; modul tertahan di status `to install`. | Instal `website` (mis. `odoo -i website,church_management -d <db> --stop-after-init`), lalu instal ulang. |
| `ParseError: External ID not found ... menu_church_operations` | Kopi modul lama dengan urutan menu yang salah (bug < 1.1.1). | Ganti seluruh folder modul dengan versi **1.1.1+**, lalu upgrade. |
| `"res.config.settings"."vat_check_vies" field is undefined` (klien) | Sisa modul `base_vat` dari migrasi Odoo 17 → 18; view settings lama masih merujuk field yang sudah dihapus. | Nonaktifkan view sisa: `UPDATE ir_ui_view SET active = false WHERE id = <id_view>;` (cari via `arch_db::text LIKE '%vat_check_vies%'`). |
| Perubahan kode tidak berefek | Layanan masih memuat registry lama. | `Restart-Service odoo-server-18.0` lalu upgrade. |
| `lxml XMLSyntaxError: Entity 'mdash' not defined` saat install | View XML memakai entitas HTML (`&mdash;`, `&ndash;`) yang tidak valid di XML (server Linux/lxml ketat). | Ganti dengan karakter Unicode literal (`—`, `–`). Hanya `&amp; &lt; &gt; &quot; &apos;` yang valid. |
| `AttributeError: module ... has no attribute 'post_init_hook'` | `__init__.py` tidak mengimpor hook. | Tambahkan `from . import hooks` **dan** `from .hooks import post_init_hook` di `__init__.py`. |
| `ValidationError: Start tag expected, '<' not found` saat hook menulis arch | Menulis `arch_db` menyisakan satu bahasa (mis. `en_US`) kosong, atau via ORM memicu validasi. | Selalu sertakan `en_US`, dan tulis `arch_db` via raw SQL (`UPDATE ir_ui_view SET arch_db = ...::jsonb`). |

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

## 11. Tema Pendamping `church_theme`

Halaman beranda website (hero, fitur, kalender, CTA) didesain oleh **`church_theme`** —
sebuah tema website Odoo 18 terpisah yang bergantung hanya pada `website`.

- **Opsional** tetapi disarankan jika ingin beranda ber-tema.
- Salin folder `church_theme` ke direktori addons, lalu **instal** seperti modul lain.
- Jika tidak diinstal, modul tetap berfungsi penuh (backend, `/church-calendar`,
  `/church-pray`, `/christianity-news`) namun beranda memakai tema default Odoo.

---

## 12. Lisensi

Modul dirilis di bawah lisensi **LGPL-3** — bebas digunakan dan dimodifikasi.
