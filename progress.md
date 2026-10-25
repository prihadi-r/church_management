# Progress Log — Darash Church Management

Chronological log of completed work, verification evidence and open items.
Task breakdown lives in [task.md](task.md).

---

## 2026-10-25 — License change

- Replaced **LGPL-3** with a **custom license**: free to use and free to distribute
  (verbatim copies); **any modification requires the prior written approval of the
  owner**. See [LICENSE](LICENSE).
- `__manifest__.py`: `license` → `Other proprietary` (Odoo has no custom key), summary and
  description updated.
- Docs updated: `README.md` (hero text, badge, "Why Darash" bullet, license section),
  `CONTRIBUTING.md` (contributions need owner approval), `INSTALLATION_GUIDE.md` (§12).

---

## 2026-10-25 — v2.2.0: Mission app

### Done

- **Models (10)**
  - Master data (no selection fields): `church.mission.field`, `church.mission.type`,
    `church.mission.status`, `church.mission.role`, `church.missionary.status`.
  - `church.mission.agency` — `_inherits = {'res.partner': 'partner_id'}`, auto-created
    partner is a company.
  - `church.mission.missionary` — `_inherits` `res.partner`; field, agency, status,
    supervisor, support target + computed support total/progress.
  - `church.mission.trip` — `_inherits` `event.event`; type, field, agency, status, leader,
    budget + computed support/funding progress and participant counts.
  - `church.mission.participant` — `_inherits` `res.partner`; role, confirmation,
    unique per (trip, partner).
  - `church.mission.support` — donor, date, amount, donation type, missionary/trip,
    optional link to `account.payment` (reverse field added on `account.payment`).
- **Views** — kanban/list/calendar/form/search for trips, missionaries and participants;
  list/pivot/form/search for support; list/form/search for all masters and agencies.
- **Mission dashboard** — `board.board` with 8 graph dashlets (trips by status/type/field,
  missionaries by status, participants by role, support per month/missionary/donation type).
- **Menu** — `Church Management → Mission` with Dashboard, Mission Trips, Missionaries,
  Participants, Mission Support and Configuration.
- **Security** — read/write/full ACLs for all 10 models on the three church groups.
- **Data** — sequences (`MT/`, `MSN/`, `MSP/`), 6 fields, 6 types, 4 trip statuses,
  6 roles, 5 missionary statuses, plus sample data (2 agencies, 5 missionaries, 5 trips,
  9 participants, 8 support lines).
- **Docs** — `README.md` (features, menu tree, integrations, version history),
  `USER_GUIDE.md` (new section 6 + renumbered sections + quick-fill rows + tips),
  `__manifest__.py` (description, data list, version `2.2.0`).

### Verification

Environment: Odoo 18 from `/usr/lib/python3/dist-packages/odoo`, PostgreSQL 14.
Database operations were run as the **`odoo`** Postgres role in a throw-away database
(dropped afterwards); the role's password was reset to `NULL` after the run.

| Check | Result |
|---|---|
| Fresh `-i church_management` into an empty DB | ✅ `EXIT=0`, no module errors (only pre-existing docutils warnings from module descriptions) |
| `-u church_management` upgrade | ✅ `EXIT=0` |
| Sample data counts | ✅ 5 trips, 5 missionaries, 2 agencies, 9 participants, 8 support lines, 6/6/4/6/5 masters |
| Admin menu tree | ✅ `Church Management / Mission` → Dashboard, Mission Trips, Missionaries, Participants, Mission Support, Configuration |
| Computed values | ✅ Cianjur trip 2 participants / 1 confirmed / 5,250,000 support / 35 %; Petrus Halim 3,500,000 support / 14.58 % |
| Event + calendar sync | ✅ creating a trip creates its `event.event` and `church.activity` row; changing `date_begin` updates the calendar row |
| Auto codes | ✅ `MT/2026/0003`, `MSN/2026/0001`, `MSP/2026/0009` |
| Trip deletion | ✅ event removed, calendar rows removed |
| Support validation | ✅ "must be linked to a missionary or a mission trip" raised on create |
| Delegated search/order | ✅ `date_begin`, `active`, `name` work through `event.event` / `res.partner` |
| Views load | ✅ `kanban`, `list`, `calendar`, `form`, `search`, `pivot` for all models |
| Dashboard actions | ✅ all 8 actions resolve to their own graph view |
| Access rights | ✅ Read Only can read all 10 models; create is blocked |
| Diagrams/board | ✅ `board.board` form view + `action_church_mission_dashboard` load |

### Open items

See the backlog in [task.md](task.md). Most important:

1. Upgrade the running `demo` database to `18.0.2.2.0` (it is still on `2.0.0`).
2. Add screenshots of the Mission dashboard.
