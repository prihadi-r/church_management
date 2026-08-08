"""Pre-migration 1.0.1: konversi data Baptism ke struktur baru.

Perubahan struktur model:
- baptism_date + baptism_time  ->  baptism_datetime (SATU field DateTime)
- father_name / mother_name    ->  father_id / mother_id (Many2one res.partner)
- name (Char)                  ->  terkait (related) ke partner_id (res.partner)

Pre-migrate dijalankan SEBELUM skema model diperbarui, sehingga kolom lama
masih dapat dibaca.
"""


def migrate(cr, version):
    # Kolom relasi baru (belum ada sebelum model update)
    cr.execute(
        "ALTER TABLE church_baptism_registration "
        "ADD COLUMN IF NOT EXISTS father_id integer"
    )
    cr.execute(
        "ALTER TABLE church_baptism_registration "
        "ADD COLUMN IF NOT EXISTS mother_id integer"
    )

    # 1) Gabungkan tanggal + jam ke SATU kolom baptism_datetime
    cr.execute("""
        UPDATE church_baptism_registration
        SET baptism_datetime = baptism_date + (COALESCE(baptism_time, 0) * interval '1 hour')
        WHERE baptism_date IS NOT NULL
    """)

    # 2) Candidate -> res.partner (buat contact baru bila belum ada)
    cr.execute("""
        INSERT INTO res_partner (name, create_uid, create_date, write_uid, write_date)
        SELECT DISTINCT br.name, 1, now(), 1, now()
        FROM church_baptism_registration br
        WHERE br.partner_id IS NULL
          AND br.name IS NOT NULL
          AND NOT EXISTS (SELECT 1 FROM res_partner rp WHERE rp.name = br.name)
    """)
    cr.execute("""
        UPDATE church_baptism_registration br
        SET partner_id = rp.id
        FROM res_partner rp
        WHERE br.partner_id IS NULL
          AND rp.name = br.name
    """)

    # 3) Ayah & ibu -> res.partner (father_id / mother_id)
    for src, tgt in (('father_name', 'father_id'), ('mother_name', 'mother_id')):
        cr.execute(f"""
            INSERT INTO res_partner (name, create_uid, create_date, write_uid, write_date)
            SELECT DISTINCT br.{src}, 1, now(), 1, now()
            FROM church_baptism_registration br
            WHERE br.{tgt} IS NULL
              AND br.{src} IS NOT NULL
              AND NOT EXISTS (SELECT 1 FROM res_partner rp WHERE rp.name = br.{src})
        """)
        cr.execute(f"""
            UPDATE church_baptism_registration br
            SET {tgt} = rp.id
            FROM res_partner rp
            WHERE br.{tgt} IS NULL
              AND rp.name = br.{src}
        """)
