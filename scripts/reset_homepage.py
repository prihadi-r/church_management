# -*- coding: utf-8 -*-
# =============================================================================
# reset_homepage.py  —  clear the leftover Odoo default demo homepage
#
# This clears the default Odoo demo content (e.g. the "band" homepage) that
# remains in the website homepage on the deployment server, leaving only the
# church_theme homepage content (hero / features / events / CTA) to render —
# matching the local setup.
#
# It is an ODOO SHELL SCRIPT (Python), NOT a bash script. Run it as shown in
# the instructions below.
#
# Run on the Linux deployment server (as the Odoo user):
#
#   sudo -u odoo odoo-bin shell -d <DB_NAME> -c /etc/odoo.conf --no-http < reset_homepage.py
#
#   # or, if only `odoo` is on PATH:
#   sudo -u odoo odoo shell -d <DB_NAME> -c /etc/odoo.conf --no-http < reset_homepage.py
#
# Replace <DB_NAME> with your actual database name.
# =============================================================================

import json

# Minimal empty homepage template (keeps the <div id="wrap"> so the inherited
# church_theme sections still inject their content into the page).
EMPTY = """<t name="Home" t-name="website.homepage">
        <t t-call="website.layout">
            <t t-set="pageName" t-value="'homepage'"/>
            <div id="wrap" class="oe_structure oe_empty"/>
        </t>
    </t>"""

# Reset EVERY website.homepage view (base + all website copies), for ALL
# languages including en_US, by writing the stored arch_db (translated JSONB)
# directly via SQL. Raw SQL bypasses Odoo's view XML validation, which would
# otherwise fail when a language (e.g. en_US) is left empty.
views = env['ir.ui.view'].search([('key', '=', 'website.homepage')])
print("Found website.homepage view(s):", views.ids)

langs = env['res.lang'].search([('active', '=', True)]).mapped('code') or []
if 'en_US' not in langs:
    langs = ['en_US'] + langs
arch_map = {lang: EMPTY for lang in langs}
print("Writing empty homepage for languages:", langs)

for v in views:
    env.cr.execute(
        "UPDATE ir_ui_view SET arch_db = %s::jsonb WHERE id = %s",
        (json.dumps(arch_map), v.id),
    )
    print("Reset view id=%s (website=%s)" % (v.id, v.website_id.id))

env.cr.commit()

# The running web server still holds the old compiled homepage in its own
# in-memory cache, so it must be restarted to pick up the change.
print("Committed. Now restart the web container:")
print("  docker compose restart web")
