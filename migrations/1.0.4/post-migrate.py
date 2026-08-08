# -*- coding: utf-8 -*-
"""Post-migration 1.0.4: backfill care cell status/color + Church Calendar.

Kenapa perlu migration, bukan post_init_hook:
- post_init_hook hanya dijalankan saat INSTALL, BUKAN saat upgrade modul.
- Akibatnya backfill untuk record care cell yang SUDAH ADA tidak pernah
  dieksekusi pada upgrade (terbukti: color NULL, status kosong, 0 baris
  church.activity untuk care cell meski versi modul sudah naik).
- Script post-migrate DIJAMIN berjalan saat upgrade.

Yang dilakukan:
1. Status bervariasi untuk sampel care cell (agar warna terlihat).
2. Status Proposal untuk care cell lain yang masih kosong.
3. Paksa hitung & simpan warna (color) dari status.
4. Rebuild Church Calendar lalu pastikan setiap care cell tersinkron.
"""

from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    CareCell = env['church.care.cell']
    Status = env['church.care.cell.status']
    Activity = env['church.activity']

    # 1) Sampel care cell -> status bervariasi agar warna terlihat.
    sample_status = {
        'church_management.care_cell_1': 'proposal',
        'church_management.care_cell_2': 'review',
        'church_management.care_cell_3': 'approved',
        'church_management.care_cell_4': 'running',
        'church_management.care_cell_5': 'pending',
    }
    for xml_id, code in sample_status.items():
        cell = env.ref(xml_id, raise_if_not_found=False)
        status = Status.search([('code', '=', code)], limit=1)
        if cell and status and cell.status_id.id != status.id:
            cell.status_id = status.id

    # 2) Care cell lain tanpa status -> Proposal.
    proposal = Status.search([('code', '=', 'proposal')], limit=1)
    for cell in CareCell.search([('status_id', '=', False)]):
        if proposal:
            cell.status_id = proposal.id

    # 3) Paksa warna terhitung & tersimpan untuk SEMUA care cell.
    CareCell.search([])._compute_color()

    # 4) Rebuild Church Calendar lalu pastikan care cell tersinkron.
    Activity.regenerate()
    for cell in CareCell.search([]):
        Activity._sync_from_care_cell(cell)
