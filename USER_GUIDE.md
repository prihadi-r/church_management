# ⛪ Darash — Panduan Penggunaan (User Guide)

> Modul manajemen gereja pada Odoo 18. Dokumen ini menjelaskan fungsi setiap menu, layar yang tersedia, dan cara pengisian data. Disusun untuk bahan presentasi di gamma.app.

---

## 1. Ringkasan Modul

**Apa itu Church Management?**
- Modul Odoo 18 untuk mengelola kegiatan dan data gereja dalam satu aplikasi.
- Mengelola **keanggotaan jemaat**, **baptis**, **pernikahan**, **jadwal ibadah**, **pelayanan musik**, **sekolah minggu (Sunday School)**, **misi (Mission)**, **permohonan doa**, dan **kalender kegiatan gereja** secara terpadu.

**Manfaat Utama**
- Semua data tersimpan di satu database (tidak perlu buku fisik).
- Setiap kegiatan (ibadah, baptis, nikah, jadwal musisi, sesi sekolah minggu) otomatis tampil di **satu Kalender Kegiatan Gereja**.
- **Dashboard** dibuat dengan **Odoo Dashboards** (`board`): halaman utama berisi kotak-kotak **grafik** (bar & pie) yang ringkas, bukan tabel angka panjang.
- Alur kerja (workflow) dengan status: antrian → disetujui → selesai.
- Modul **Sekolah Minggu** lengkap: kelas, guru, murid, sesi pertemuan, dan kehadiran.
- Modul **Misi** lengkap: perjalanan misi, misionaris, peserta, dukungan dana, dan dashboard grafiknya sendiri.
- **Mobile API** untuk aplikasi **Flutter**: data **kalender kegiatan** dan **ringkasan dashboard misi** tersedia sebagai JSON dengan autentikasi **kunci API** (lihat **Bagian 13**).

