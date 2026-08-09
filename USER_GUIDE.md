# ⛪ Darash — Panduan Penggunaan (User Guide)

> Modul manajemen gereja pada Odoo 18. Dokumen ini menjelaskan fungsi setiap menu, layar yang tersedia, dan cara pengisian data. Disusun untuk bahan presentasi di gamma.app.

---

## 1. Ringkasan Modul

**Apa itu Church Management?**
- Modul Odoo 18 untuk mengelola kegiatan dan data gereja dalam satu aplikasi.
- Mengelola **keanggotaan jemaat**, **baptis**, **pernikahan**, **jadwal ibadah**, **pelayanan musik**, **permohonan doa**, dan **kalender kegiatan gereja** secara terpadu.

**Manfaat Utama**
- Semua data tersimpan di satu database (tidak perlu buku fisik).
- Setiap kegiatan (ibadah, baptis, nikah, jadwal musisi) otomatis tampil di **satu Kalender Kegiatan Gereja**.
- Ada **Dashboard** sebagai halaman utama yang menampilkan ringkasan angka.
- Alur kerja (workflow) dengan status: antrian → disetujui → selesai.

**Struktur Menu**
```
Church Management
├── Dashboard (halaman utama)
├── Master Data
│   ├── Member Types
│   ├── Care Cells
│   ├── Donation Types
│   ├── Sacrament Types
│   ├── Event Roles
│   └── Musician Roles
└── Operations
    ├── Event Rosters
    ├── Musician Schedule
    ├── Baptism Registrations
    ├── Marriage Registrations
    ├── Pray Requests
    └── Church Calendar
```

---

## 2. Dashboard (Halaman Utama)

**Fungsi:** Menampilkan ringkasan jumlah kegiatan gereja secara langsung saat aplikasi dibuka.

**Layar yang tersedia:**
- Lima kartu statistik:
  - **👥 Jemaat** — total jemaat (terdaftar sebagai anggota).
  - **💧 Baptis** — Baptis bulan ini, bulan lalu, dan jumlah yang masih antrian.
  - **💍 Pernikahan** — Pernikahan bulan ini, bulan lalu, dan yang masih antrian.
  - **⛪ Jadwal Ibadah** — Ibadah bulan ini, bulan lalu, dan yang akan datang.
  - **🙏 Pray Requests** — Permohonan doa bulan ini, bulan lalu, dan yang masih diproses.
- Bagian **Jemaat per Tipe Anggota**: rincian jumlah per tipe (Musisi, Pastur, dst.).
- Tombol pintasan (di bagian atas): *Baptism Registrations*, *Marriage Registrations*, *Pray Requests*, *Church Calendar*.

**Cara pakai:**
1. Buka menu **Church Management → Dashboard**.
2. Angka ter-update otomatis setiap kali dashboard dibuka.
3. Klik tombol pintasan untuk langsung membuka layar terkait.

> 💡 **Tip:** Angka "Antrian" = pendaftaran dengan status *Draft* atau *Under Review* (belum selesai diproses).

---

## 3. Master Data (Data Dasar)

Master Data berisi daftar istilah / kategori yang dipakai di seluruh modul. Semua layarnya sama: **Daftar (List)** dan **Form Isian**.

### 3.1 Member Types (Tipe Anggota)
- **Fungsi:** Kategori keanggotaan jemaat.
- **Layar:** List + Form.
- **Cara isi:** Klik **New** → isi **Name** (contoh: *Simpatisan, Jemaat Tetap, Musisi, Pastur, Pendoa* dst.) → **Save**.
- **Penting:** Tipe *Musisi* membuat field "Musician Role" muncul di Kontak; tipe *Pastur* membuat kontak bisa dipilih sebagai petugas (Officiating Minister) di Baptis & Pernikahan.

### 3.2 Care Cells (Kelompok Sel)
- **Fungsi:** Nama kelompok sel / komsel.
- **Cara isi:** New → isi **Name** → Save.

### 3.3 Donation Types (Jenis Persembahan)
- **Fungsi:** Jenis-jenis persembahan/donasi.
- **Cara isi:** New → isi **Name** → Save.

### 3.4 Sacrament Types (Jenis Sakramen)
- **Fungsi:** Jenis sakramen (contoh: *Baptis, Pernikahan*).
- **Cara isi:** New → isi **Name** → Save.

