# =============================================================================
#  Darash — Church Management (Odoo 18)
#
#  Production-ready image for the `church_management` module.
#  Base image: official Odoo 18 (Debian + Python 3.11).
#
#  Usage:
#    - docker compose up -d --build   (recommended — see docker-compose.yml)
#    - docker build -t church_management:18.0 .
# =============================================================================
FROM odoo:18

USER root

# Extra Python dependency required by the module (RSS / news feed ingestion).
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir feedparser

# Bake the module into the addons directory.
# (docker-compose also bind-mounts ./ to this same path so you can edit the
# module without rebuilding the image — the mount overrides this copy.)
COPY . /mnt/extra-addons/church_management

# Default Odoo configuration. The official image generates /etc/odoo/odoo.conf
# at startup from env vars when the file does not exist; providing this file
# makes the config explicit and overridable (docker-compose mounts its own copy).
COPY ./odoo.conf /etc/odoo/odoo.conf

# Ensure the module is readable/writable by the (non-root) odoo user.
RUN chown -R odoo:odoo /mnt/extra-addons

# Switch back to the non-root odoo user (ENTRYPOINT / CMD inherited from base).
USER odoo