**Struktur Menu**
```
Church Management
├── Dashboard (halaman utama — papan grafik)
├── Master Data
│   ├── Member Types
│   ├── Care Cells
│   ├── Donation Types
│   ├── Sacrament Types
│   ├── Event Roles
│   └── Musician Roles
├── Sunday School
│   ├── Classes
│   ├── Teachers
│   ├── Students
│   ├── Sessions
│   ├── Attendance
│   └── Configuration
│       ├── Class Levels
│       ├── Teacher Roles
│       ├── Class Statuses
│       ├── Student Statuses
│       ├── Attendance Statuses
│       └── Session Statuses
├── Mission
│   ├── Dashboard (papan grafik misi)
│   ├── Mission Trips
│   ├── Missionaries
│   ├── Participants
│   ├── Mission Support
│   └── Configuration
│       ├── Mission Fields
│       ├── Mission Types
│       ├── Mission Statuses
│       ├── Mission Roles
│       ├── Missionary Statuses
│       └── Mission Agencies
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

**Fungsi:** Halaman utama berupa **papan dashlet** dari aplikasi **Dashboards** milik Odoo (`board`). Setiap kotak berisi **grafik** yang bisa langsung dibaca, sehingga tidak perlu membaca tabel angka yang panjang.

**Delapan kotak grafik (dashlet):**

| Kotak | Isi | Jenis grafik |
|---|---|---|
| **Jemaat** | Jumlah jemaat per tipe anggota (Simpatisan, Jemaat Tetap, Musisi, Pastur, ...) | Bar |
| **Baptis** | Pendaftaran baptis per bulan | Bar |
| **Pernikahan** | Pendaftaran pernikahan per bulan | Bar |
| **Doa** | Permohonan doa per status (New, In Progress, Answered, Closed) | Pie |
| **Murid** | Jumlah murid sekolah minggu per kelas | Bar |
| **Sesi** | Jumlah sesi sekolah minggu per kelas | Bar |
| **Kehadiran** | Kehadiran sekolah minggu per status (Present, Late, Permission, Sick, Absent) | Pie |
| **Care Cell** | Care cell per status (Proposal, Review, Approved, Running, Pending) | Pie |

**Cara pakai:**
1. Buka menu **Church Management → Dashboard**.
2. Di dalam setiap kotak ada tombol **Measures** dan ikon jenis grafik (bar / line / pie / list) — klik untuk mengganti tampilan atau ukuran yang dihitung.
3. Tombol **Change Layout** (kanan atas) mengubah susunan kolom dashboard.
4. Ikon **— / ☐** pada judul kotak melipat atau membuka kembali kotak; ikon **×** menyembunyikan kotak dari dashboard Anda.

> 💡 **Tip:** Grafik **Jemaat** hanya menghitung kontak yang punya **Member Type**. Kontak tanpa tipe anggota (mis. murid dan guru sekolah minggu) tidak ikut dihitung, sehingga angka "Jemaat" tetap akurat.
>
> 💡 **Tip:** Susunan dashboard bersifat **per pengguna** — perubahan yang Anda lakukan (melipat, menyembunyikan, mengubah grafik) tidak memengaruhi pengguna lain.

---

## 3. Master Data (Data Dasar)

Master Data berisi daftar istilah / kategori yang dipakai di seluruh modul. Semua layarnya sama: **Daftar (List)** dan **Form Isian**.

### 3.1 Member Types (Tipe Anggota)
- **Fungsi:** Kategori keanggotaan jemaat.
- **Layar:** List + Form.
- **Cara isi:** Klik **New** → isi **Name** (contoh: *Simpatisan, Jemaat Tetap, Musisi, Pastur, Pendoa* dst.) → **Save**.
- **Penting:** Tipe *Musisi* membuat field "Musician Role" muncul di Kontak; tipe *Pastur* membuat kontak bisa dipilih sebagai petugas (Officiating Minister) di Baptis & Pernikahan.

### 3.2 Care Cells (Kelompok Sel / Komsel)
- **Fungsi:** Mengelola kelompok sel (komsel) beserta anggotanya, sesi pertemuan, dan statusnya.
- **Layar:** **Kanban** (kartu dikelompokkan per status), **Kalender**, **List**, **Form**, **Search**.
- **Cara isi:**
  1. Klik **New**.
  2. Isi **Name** (nama komsel), **Leader** (ketua kelompok), **Status** (*Proposal / Review / Approved / Running / Pending / Cancel*), **Start Date**, dan **End Date**.
  3. Jumlah **Attendees** (anggota) dan **Sessions** (sesi) terisi otomatis; **Next Session Date** otomatis dihitung dari sesi terdekat.
- **Tab Attendees (Anggota):** tambahkan kontak anggota dengan **Role** (*Leader / Member / Guest*), **Joined Date**, dan **Notes**.
- **Tab Sessions (Pertemuan):** catat tiap pertemuan: **Name** (judul), **Date** (tanggal), **Plan** (rencana), dan **Note** (catatan).
- **Kalender:** komsel tampil pada tampilan kalender sesuai rentang **Start Date → End Date**.
- **Search:** filter **Active Now**, **Upcoming**, dan per status; dapat dikelompokkan berdasarkan **Status** atau **Leader**.
- Otomatis tampil di **Kalender Kegiatan Gereja** (Church Calendar) dan di kalender publik website.

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
- Otomatis tampil di **Church Calendar** dan di **Dashboard** (kotak grafik **Doa**).

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

## 5. Sunday School (Sekolah Minggu)

Menu **Church Management → Sunday School** mengelola kelas, guru, murid, sesi pertemuan, dan kehadiran sekolah minggu.

> ℹ️ **Murid dan guru adalah Kontak.** Keduanya memakai *delegation inheritance* (`_inherits`) ke `res.partner`, jadi nama, telepon, e-mail, dan alamat diambil langsung dari layar **Contacts** — tidak perlu diisi dua kali.

### 5.1 Classes (Kelas)
- **Fungsi:** Data kelas sekolah minggu.
- **Layar:** **Kanban** (dikelompokkan per status), **List**, **Form**, **Search**.
- **Cara isi:**
  1. Klik **New**.
  2. Isi **Class Name** (wajib), **Code**, **Sequence**.
  3. Pilih **Class Level** (wajib) — daftar dari *Configuration → Class Levels*: *Toddler, Kindergarten, Primary, Teen, Youth*.
  4. Pilih **Status** (*Planned / Running / Completed / Cancelled*) dan **Head Teacher**.
  5. Isi **Room**, **Weekly Meeting Time** (mis. `07:30`), **Start Date**, **End Date**, **Capacity**.
  6. **Save**.
- **Tab Students** — murid yang terdaftar di kelas ini.
- **Tab Teachers** — guru pengajar beserta **Role**-nya.
- **Tab Sessions** — sesi pertemuan kelas.
- Angka **Students**, **Teachers**, **Sessions**, dan **Next Session** dihitung otomatis.

### 5.2 Teachers (Guru)
- **Fungsi:** Data guru sekolah minggu.
- **Layar:** List + Form.
- **Cara isi:**
  1. Klik **New** → pilih **Contact** (kontak jemaat yang sudah ada).
  2. Isi **Serving Since** dan **Notes** → **Save**.
- **Tab Class Assignments:** tambahkan kelas yang diajar beserta **Role**:
  - **Supervisor**, **Head Teacher**, **Assistant Teacher**, **Substitute Teacher**.
  - Satu guru boleh mengajar beberapa kelas dengan peran berbeda.

### 5.3 Students (Murid)
- **Fungsi:** Data murid sekolah minggu.
- **Layar:** List + Form.
- **Cara isi:**
  1. Klik **New** → pilih **Contact**.
  2. Isi **Birth Date** (umur dihitung otomatis), **Class**, **Status**, **Enrollment Date**, dan **Parent / Guardian**.
  3. **Save** — **Student Code** dibuat otomatis dengan format `SS/2026/0001`.
- **Tab Attendance** menampilkan riwayat kehadiran; **Attendance Rate (%)** dihitung otomatis.

### 5.4 Sessions (Sesi Pertemuan)
- **Fungsi:** Mencatat pertemuan kelas (topik/materi per minggu).
- **Layar:** List + Form.
- **Cara isi:**
  1. Klik **New** → pilih **Class** dan **Teacher**.
  2. Isi **Topic** (nama sesi), **Start**, **End**, dan **Status** (*Planned / In Progress / Done / Cancelled*).
  3. Isi **Lesson Summary** / **Notes** bila perlu → **Save**.
- Setiap sesi otomatis masuk ke **Church Calendar**.

### 5.5 Attendance (Kehadiran)
- **Fungsi:** Mencatat kehadiran murid pada tiap sesi.
- **Cara isi:**
  1. Buka salah satu **Session** → tab **Attendance** → **Add a line**.
  2. Pilih **Student** dan **Attendance Status**:
     - **Present** dan **Late** dihitung *hadir*;
     - **Permission**, **Sick**, dan **Absent** dihitung *tidak hadir*.
  3. **Save**.
- Rekap **Present**, **Absent**, dan **Attendance Rate** pada murid maupun kelas ter-update otomatis.

### 5.6 Configuration (Pengaturan)
- **Class Levels** — jenjang kelas (Toddler, Kindergarten, Primary, Teen, Youth).
- **Teacher Roles** — peran guru (Supervisor, Head Teacher, Assistant Teacher, Substitute Teacher).
- **Class Statuses** — status kelas (Planned, Running, Completed, Cancelled).
- **Student Statuses** — status murid (Active, Graduated, Withdrawn, Inactive).
- **Attendance Statuses** — status kehadiran beserta opsi **Counts as Present**.
- **Session Statuses** — status sesi (Planned, In Progress, Done, Cancelled).

> 💡 **Tip:** Data contoh sudah tersedia: **5 kelas** (Toddler, Kindergarten, Primary, Teen, Youth) dengan **20 murid per kelas** bernama asli, **12 guru**, serta **sesi dan catatan kehadiran** — buka **Sunday School → Classes** untuk melihatnya.

---

## 6. Mission (Misi)

Menu **Church Management → Mission** mengelola **perjalanan misi**, **misionaris**, **peserta**, dan **dukungan dana (mission support)**.

> ℹ️ **Semua orang adalah Kontak, semua perjalanan adalah Event.** Misionaris, peserta, dan lembaga pengirim memakai *delegation inheritance* (`_inherits`) ke `res.partner`; perjalanan misi (`church.mission.trip`) mewarisi `event.event`. Jadi data otomatis muncul di aplikasi **Contacts** dan **Events**, serta di **Church Calendar**.
>
> ℹ️ **Tidak ada selection field.** Semua status, jenis misi, wilayah, dan peran peserta adalah **master data** yang bisa ditambah sendiri lewat menu **Configuration**.

### 6.1 Dashboard (Mission)
- **Fungsi:** ringkasan grafik khusus misi (papan dashlet Odoo `board`).
- **Delapan kotak grafik:**

| Kotak | Isi | Jenis grafik |
|---|---|---|
| **Missions by Status** | Perjalanan misi per status (Planned, Ongoing, Completed, Cancelled) | Pie |
| **Missions by Type** | Perjalanan misi per jenis (Evangelism, Medical, Education, ...) | Bar |
| **Missions by Field** | Perjalanan misi per wilayah misi | Bar |
| **Missionaries** | Misionaris per status (Candidate, Preparing, On the Field, Furlough, Completed) | Pie |
| **Participants** | Peserta per peran (Team Leader, Medical, Logistics, ...) | Pie |
| **Support per Month** | Total dukungan dana per bulan | Bar |
| **Support per Missionary** | Total dukungan dana per misionaris | Bar |
| **Support by Donation Type** | Dukungan dana per jenis donasi | Pie |

- **Cara pakai:** sama seperti Dashboard utama — tombol **Measures** untuk mengganti ukuran, **Change Layout** untuk susunan kolom, dan ikon **×** untuk menyembunyikan kotak (per pengguna).

### 6.2 Mission Trips (Perjalanan Misi)
- **Fungsi:** Data perjalanan misi (outreach, medis, penanaman gereja, dsb.).
- **Layar:** **Kanban** (dikelompokkan per status), **List**, **Calendar**, **Form**, **Search**.
- **Cara isi:**
  1. Klik **New**.
  2. Isi **Mission Trip** (nama) serta **Start Date** dan **End Date** (wajib — ini tanggal Event).
  3. Pilih **Mission Type**, **Mission Field**, **Sending Agency**, dan **Trip Leader**.
  4. Pilih **Venue** dan isi **Budget**.
  5. **Save** — **Trip Code** dibuat otomatis (`MT/2026/0001`).
- **Status** diubah dari status bar: **Planned → Ongoing → Completed** (atau **Cancelled**).
- **Support Received** dan **Funding Progress (%)** dihitung otomatis dari tab **Support**.
- **Tab Participants** — anggota tim + peran dan konfirmasi.
- **Tab Support** — donasi untuk perjalanan ini (dengan tombol **Total**).
- **Tab Description / Notes** — tujuan kegiatan dan catatan internal.
- Karena merupakan Event, perjalanan misi otomatis tampil di **Events** dan **Church Calendar**.

### 6.3 Missionaries (Misionaris)
- **Fungsi:** Data misionaris beserta wilayah, lembaga pengirim, status, dan target dukungan.
- **Layar:** **Kanban** (per status), **List**, **Form**.
- **Cara isi:**
  1. Klik **New** → pilih **Contact** (atau buat kontak baru).
  2. Pilih **Mission Field**, **Sending Agency**, **Status**, dan **Supervisor**.
  3. Isi **Ministry Start / End**, **Support Target**.
  4. Lengkapi **Contact Details** (jabatan, telepon, e-mail, alamat) → **Save**.
- **Missionary Code** otomatis (`MSN/2026/0001`).
- **Support Received** dan **Support Progress (%)** dihitung otomatis dari donasi pada tab **Support**.
- **Tab Led Mission Trips** menampilkan perjalanan yang dipimpin misionaris ini.

### 6.4 Participants (Peserta Misi)
- **Fungsi:** Anggota tim pada satu perjalanan misi.
- **Layar:** **List**, **Kanban** (per perjalanan), **Form**.
- **Cara isi:**
  1. Klik **New** → pilih **Contact** dan **Mission Trip**.
  2. Pilih **Role** (Team Leader, Team Member, Medical Personnel, Teacher, Logistics, Intercessor).
  3. Isi **Registration Date** dan centang **Confirmed** bila sudah pasti ikut.
  4. **Save**.
- Satu kontak hanya boleh terdaftar **sekali** pada perjalanan yang sama.
- Peserta juga bisa ditambahkan langsung dari tab **Participants** pada form perjalanan.

### 6.5 Mission Support (Dukungan Dana)
- **Fungsi:** Mencatat donasi/support untuk misionaris maupun perjalanan misi.
- **Layar:** **List**, **Pivot**, **Form**.
- **Cara isi:**
  1. Klik **New** → pilih **Donor** (kontak) dan **Date**.
  2. Isi **Amount** dan pilih **Donation Type** (master yang sama dengan persembahan gereja).
  3. Pilih **Missionary** dan/atau **Mission Trip** (minimal salah satu).
  4. (Opsional) pilih **Accounting Payment** bila donasi sudah tercatat di akuntansi.
  5. **Save** — referensi otomatis (`MSP/2026/0001`).
- **Pivot** menganalisis total dukungan per misionaris/perjalanan per bulan.

### 6.6 Configuration (Pengaturan Misi)
- **Mission Fields** — wilayah/medan misi (Jabodetabek, Sumatra, Kalimantan, Nusa Tenggara, Papua, Southeast Asia), bisa bertingkat.
- **Mission Types** — jenis misi (Evangelism, Church Planting, Medical Mission, Education & Literacy, Disaster Relief, Community Development).
- **Mission Statuses** — status perjalanan (Planned, Ongoing, Completed, Cancelled) + penanda **Closed Status**.
- **Mission Roles** — peran peserta (Team Leader, Team Member, Medical Personnel, Teacher, Logistics, Intercessor).
- **Missionary Statuses** — status misionaris (Candidate, Preparing, On the Field, Furlough, Completed).
- **Mission Agencies** — lembaga pengirim; setiap agency adalah **perusahaan di Contacts**.

> 💡 **Tip:** Data contoh sudah tersedia: **2 lembaga misi**, **5 misionaris**, **5 perjalanan misi** (Juli–Desember 2026), **9 peserta**, dan **8 baris dukungan dana** — buka **Mission → Mission Trips** atau **Mission → Dashboard** untuk melihatnya.

---

## 7. Kontak / Jemaat (Contacts)

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

## 8. Ibadah / Event

- **Fungsi:** Mencatat jadwal ibadah & kegiatan (Ibadah Minggu, Persekutuan Doa, Retret, dst.).
- **Layar:** List + Form + **Roster** (jadwal petugas) + **Event Status** (Upcoming/Ongoing/Finished).
- **Cara isi:** New → isi **Name**, **Date Begin/End** → Save. Tambahkan petugas lewat tab **Service Roster**.
- Otomatis tampil di Kalender Kegiatan Gereja.

---

## 9. Leads & Donasi (CRM / Akuntansi)

- **CRM Leads:** Lead/calon jemaat dapat memuat data sakramen (tampilan Kanban khusus sakramen tersedia).
- **Payments (Pembayaran/Donasi):** pembayaran persembahan tercatat; jenis persembahan mengacu pada **Donation Types**.

---

## 10. Alur Kerja & Status

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

## 11. Cara Cepat Mengisi Data (Ringkasan)

| Data | Menu | Langkah Singkat |
|---|---|---|
| Tipe anggota baru | Master Data → Member Types | New → Name → Save |
| Kelompok sel (komsel) | Master Data → Care Cells | New → Name + Leader + Status + Tanggal → Save |
| Anggota komsel | Master Data → Care Cells → tab Attendees | Tambah → Kontak + Peran + Tanggal gabung → Save |
| Sesi pertemuan komsel | Master Data → Care Cells → tab Sessions | Tambah → Judul + Tanggal + Rencana → Save |
| Kontak jemaat | Contacts | New → isi data + Member Type / Care Cell |
| Jadwal ibadah | Ibadah (Event) | New → Name + Tanggal → Save |
| Petugas ibadah | Operations → Event Rosters | New → Event + Role + Petugas → Save |
| Jadwal musisi | Operations → Musician Schedule | New → Musisi + Peran + Waktu → Save |
| Pendaftaran baptis | Operations → Baptism Registrations | New → Partner + Tanggal + Petugas → Save → Approve |
| Pendaftaran nikah | Operations → Marriage Registrations | New → Mempelai + Tanggal + Petugas → Save → Approve |
| Permohonan doa (backend) | Operations → Pray Requests | New → Judul + Pemohon + Sesi Doa → Save |
| Permohonan doa (publik) | Website → /church-pray | Isi form → Submit |
| Kelas sekolah minggu | Sunday School → Classes | New → Nama + Level + Status + Head Teacher → Save |
| Guru sekolah minggu | Sunday School → Teachers | New → Contact + Serving Since → Save → tab Class Assignments |
| Murid sekolah minggu | Sunday School → Students | New → Contact + Tanggal Lahir + Kelas → Save |
| Sesi sekolah minggu | Sunday School → Sessions | New → Kelas + Guru + Topik + Waktu → Save |
| Kehadiran murid | Sunday School → Sessions → tab Attendance | Add a line → Murid + Status → Save |
| Perjalanan misi | Mission → Mission Trips | New → Nama + Tanggal + Type + Field + Leader → Save |
| Misionaris | Mission → Missionaries | New → Contact + Field + Agency + Support Target → Save |
| Peserta misi | Mission → Participants | New → Contact + Mission Trip + Role → Save |
| Dukungan misi | Mission → Mission Support | New → Donor + Date + Amount + Missionary/Trip → Save |
| Ringkasan misi (grafik) | Mission → Dashboard | (otomatis) |
| Lihat semua kegiatan | Operations → Church Calendar | (otomatis) |
| Lihat kalender publik (tanpa login) | Website → /church-calendar | (otomatis) |
| Baca berita Kristen (publik) | Website → /christianity-news | (otomatis) |
| Ringkasan grafik | Dashboard | (otomatis) |

---

## 12. Tips & Hal yang Perlu Diperhatikan

- **Officiating Minister** hanya bisa memilih kontak dengan tipe anggota **Pastur** — pastikan tipe tersebut sudah diisi pada kontak petugas.
- **Musician Role** hanya tampil jika tipe anggota kontak = **Musisi**.
- Semua kegiatan otomatis masuk **Church Calendar** — tidak perlu input ganda.
- **Permohonan doa** otomatis masuk **Church Calendar**; kirim lewat form publik di **`/church-pray`** tanpa login.
- **Berita Kristen** tersedia di **`/christianity-news`** dan ditautkan dari **beranda** serta **menu website**.
- **Halaman beranda** dan halaman publik memiliki **SEO** yang dapat disesuaikan agar mudah ditemukan di mesin pencari.
- **Sekolah minggu:** data **murid** dan **guru** memakai **Contacts** (`res.partner`). Mengubah nama/telepon di kontak langsung terlihat di data murid/guru; menghapus kontak juga menghapus data murid/guru terkait.
- **Sesi sekolah minggu** otomatis masuk **Church Calendar**, sama seperti ibadah, baptis, dan nikah.
- **Misi:** misionaris, peserta, dan lembaga pengirim adalah **Contacts** (`res.partner`), sedangkan **perjalanan misi adalah Event** (`event.event`) — mengubah tanggal/venue di Events langsung terlihat di form Mission Trip, dan sebaliknya. Perjalanan misi otomatis muncul di **Church Calendar**.
- **Misi:** status/jenis/wilayah/peran adalah **master data** (bukan pilihan tetap). Tambah data baru di **Mission → Configuration** agar langsung tersedia di semua form.
- **Mission Support:** setiap baris dukungan harus terhubung ke **minimal satu** misionaris atau perjalanan misi; nominal harus lebih besar dari nol.
- **Dashboard bergrafik:** susunan kotak bersifat **per pengguna** (tidak memengaruhi pengguna lain). Gunakan **Change Layout** untuk mengubah jumlah kolom, tombol **Measures** untuk mengganti ukuran/tipe grafik, dan ikon **×** untuk menyembunyikan kotak yang tidak dipakai.
- Data sample (contoh) sudah disediakan agar mudah berlatih, termasuk **56 jemaat** dengan nama Indonesia (mis. *Agus Saputra, Pdt. Paulus Situmorang*) yang terlibat dalam **pernikahan, baptis, dan komsel** untuk rentang **Agustus – Oktober 2026** (bulan berjalan hingga 2 bulan ke depan), beserta **6 komsel** (Komsel Imanuel, Bethel, Elim, Getsemani, Kanaan, Siloam) lengkap dengan anggota dan sesi pertemuannya, serta **5 kelas sekolah minggu** dengan **20 murid per kelas**, **12 guru**, **sesi**, dan **catatan kehadiran**.
- Pastikan pengguna mendapat akses menu yang sesuai dari administrator melalui
  **Settings → Users → Access Rights** (kategori **Church Management**): grup
  **Read Only**, **Write Only**, atau **Full Access**. Tanpa salah satu grup ini,
  menu **Church Management** tidak akan muncul.

---

## 13. Mobile API (Aplikasi Flutter)

Modul menyediakan endpoint **JSON** untuk aplikasi mobile Flutter. Semua endpoint
menggunakan **kunci API** (bukan login web) dan tunduk pada hak akses grup
**Church Management** milik pemilik kunci.

### 13.1 Pengguna & Kunci API

| Langkah | Keterangan |
|---------|------------|
| 1 | Login sebagai pengguna layanan **Mobile API** (login `mobile_api`). Pengguna ini dibuat otomatis saat instalasi dan **tidak punya password**. |
| 2 | Buka **Preferences → Account Security → New API Key**, beri nama (mis. *Flutter app*), lalu salin kuncinya. |
| 3 | Atur hak akses di **Settings → Users → Access Rights** (kategori **Church Management**): **Read Only** (default), **Write Only**, atau **Full Access**. |
| 4 | Kirim setiap permintaan dengan header `X-Api-Key`; header `X-Database` bersifat opsional (harus sama dengan database yang dituju). |

> ℹ️ Kunci API bersifat rahasia. Jika bocor, hapus di **Account Security** lalu buat kunci
> baru. Aplikasi mobile tidak boleh menyimpan kunci di kode sumber.

### 13.2 Endpoint yang Sudah Tersedia

**Kalender gereja** — basis `/api/v1/mobile/calendar`:

| Endpoint | Fungsi |
|----------|--------|
| `GET /activities` | Daftar kegiatan (event, baptis, nikah, komsel, doa, sekolah minggu). Filter: `type`, `state`, `date_from`, `date_to`, `limit` (default 20, maks 100), `offset`. |
| `GET /activities/<id>` | Detail satu kegiatan + sumbernya (`source_type`, `source_model`, `source_id`). |
| `GET /agenda` | Kegiatan dikelompokkan per bulan/hari (`group=day`, default) atau per tipe (`group=type`). |
| `GET /upcoming` | Kegiatan terdekat dari sekarang (`limit` default 5, maks 50) untuk halaman utama. |
| `GET /metrics` | Jumlah kegiatan per tipe dan per bulan untuk grafik. |

**Dashboard misi** — `GET /api/v1/mobile/mission/dashboard/metrics`: kartu KPI
(`active_trips`, `missionaries_in_field`, `total_support_raised`, `upcoming_departures`,
`next_departure`) dan 8 seri grafik yang sama dengan dashboard web Mission.

**Master data misi** — basis `/api/v1/mobile/mission/master`. Parameter `active` menerima
`true` (default, hanya data aktif), `false` (hanya data yang diarsipkan) atau `all` (keduanya):

| Endpoint | Fungsi |
|----------|--------|
| `GET /types` | Jenis misi (`church.mission.type`). |
| `GET /fields` | Medan/wilayah misi (`church.mission.field`) beserta `country` dan `parent`. `limit` (default 50, maks 200), `offset`. |
| `GET /statuses` | Status perjalanan (`trip_statuses`) dan status misionaris (`missionary_statuses`), masing-masing dengan `is_closed`. |
| `GET /roles` | Peran peserta tim misi (`church.mission.role`). |

**Perjalanan misi** — basis `/api/v1/mobile/mission/trips`:

| Endpoint | Fungsi |
|----------|--------|
| `GET /` | Daftar perjalanan misi (status, medan, tanggal, budget, dana terkumpul & progres). Filter: `field_id`, `status_id`, `date_begin`, `date_end` (perjalanan yang **beririsan** dengan rentang tersebut), `limit` (default 20, maks 100), `offset`. |
| `GET /<id>` | Detail satu perjalanan: field `event.event` turunan (deskripsi, venue, seats), budget, leader, organizer/penanggung jawab, jumlah peserta dan total dukungan. |
| `GET /<id>/participants` | Peserta perjalanan beserta nama, telepon, email, peran dan tanggal pendaftaran. Parameter `confirmed`: `true` (default, hanya peserta terkonfirmasi), `false` (menunggu konfirmasi) atau `all`; `limit`/`offset`. |
| `POST /<id>/register` | Mendaftarkan kontak ke perjalanan. Body JSON: `partner_id` (wajib), `role_id`, `notes`. Ditolak `400 validation_error` bila perjalanan sudah berakhir, penuh (`seats_max`), peserta sudah terdaftar, atau kontak/peran tidak ada. Peserta baru berstatus **belum terkonfirmasi**. |

> Kegiatan yang **belum disetujui** (`draft`, `review`, `cancelled`) tidak ditampilkan,
> sama seperti halaman publik `/church-calendar`. Permohonan doa selalu ditampilkan.
> Tanggal dikirim dalam **UTC** (`YYYY-MM-DD HH:MM:SS`); aplikasi yang mengubahnya ke zona
> waktu pengguna.

### 13.3 Format Respons & Kode Error

```json
{ "success": true, "data": { } }

