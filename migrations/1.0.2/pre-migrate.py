"""Pre-migration 1.0.2: backfill start_date pada church_care_cell.

start_date menjadi REQUIRED. Baris lama yang sudah ada (dari instalasi
sebelumnya) masih NULL sehingga Odoo tidak bisa set NOT NULL pada kolom
(muncul warning: "unable to set NOT NULL on column 'start_date'").

Pre-migrate dijalankan SEBELUM skema diperbarui, jadi isi dulu nilai NULL
dengan CURRENT_DATE sebagai default agar constraint NOT NULL dapat diterapkan.
Idempoten: hanya menyentuh baris dengan start_date IS NULL.
"""


def migrate(cr, version):
    cr.execute("""
        UPDATE church_care_cell
        SET start_date = CURRENT_DATE
        WHERE start_date IS NULL
    """)