### 3.5 Event Roles (Peran Pelayanan)
- **Fungsi:** Peran pelayanan dalam ibadah (contoh: *Pengkhotbah, Usher, WL*).
- **Cara isi:** New → isi **Name** → Save.

### 3.6 Musician Roles (Peran Pemusik)
- **Fungsi:** Posisi pemusik (contoh: *Bass, Gitaris, Singer, Pianis*).
- **Cara isi:** New → isi **Name** → Save.

---

## 4. Operations (Kegiatan)

### 4.1 Event Rosters (Jadwal Petugas Ibadah)
- **Fungsi:** Menentukan siapa bertugas pada suatu ibadah/event, dengan peran tertentu.
- **Layar:** List + Form.
- **Cara isi:**
  1. Klik **New**.
  2. Pilih **Event** (ibadah) dan **Role** (peran pelayanan).
  3. Isi petugas / kontak yang bertugas.
  4. **Save**.
- Otomatis tampil pada form Event (Ibadah) yang bersangkutan.

### 4.2 Musician Schedule (Jadwal Musisi)
- **Fungsi:** Menjadwalkan pemusik beserta peran dan waktu pelayanan.
- **Layar:** **Kalender** + List + Form.
- **Cara isi:**
  1. Klik **New** (atau klik tanggal di tampilan Kalender → **New**).
  2. Pilih **Musician** (kontak) — jika tipe anggota *Musisi*, field **Musician Role** otomatis tampil.
  3. Isi **Date**, **Start Time**, **End Time**.
  4. **Save** — otomatis masuk ke Kalender Kegiatan Gereja.

### 4.3 Baptism Registrations (Pendaftaran Baptis)
- **Fungsi:** Mencatat dan memproses pendaftaran baptis jemaat.
- **Layar:** **Kanban** (kartu per status), **Kalender**, **List**, **Form**, **Search** (filter status).
- **Cara isi:**
  1. Klik **New**.
  2. Pilih **Partner** (kandidat/calon yang dibaptis) — data nama, telepon, email, alamat otomatis terbawa.
  3. Isi **Birth Date** (tanggal lahir), **Age** (otomatis), dan **Father / Mother** bila baptis anak.
  4. Pilih **Sacrament Type**, **Baptism Datetime** (tanggal & jam), dan **Officiating Minister** (hanya kontak ber-type *Pastur*).
  5. **Save**, lalu proses lewat tombol di atas form:
     - **Submit for Review** → **Approve** → **Mark Completed**
     - **Cancel** untuk membatalkan.
- **Kanban:** kartu berwarna sesuai status; seret kartu antar kolom untuk mengubah status.
- Otomatis tampil di Kalender Kegiatan Gereja.

### 4.4 Marriage Registrations (Pendaftaran Pernikahan)
- **Fungsi:** Mencatat dan memproses pendaftaran pernikahan.
- **Layar:** **Kanban**, **Kalender**, **List**, **Form**, **Search**.
- **Cara isi:**
  1. Klik **New**.
  2. Pilih **Groom** (mempelai pria) dan **Bride** (mempelai wanita) — **Name** otomatis terbentuk.
  3. Pilih **Sacrament Type**, **Marriage Datetime**, dan **Officiating Minister** (hanya kontak ber-type *Pastur*).
  4. **Save**, lalu proses: **Submit for Review** → **Approve** → **Mark Completed**.
- **Kanban:** kartu berwarna sesuai status.
- Otomatis tampil di Kalender Kegiatan Gereja.

### 4.5 Pray Requests (Permohonan Doa)
- **Fungsi:** Mencatat permohonan doa dari jemaat/publik dan memprosesnya melalui sesi-sesi doa.
- **Layar:** **Kanban** (kartu per status), **Kalender**, **List**, **Pivot** (grid cohort), **Form**, **Search**.
- **Alur status:** *New* → *In Progress* → *Answered* / *Closed*.
- **Cara isi (backend):**
  1. Klik **New**.
  2. Isi **Request Title** (judul permohonan), **Description**, dan data pemohon (bisa pilih **Requester** dari kontak, atau isi nama/email/telepon langsung).
  3. Pada tab **Prayer Sessions**, tambahkan sesi doa: **Date & Time**, **Prayers** (pilih kontak yang mendoakan), dan **Notes**.
  4. **Save**, lalu proses lewat tombol: **Start Praying** → **Mark Answered** → **Close**.
