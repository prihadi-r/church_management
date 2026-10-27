# Progress Log — Darash Church Management

Chronological log of completed work, verification evidence and open items.
Task breakdown lives in [task.md](task.md).

---

## 2026-10-27 — v2.3.0: Missionary, agency and support endpoints (tasks 17.1–17.4, 18.1–18.3)

- New `controllers/missionary_controller.py` serving `/api/v1/mobile/missionaries`:
  `GET /` (paginated directory), `GET /<id>` (profile) and `GET /<id>/avatar`. Contact data comes
  from the delegated `res.partner` (name, phone, mobile, email, image URLs); `active` accepts
  `true`/`false`/`all` and is evaluated on `partner_id.active` with `active_test=False`, so
  archived contacts are only returned when explicitly requested. Extra filters: `status_id`,
  `field_id`, `agency_id`, plus `limit` (default 20, capped 100) and `offset`.
- The profile adds `contact.address`, the agency with its contact block, `supervisor`, the trips
  the missionary leads, a support summary (total, count, last date) and avatar URLs for the two
  supported sizes.
- `GET /<id>/avatar` streams `res.partner.image_256` (or `size=1920`) as binary with
  `ETag` (weak, from `write_date` + size), `Last-Modified` and `Cache-Control: private, max-age=86400`.
  `If-None-Match` and `If-Modified-Since` are evaluated by the controller (weak comparison) and
  answer `304` with an empty body; the MIME type is sniffed from the image magic bytes. A contact
  without a photo → `404 not_found`; an unsupported `size` → `400 validation_error`.
- New `controllers/agency_controller.py` serving `GET /api/v1/mobile/missionaries/agencies`:
  contact block, address, `mission_fields`, `trip_count` and `missionary_count` counting only
  **active** missionaries (`partner_id.active`), with `active`/`field_id`/`limit`/`offset` filters.
- New `controllers/support_controller.py` serving `/api/v1/mobile/mission/support`:
  - `GET /summary` — `totals` (`pledged`, `collected`, `outstanding`, counts), `targets`
    (`overall`/`missionaries`/`trips` with `target`, `pledged`, `collected`, `pledge_progress`,
    `collection_progress`) and `by_donation_type`, all aggregated with `_read_group`/`search_count`.
  - `POST /pledge` — JSON (or form) body `partner_id`, `amount`, at least one of
    `missionary_id`/`trip_id`, optional `date` (`YYYY-MM-DD`), `donation_type_id`, `notes`;
    answers `201` with the created record. Validates the donor, a positive amount, the target
    (existing and not archived) and the donation type.
  - `GET /history` — paginated history ordered `date desc, id desc` with filters `partner_id`,
    `missionary_id`, `trip_id`, `donation_type_id`, `date_from`, `date_to`,
    `collected=true|false|all`, `limit`, `offset`.
- **Design note:** `church.mission.support` has no state field, so the API derives the status
  from the accounting link — a record is `pending` until it has a `payment_id`, then `collected`.
  No model, view, ACL or data change was needed. Payment details are only serialised when the
  API user may read `account.payment`; otherwise the payload carries `{"id": …, "restricted": true}`
  while `collected` stays accurate. Monetary totals are summed without currency conversion, the
  same known limitation as the web dashboard.
