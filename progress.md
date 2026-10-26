# Progress Log — Darash Church Management

Chronological log of completed work, verification evidence and open items.
Task breakdown lives in [task.md](task.md).

---

## 2026-10-26 — Task board: Sunday School & Church Calendar mobile endpoints

- [task.md](task.md): added the **20. Sunday School Endpoints**
  (`/api/v1/mobile/sunday-school`, 9 tasks) and **21. Church Calendar Endpoints**
  (`/api/v1/mobile/calendar`, 6 tasks) groups, continuing the v2.3.0 numbering after 19.
- The tasks are grounded in the existing models: `church.sunday.school.class` / `.session` /
  `.student` / `.teacher` / `.attendance` (plus their master-data models), and the
  `church.activity` calendar aggregator — which already carries `sunday_school` as an
  `activity_type` — reusing the confirmation rule of the public `/church-calendar` page.
- Documented the shared route conventions for v2.3.0: JSON `type='http'` (`auth='public'`,
  `csrf=False`) composing `@require_mobile_api_key` + `@handle_api_errors` and answering through
  `success_response()` / `error_response()`.
- [README.md](README.md): new **Mobile API (Flutter)** feature section (auth headers, envelope,
  error codes, service-account setup) and a `2.3.0 (in progress)` version-history row.
- Status: every endpoint task is still ⬜ planned — only the shared layer (tasks 14.1–14.4) is
  implemented. Open item: the `demo` database still needs the module upgrade before any endpoint
  can be exercised.

---

## 2026-10-26 — v2.3.0: Mobile API envelope + service user (tasks 14.3, 14.4)

- New `controllers/common.py`: `success_response()` / `error_response()` implement the
  `{"success": ..., "data": ... | "error": {"code", "message"}}` envelope, and
  `@handle_api_errors` maps Odoo exceptions to HTTP statuses —
  `ValidationError` → 400 `validation_error`, `AccessError` → 403 `access_error`,
  `AccessDenied` → 403 `access_denied`, `MissingError` → 404 `not_found`,
  other `UserError` → 400 `user_error`, `HTTPException` → its own code, any other
  exception → 500 `internal_error` with a generic message. Tracebacks stay in the
  server log (`_logger.exception`), never in the response.
- `controllers/security.py` now imports `error_response` from `common.py` instead of
  keeping its own copy; `controllers/__init__.py` imports `common` first.
- New `data/church_mission_api_user.xml`: service account `mobile_api`
  ("Mobile API") with **no password** (API-key reachable only) and the Church
  **Read Only** role, loaded with `noupdate="1"` so the admin's choice of
  Read Only / Write Only / Full Access survives upgrades. Registered in
  `__manifest__.py` right after the security files.
- Verified with a throwaway `odoo-bin shell` harness on the `demo` database
  (transaction rolled back): envelope shapes, every exception mapping (including a
  `ValueError` returning the generic 500 message while the real error stayed in the
  log), 14.1/14.2 regression (401 missing key, valid GET, 403 read-only POST), and
  `convert_file` loading the XML — user created with `login='mobile_api'`,
  `read_only=True`, `password` unset.

---

## 2026-10-26 — v2.3.0: Mobile API execution context (task 14.2)

- `@require_mobile_api_key` now switches the request environment to the API key owner
  (`request.update_env(user=user_id)`), so every model operation in the handler is
  evaluated against that user and the standard Odoo ACLs / record rules apply.
- Data-modifying methods (`POST`, `PUT`, `PATCH`, `DELETE`) are refused with
  `403 read_only_access` when the key owner only holds **Read Only**
  (`church_management.group_church_read_only`) without *Write Only* or *Full Access*.
- Verified with a throwaway `odoo-bin shell` harness on the `demo` database (transaction
  rolled back): `env.uid`/`env.su` inside the handler match the key owner and are never
  the superuser; Read Only key + `POST`/`PUT`/`DELETE` → 403 without running the handler;
  Write Only and admin keys keep working; with the read-only env a `res.users` search
  succeeds while `create` raises `AccessError`, proving ACLs are enforced.
- Open note: the `demo` database is still on module version `2.0.0`, so ACL rows for the
  mission models are not installed there yet — that is the pending upgrade already listed
  in the backlog.

---

## 2026-10-26 — v2.3.0: Mobile API key authentication (task 14.1)

- New `controllers/security.py` with `@require_mobile_api_key`: reads `X-Api-Key` and
  `X-Database`, authenticates the key through
  `res.users.apikeys.sudo()._check_credentials(scope='rpc')`, and answers `401`
  (`missing_api_key`, `invalid_api_key`) or `403` (`database_mismatch`,
  `database_unavailable`) using the `{"success": false, "error": {...}}` envelope.
- Resolved user is stored on `request.mobile_api_user` (helper
  `get_authenticated_user()`); switching the environment to that user so Odoo ACLs apply
  is task **14.2**.
- Registered the module in `controllers/__init__.py`.
- Verified with a throwaway `odoo-bin shell` harness on the `demo` database (transaction
  rolled back): missing key → 401, mismatched `X-Database` → 403, invalid key → 401,
  no database → 403, valid key and valid key + matching database → handler runs and
  `mobile_api_user` resolves to the key owner.

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