{ "success": false, "error": { "code": "invalid_api_key",
                               "message": "The provided API key is invalid or expired." } }
```

| HTTP | `code` | Arti |
|------|--------|------|
| 401 | `missing_api_key` | Header `X-Api-Key` tidak dikirim. |
| 401 | `invalid_api_key` | Kunci salah, kedaluwarsa, atau penggunanya nonaktif. |
| 403 | `database_mismatch` | `X-Database` tidak cocok dengan database tujuan. |
| 403 | `read_only_access` | Pengguna **Read Only** mencoba `POST`/`PUT`/`PATCH`/`DELETE`. |
| 403 | `access_error` | Hak akses Odoo menolak operasi tersebut. |
| 400 | `validation_error` | Parameter tidak valid (mis. `type` atau tanggal salah format). |
| 404 | `not_found` | Data yang diminta tidak ada. |
| 500 | `internal_error` | Kesalahan tak terduga (detail hanya ada di log server). |

### 13.4 Yang Belum Tersedia

Endpoint **Mission** untuk misionaris/agensi dan dukungan, **Sunday School**, serta ekspor
**iCal** masih dalam rencana — lihat [task.md](task.md). Daftar dan detail perjalanan misi
sudah tersedia (lihat **Bagian 13.2**).

---

*Dokumen ini dapat digunakan sebagai kerangka slide untuk presentasi modul Church Management.*