- Verified end-to-end over HTTP against a throwaway database with a **fresh install**
  (`--without-demo=all`, temporary server on port 8072, temporary read-only + write API keys,
  a 1x1 PNG on the first missionary's contact and one `account.payment`-linked support, all
  removed afterwards; `demo` untouched):
  - missionaries: list 200 (`total=5`), `status_id=2` → 1, `field_id=4` → 1, `agency_id=2` → 2,
    `limit=1&offset=1` → id 1, `limit=abc` → 400; detail 200 (`MSN/2026/0001`, target 24,000,000,
    total 3,500,000, progress 14.58, agency contact, 1 trip, support count 2 / last 2026-08-11);
    archiving one contact → default 4, `active=false` → 1, `active=all` → 5, agency count 3 → 2.
  - avatar: 200 `image/png` 70 bytes with `ETag`/`Last-Modified`; `If-None-Match` → 304 (0 bytes);
    `If-Modified-Since` → 304; stale `If-Modified-Since` → 200; `size=64` → 400;
    missionary without photo → 404; unknown id → 404; no key → 401; `size=1920` → 200.
  - agencies: 2 records matching the ORM (GMP 3 active missionaries / 2 trips, YMN 2 / 3),
    `field_id=3` → 1, paging works, `active=maybe` → 400, no key → 401.
  - summary: `pledged` 16,900,000, `collected` 1,500,000, `outstanding` 15,400,000, 8/1/7 counts,
    missionary target 94,000,000 (pledged 10,750,000 → 11.44 %), trip target 49,500,000
    (pledged 9,400,000 → 18.99 %), overall 143,500,000 (pledged 20,150,000 → 14.04 %,
    collected 3,000,000 → 2.09 %); `by_donation_type` sums to the same 16.9 M — all equal to the
    ORM oracle.
  - history: 8 records, `collected=true` → 1, `false` → 7, `all` → 8, `missionary_id=1` → 2,
    `trip_id=1` → 1, `partner_id=120` → 2, August window → 1, `limit=3&offset=6` → ids 2,1,
    `collected=maybe`/`date_from=27-10-2026`/`partner_id=abc` → 400; the collected record carries
    `status: "collected"` and `payment: {"id": 1, …, "restricted": true}` (no accounting rights),
    the pending ones `status: "pending"` and `payment: null`.
  - pledge: read-only key → 403 `read_only_access`; write key → 201 (`MSP/2026/0009`,
    `status: "pending"`), trip-only pledge → 201 (`MSP/2026/0010`); missing/zero/negative/
    non-numeric `amount`, missing/unknown `partner_id`, no target, unknown missionary/trip/
    donation type, bad `date`, malformed JSON and a JSON array → 400 with distinct messages;
    archived missionary/trip → 400 “not available”; summary then reported 17,151,000 pledged and
    10/1/9 counts, history `total=10`.
  - server log during the whole run: no `ERROR` / `CRITICAL` / `WARNING`.

---

## 2026-10-27 — v2.3.0: Mission trip endpoints (tasks 16.1–16.4)

- New `controllers/trip_controller.py` serving `/api/v1/mobile/mission/trips`:
  `GET /` (paginated list), `GET /<id>` (detail), `GET /<id>/participants` and
  `POST /<id>/register`. Every route composes `@require_mobile_api_key` +
  `@handle_api_errors`; list/participants answer through `paginated_response()`, the detail and
  the registration through `success_response()` (registration → `201`).
- List filters: `field_id`, `status_id`, `date_begin`, `date_end`, `limit` (default 20, capped
  100), `offset`. The date parameters select trips **overlapping** the window
  (`date_end >= date_begin` **and** `date_begin <= end-of-day(date_end)`), which is what a
  mobile agenda needs; a date-only upper bound is expanded to `23:59:59`.
- Trip payloads expose the inherited `event.event` data — `name`, `date_begin`/`date_end`,
  `date_tz`, `is_ongoing`/`is_finished`, venue (`address_id` + country), seat configuration,
  description/note — plus mission fields (type, field, agency, status with `is_closed` and
  `color`), leader (contact details), `budget`, `currency`, `support_total`,
  `funding_progress` and participant counts. The detail adds `organizer`, `responsible`
  (`event.event.user_id`), `event_status`, tags and a participant/support summary.
- Participants are filtered by a `confirmed` parameter (`true` default → confirmed only,
  `false` → pending, `all` → both) and serialise name, phone/mobile/email, avatar URL, role
  and registration date.
- `POST /register` accepts a JSON body (`partner_id` required, `role_id`, `notes`), or
  form-encoded parameters. It rejects with `400 validation_error`: unknown contact, unknown or
  archived role, contact already registered on the trip, a trip that already ended
  (`date_end` in the past), and a full trip (`seats_limited` with
  `max(participant_count, seats_taken) >= seats_max`). New participants are created with
  `confirmed = False` so staff can confirm them in the web app.
- Verified end-to-end over HTTP against a throwaway database with a **fresh install**
  (`--without-demo=all`, temporary server on port 8071, temporary API keys for a read-only and a
  write user, all removed afterwards; `demo` untouched): missing key → 401 `missing_api_key`;
  list → 200 with 5 trips; `field_id=4` → 2, `status_id=1` → 2, `status_id=2` → 1,
  November window → 1 (only the trip that overlaps it), `limit=2&offset=2` → rows 3–4,
  `limit=9999` → capped to 100, `field_id=abc` / `date_begin=31-12-2026` / `limit=0` → 400;
  detail → 200 with budget 15,000,000, support 5,250,000, progress 35.0 and the event
  description; unknown id → 404 `not_found`; participants → 1 confirmed, `confirmed=all` → 2,
  `confirmed=false` → 1, `confirmed=maybe` → 400; read-only key `POST /register` → 403
  `read_only_access`; write key → 201 (participant created with `confirmed=false`, visible
  through `confirmed=all`), duplicate → 400, ended trip → 400, unknown contact/role → 400,
  missing/non-integer `partner_id` → 400, malformed JSON / JSON array → 400; capacity:
  `seats_max=1` with 1 participant → 400 "full (1 of 1 seats taken)", `seats_max=2` → 201 and
  the next attempt → 400 "full (2 of 2 seats taken)". No ERROR/CRITICAL in the server log.