- **Form publik:** Jemaat/publik bisa mengirim permohonan lewat halaman website **`/church-pray`** (tanpa login). Permohonan masuk otomatis ke daftar Pray Requests.
- Otomatis tampil di **Church Calendar** dan di **Dashboard** (kartu statistik + pintasan).

### 4.6 Church Calendar (Kalender Kegiatan Gereja)
- **Fungsi:** Satu kalender terpadu berisi semua kegiatan gereja.
- **Layar:** **Kalender** (harian/mingguan/bulanan).
- **Isi otomatis dari:** Ibadah/Event, Jadwal Musisi, Pendaftaran Baptis, Pendaftaran Pernikahan, dan Permohonan Doa.
- **Cara pakai:**
  1. Buka **Operations → Church Calendar**.
  2. Ganti tampilan hari/minggu/bulan.
  3. Warna menunjukkan jenis kegiatan (event, musisi, baptis, pernikahan).
  4. Klik kegiatan untuk melihat detail.
- Data di-refresh otomatis setiap hari (ada cron harian); tombol **Refresh** tersedia untuk pembaruan manual.

### 4.7 Kalender Publik di Website (Public Church Calendar)
- **Fungsi:** Menampilkan kalender kegiatan gereja di **website publik** — dapat diakses tanpa login.
- **URL:** `/church-calendar` (mis. `https://www.situs-anda.id/church-calendar`).
- **Isi:** Semua kegiatan yang **sudah dikonfirmasi** — *Event/Ibadah*, *Baptis*, *Pernikahan*, *Care Cell*, dan *Permohonan Doa*.
  - Hanya status **Approved** dan **Completed** yang tampil (draft/review/dibatalkan disembunyikan).
  - **Jadwal Musisi tidak ditampilkan** di halaman publik.
- **Fitur:**
  1. **Filter berdasarkan jenis** — tab *All*, *Church Event*, *Baptism*, *Marriage*, *Care Cell*, *Pray Request*.
  2. **Pengelompokan** — *By Month* (per bulan) atau *By Type* (per jenis).
  3. **Legenda warna** dan jumlah total kegiatan.
- **Cara akses:** Buka menu **Church Calendar** di navigasi website, atau kunjungi langsung `/church-calendar`.

### 4.8 Berita Kristen di Website (Christianity News)
- **Fungsi:** Menampilkan berita / artikel Kristen dari berbagai sumber terpercaya di **website publik**, dapat diakses tanpa login.
- **URL:** `/christianity-news` (mis. `https://www.situs-anda.id/christianity-news`).
- **Menu navigasi:** item **"Christianity News"** muncul di menu utama website.
- **Halaman beranda:** terdapat bagian **"Christianity News"** (dengan tombol **Read Christianity News**) yang menautkan ke halaman ini.
- **Isi:** Artikel dikelompokkan per kategori (*World, Church & Faith, Theology & Opinion, Culture & Society*, dst.), bersumber dari umpan RSS yang dikelola di backend (**Christianity News → Sources / Articles / Categories**).
- **Fitur:**
  1. Tab filter kategori.
  2. Kartu artikel (judul, sumber, tanggal, ringkasan, tag) dengan tautan **"Read article"** ke sumber asli.

### 4.9 Halaman Beranda Website & SEO
- **Beranda (`/`):** menampilkan bagian hero, *What We Offer* (fitur modul), *Church Calendar*, dan *Come As You Are*.
- **SEO:** halaman utama memiliki **SEO title**, **meta description**, dan **meta keywords** (mis. "church management", "free church software", "modern church", "digital church") yang dapat disesuaikan.

---

## 5. Kontak / Jemaat (Contacts)

Modul menambah kolom gereja pada layar **Contacts** (Kontak) standar Odoo.

**Kolom tambahan:**
- **Church Member Type** — tipe keanggotaan.
- **Care Cell** — kelompok sel.
- **Musician Role** — tampil hanya jika tipe anggota = *Musisi*.
- *(internal)* **Is Pastor** — otomatis True jika tipe anggota = *Pastur*.

