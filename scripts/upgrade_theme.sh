#!/usr/bin/env bash
# =============================================================================
# upgrade_theme.sh — upgrade the Church Theme module in the Docker Compose Odoo
#
# Run this from the directory containing your docker-compose.yml (e.g.
# ~/odoo18-docker) on the server, as a user with access to docker.
#
#   ./upgrade_theme.sh [DB_NAME]
#
# DB_NAME defaults to "gosyen"; pass another name as the first argument if needed.
# =============================================================================
set -e

DB_NAME="${1:-gosyen}"
CONFIG="/etc/odoo/odoo.conf"
MODULE="church_theme"

echo "==> Stopping web container (avoid DB/registry conflict) ..."
docker compose stop web

echo "==> Upgrading module ${MODULE} on database '${DB_NAME}' ..."
docker compose run --rm -T web \
    odoo -d "${DB_NAME}" -c "${CONFIG}" -u "${MODULE}" --stop-after-init

echo "==> Starting web container ..."
docker compose start web

echo "==> Done. ${MODULE} upgraded to 1.0.1."