---

## 2026-10-27 — v2.3.0: Mission master-data endpoints (tasks 15.1–15.4)

- New `controllers/master_controller.py` serving `/api/v1/mobile/mission/master`:
  `GET /types`, `GET /fields`, `GET /statuses` (trip + missionary statuses in one payload)
  and `GET /roles`. Every route composes `@require_mobile_api_key` + `@handle_api_errors`
  and answers through `success_response()` / `paginated_response()`.
- The shared `active` query parameter accepts `true` (default: only active records),
  `false` (only archived records) or `all`; anything else is a `400 validation_error`.
  Archived rows are read with `with_context(active_test=False)` plus an `active = False`
  term, so the default Odoo archive filter never hides an explicitly requested archive.
- `GET /fields` is paginated (`limit` default 50, capped 200, `offset`) and serialises the
  nested `country` (`id` / `code` / `name`) and `parent` (`id` / `name`) references.
  Statuses carry `is_closed` so the app can tell finished trips/missionaries apart.
- Verified end-to-end over HTTP against a throwaway database with a **fresh install**
  (`--without-demo=all`, temporary server on port 8071 and a temporary API key, all removed
  afterwards): missing key → 401 `missing_api_key`, `X-Database` mismatch → 403
  `database_mismatch`; `types` 6, `fields` 6 (paging `limit=2&offset=2` → rows 3–4, `total` 6),
  `statuses` 4 trip + 5 missionary, `roles` 6 — all 200 and matching the installed master
  data. Archive handling: after archiving a type, default → 6, `active=false` → 1,
  `active=all` → 7; `active=maybe` → 400 `validation_error`; `limit=abc` / `limit=0` → 400.
  A field created with `country_id=ID` and `parent_id=Sumatra` serialised as
  `{"country": {"id": 100, "code": "ID", "name": "Indonesia"}, "parent": {"id": 2, "name": "Sumatra"}}`.
  No ERROR/CRITICAL in the server log; the `demo` database was untouched.

---

## 2026-10-26 — Docs sync for the Mobile API milestone

- `README.md`: added a **Mobile API** row to the architecture table, listed
  `TASK-FLUTTER-CONTROLLER.md` under documentation, and the `2.3.0 (in progress)` row now
  names the two live endpoint sets.
- `USER_GUIDE.md`: new **§13 Mobile API (Aplikasi Flutter)** — service-account/API-key steps,
  endpoint table, response envelope with error-code table, and what is still planned.
- `INSTALLATION_GUIDE.md`: new **§6.4 Pengguna API Mobile** (password-less `mobile_api` user,
  key creation, configurable role), a CLI upgrade recipe, and a refreshed "File Penting" table.
- `TASK-FLUTTER-CONTROLLER.md`: synced with the board — section 1 (tasks 14.1–14.4) and 6.1
  (19.1) checked off, `[cite: …]` artefacts and the trailing prompt fragment removed.
- `task.md`: added a **v2.3.0 Backlog / follow-ups** list (remaining groups 15–18, 20, 21.6;
  write-access note for the Read Only service user; currency conversion; review of the
  `event.event` read grant).
- `CONTRIBUTING.md`: project structure corrected — no `docs/` folder exists, and
  `controllers/` now also serves the mobile JSON API.

---

## 2026-10-26 — `demo` database upgraded to 18.0.2.2.0

- Backed up first: `C:\Users\Lenovo\odoo_backups\demo_before_upgrade_20261026_133951.dump`
  (`pg_dump -Fc`).
- Stopped the `odoo-server-18.0` service, ran
  `odoo-bin -d demo -u church_management --stop-after-init --max-cron-threads=0`
  (exit 0, no ERROR/CRITICAL in the log), then restarted the service (`/web/login` → 200).
- Result: module version `18.0.2.0.0` → `18.0.2.2.0`, 23 new tables
  (`church_mission_*`, `church_sunday_school_*`), the `mobile_api` service account created
  without a password, the new `event.event.church_read` ACL row present, and the mission /
  Sunday School sample data loaded (5 trips, 5 missionaries, 8 support lines, 5 classes,
  15 sessions, 85 calendar activities).
