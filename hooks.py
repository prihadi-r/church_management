# -*- coding: utf-8 -*-
"""Module hooks untuk church_management."""


def post_init_hook(env):
    """Jalankan saat install DAN setiap upgrade modul.

    1. Buat cron refresh kalender kegiatan gereja secara idempotent.
    2. Rebuild kalender (church.activity) dari seluruh data terkini.

    Dibuat via hook (bukan data XML) agar berjalan di setiap upgrade
    (data noupdate="1" tidak dijalankan ulang saat upgrade) dan tidak
    bergantung pada resolusi external id model (model_...) saat loading.
    """
    # 1) Cron harian (idempotent)
    # Catatan Odoo 17/18: ir.cron mendelegasikan state/code/model_id ke
    # ir.actions.server (via ir_actions_server_id). Field 'numbercall'
    # sudah TIDAK ADA di Odoo 18 — jangan dipakai.
    cron = env['ir.cron'].search(
        [('name', '=', 'Church Activity Calendar: Refresh')], limit=1)
    if not cron:
        env['ir.cron'].create({
            'name': 'Church Activity Calendar: Refresh',
            'model_id': env['ir.model']._get('church.activity').id,
            'state': 'code',
            'code': 'model.regenerate()',
            'interval_number': 1,
            'interval_type': 'days',
            'active': True,
        })

    # 2) Rebuild kalender dari data terkini (event, musisi, baptis, nikah,
    #    care cell)
    env['church.activity'].regenerate()

    # 3) Pastikan kontak sampel yang menjadi Officiating Minister (pastor)
    #    memiliki church member type = Pastur. Tanpa ini, field Officiating
    #    Minister pada record marriage yang SUDAH ADA tidak akan tampil
    #    karena is_pastor=False (rekaman sampel noupdate="1" tidak di-update
    #    saat upgrade). Idempoten: menulis nilai yang sama berulang kali aman.
    pastor_type = env.ref('church_management.member_type_14', raise_if_not_found=False)
    partner_ids = []
    for xml_id in ('church_management.res_partner_3', 'church_management.res_partner_4'):
        partner = env.ref(xml_id, raise_if_not_found=False)
        if partner:
            partner_ids.append(partner.id)
    if pastor_type and partner_ids:
        partners = env['res.partner'].browse(partner_ids)
        partners.write({'church_member_type_id': pastor_type.id})
        # Paksa recompute field stored is_pastor (res.partner & marriage)
        # agar nilai tersimpan pada record yang SUDAH ADA langsung benar.
        partners._compute_is_pastor()
        env['church.marriage.registration'].search([])._compute_is_pastor()

    # 4) Pastikan ada record dashboard tunggal (landing page Church Management)
    if not env['church.dashboard'].search([], limit=1):
        env['church.dashboard'].create({'name': 'Church Management Dashboard'})