**Cara isi:**
1. Buka **Contacts** → buat/ubah kontak.
2. Isi **Church Member Type** dan **Care Cell**.
3. Jika tipe = *Musisi*, pilih **Musician Role**.
4. **Save**.

---

## 6. Ibadah / Event

- **Fungsi:** Mencatat jadwal ibadah & kegiatan (Ibadah Minggu, Persekutuan Doa, Retret, dst.).
- **Layar:** List + Form + **Roster** (jadwal petugas) + **Event Status** (Upcoming/Ongoing/Finished).
- **Cara isi:** New → isi **Name**, **Date Begin/End** → Save. Tambahkan petugas lewat tab **Service Roster**.
- Otomatis tampil di Kalender Kegiatan Gereja.

---

## 7. Leads & Donasi (CRM / Akuntansi)

- **CRM Leads:** Lead/calon jemaat dapat memuat data sakramen (tampilan Kanban khusus sakramen tersedia).
- **Payments (Pembayaran/Donasi):** pembayaran persembahan tercatat; jenis persembahan mengacu pada **Donation Types**.

---

## 8. Alur Kerja & Status

Semua pendaftaran (Baptis & Pernikahan) memakai alur kerja yang sama:

```
Draft → Under Review → Approved → Completed
            ↘        Cancelled        ↗
```

| Status | Arti |
|---|---|
| **Draft** | Baru dibuat, belum diajukan. |
| **Under Review** | Sedang ditinjau. |
| **Approved** | Disetujui. |
| **Completed** | Selesai dilaksanakan. |
| **Cancelled** | Dibatalkan. |

---

## 9. Cara Cepat Mengisi Data (Ringkasan)

| Data | Menu | Langkah Singkat |
|---|---|---|
| Tipe anggota baru | Master Data → Member Types | New → Name → Save |
| Kontak jemaat | Contacts | New → isi data + Member Type / Care Cell |
| Jadwal ibadah | Ibadah (Event) | New → Name + Tanggal → Save |
| Petugas ibadah | Operations → Event Rosters | New → Event + Role + Petugas → Save |
| Jadwal musisi | Operations → Musician Schedule | New → Musisi + Peran + Waktu → Save |
| Pendaftaran baptis | Operations → Baptism Registrations | New → Partner + Tanggal + Petugas → Save → Approve |
| Pendaftaran nikah | Operations → Marriage Registrations | New → Mempelai + Tanggal + Petugas → Save → Approve |
| Permohonan doa (backend) | Operations → Pray Requests | New → Judul + Pemohon + Sesi Doa → Save |
| Permohonan doa (publik) | Website → /church-pray | Isi form → Submit |
| Lihat semua kegiatan | Operations → Church Calendar | (otomatis) |
| Lihat kalender publik (tanpa login) | Website → /church-calendar | (otomatis) |
| Baca berita Kristen (publik) | Website → /christianity-news | (otomatis) |
| Ringkasan angka | Dashboard | (otomatis) |

---

## 10. Tips & Hal yang Perlu Diperhatikan

- **Officiating Minister** hanya bisa memilih kontak dengan tipe anggota **Pastur** — pastikan tipe tersebut sudah diisi pada kontak petugas.
- **Musician Role** hanya tampil jika tipe anggota kontak = **Musisi**.
- Semua kegiatan otomatis masuk **Church Calendar** — tidak perlu input ganda.
- **Permohonan doa** otomatis masuk **Church Calendar**; kirim lewat form publik di **`/church-pray`** tanpa login.
- **Berita Kristen** tersedia di **`/christianity-news`** dan ditautkan dari **beranda** serta **menu website**.
- **Halaman beranda** dan halaman publik memiliki **SEO** yang dapat disesuaikan agar mudah ditemukan di mesin pencari.
- Data sample (contoh) sudah disediakan agar mudah berlatih.
- Pastikan pengguna mendapat akses menu yang sesuai dari administrator melalui
  **Settings → Users → Access Rights** (kategori **Church Management**): grup
  **Read Only**, **Write Only**, atau **Full Access**. Tanpa salah satu grup ini,
  menu **Church Management** tidak akan muncul.

---

*Dokumen ini dapat digunakan sebagai kerangka slide untuk presentasi modul Church Management.*