- Live smoke test on `http://localhost:8069` with a temporary API key (deleted afterwards):
  `GET /api/v1/mobile/mission/dashboard/metrics` → 200 (IDR, 3 active trips, 2 missionaries
  in field, 16,900,000 support, 2 upcoming), `GET /api/v1/mobile/calendar/activities` → 200,
  `GET /api/v1/mobile/calendar/agenda` → 200 (localised "October 2026"),
  `GET /api/v1/mobile/calendar/upcoming` → 200, without a key → 401 `missing_api_key`.
  This also resolves the stale-schema 500 (`church_activity.sunday_school_session_id`).

---

## 2026-10-26 — v2.3.0: Mission dashboard metrics endpoint (task 19.1)

- New `controllers/dashboard_controller.py` serving
  `GET /api/v1/mobile/mission/dashboard/metrics` with `kpi` (`active_trips`,
  `missionaries_in_field`, `total_support_raised`, `upcoming_departures`,
  `next_departure`) and `charts` mirroring the eight web dashlets: `trips_by_status`,
  `trips_by_type`, `trips_by_field`, `missionaries_by_status`, `participants_by_role`,
  `support_by_month`, `support_by_missionary`, `support_by_donation_type`.
- Aggregation uses `_read_group` (no record loading); categorical series are sorted
  largest-first, the month series oldest-first, and status groups carry `color`/`code`
  for chart styling. `active_trips` = status `planned`/`ongoing` (an unset status counts
  as active), `missionaries_in_field` = status `on_field`.
- **Security fix required by this task:** `security/ir.model.access.csv` had no rule for
  `event.event`, so church groups could not read mission trips at all — and mission trips
  *are* events (`_inherits`). Added
  `access_event_event_church_read,event.event.church_read,model_event_event,group_church_read_only,1,0,0,0`
  (read-only for the church Read Only group; Write/Full inherit it). This also fixes the
  same AccessError in the web Mission app for read-only church users.
- Verified over HTTP against a throwaway database with a **fresh install**, cross-checked
  against ORM oracles: `active_trips=3` (3), `missionaries_in_field=2` (2),
  `total_support_raised=16,900,000` (16,900,000), `upcoming_departures=2` (2),
  `next_departure=2026-11-02 01:00:00`; chart series total 5 trips / 5 missionaries /
  9 participants / 16.9M support, and the three support breakdowns
  (month, missionary, donation type) each sum to the same 16.9M KPI. Missing API key → 401.
  The temporary database/server/key were removed afterwards; `demo` was untouched.
- Known limitation: monetary totals are summed in the company currency (multi-currency
  conversion is still in the backlog).

---

## 2026-10-26 — v2.3.0: Church Calendar endpoints (tasks 21.1–21.5)

- New `controllers/calendar_controller.py` serving `/api/v1/mobile/calendar`:
  `GET /activities` (filters `type`, `state`, `date_from`, `date_to`, `limit`, `offset`),
  `GET /activities/<id>` (adds `source_type` / `source_model` / `source_id` / `source_name`),
  `GET /agenda` (`group=day` month/day roll-up or `group=type`), `GET /upcoming`
  (default 5, capped 50) and `GET /metrics` (counts per type and per month).
- Unconfirmed activities are hidden exactly like the public `/church-calendar` page
  (only `approved`/`done`, pray requests always shown). The domain is built with
  `expression.AND`/`OR` — Odoo 18's `_where_calc` rejects nested domain lists.
- Agenda labels are formatted with Babel in the API user's language instead of the server
  locale; datetimes stay naive UTC strings as Odoo stores them.
- `controllers/common.py`: added `paginated_response()` (`items` / `total` / `limit` / `offset`).
- Verified end-to-end over HTTP against a throwaway database with a **fresh install**
  (`churchapitest`, since the `demo` database is still on module `2.0.0` and lacks the
  `sunday_school_session_id` column): 401 missing key, 403 database mismatch,
  `activities` / `filter` / `paging` / `agenda` / `upcoming` / `metrics` all 200,
  `type=nope` / `date_from=31-12-2026` / `limit=abc` / `group=week` / `limit=-3` → 400
  `validation_error`, unknown id → 404 `not_found`, `state=draft` → 0 rows (confirmation
  rule), `type=pray` and `type=sunday_school` return rows, agenda labels rendered as
  "October 2026" / "Saturday, 03 October 2026". The temporary database, server and API key
  were removed afterwards; the `demo` database was left untouched.
- Open item: task **21.6** (iCal export) is still planned.

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
