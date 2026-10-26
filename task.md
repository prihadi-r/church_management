# Task Board — Darash Church Management

Status legend: ✅ done · 🚧 in progress · ⬜ planned · ⛔ blocked

---

## Milestone: v2.2.0 — Mission (missions & missionaries)

**Request:** new model(s) for church missions management under a **Mission** menu in
Church Management, using **master-data models instead of selection fields** and
**inheriting base models** (`res.partner`, `event.event`, …), plus a **Mission dashboard**.

### Scope & tasks

| # | Task | Status | Deliverable |
|---|------|--------|-------------|
| 1 | Mission menu under **Church Management** | ✅ | [views/church_mission_menu.xml](views/church_mission_menu.xml) |
| 2 | Master data models, **no selection fields** | ✅ | `church.mission.field`, `church.mission.type`, `church.mission.status`, `church.mission.role`, `church.missionary.status` |
| 3 | Mission agency — inherit `res.partner` | ✅ | [models/church_mission_agency.py](models/church_mission_agency.py) |
| 4 | Missionary — inherit `res.partner` | ✅ | [models/church_missionary.py](models/church_missionary.py) |
| 5 | Mission trip — inherit `event.event` | ✅ | [models/church_mission_trip.py](models/church_mission_trip.py) |
| 6 | Participant — inherit `res.partner` | ✅ | [models/church_mission_participant.py](models/church_mission_participant.py) |
| 7 | Mission support — reuse `church.donation.type` + `account.payment` | ✅ | [models/church_mission_support.py](models/church_mission_support.py) |
| 8 | Views: kanban / list / calendar / form / search / pivot | ✅ | [views/church_mission_views.xml](views/church_mission_views.xml), [views/church_mission_master_views.xml](views/church_mission_master_views.xml) |
| 9 | Mission dashboard (Odoo Dashboards board, 8 graph dashlets) | ✅ | [views/church_mission_dashboard_views.xml](views/church_mission_dashboard_views.xml) |
| 10 | Access rights for Read Only / Write Only / Full Access | ✅ | [security/ir.model.access.csv](security/ir.model.access.csv) |
| 11 | Sequences + master data + sample data | ✅ | [data/church_mission_data.xml](data/church_mission_data.xml), [data/church_mission_sample.xml](data/church_mission_sample.xml) |
| 12 | Documentation (README, User Guide, manifest) | ✅ | [README.md](README.md), [USER_GUIDE.md](USER_GUIDE.md), [__manifest__.py](__manifest__.py) |
| 13 | Validation (fresh install, ORM smoke tests, ACL test) | ✅ | see [progress.md](progress.md) |

### Acceptance criteria

- [x] **Mission** menu appears under Church Management with Dashboard, trips, missionaries,
      participants, support and Configuration.
- [x] No `fields.Selection` is used by the new models — every status/type/role/field is a
      master record editable from **Mission → Configuration**.
- [x] Missionaries, participants and agencies reuse `res.partner` (delegation inheritance),
      so they are real Contacts (name, phone, email, address, photo).
- [x] A mission trip **is** an `event.event`, so it is listed in the Events app and appears
      automatically in the Church Calendar; deleting the trip removes its event and calendar row.
- [x] Mission support requires a missionary and/or trip, and amounts must be positive.
- [x] Trip/participant counts, support totals and funding/support progress are computed.
- [x] The Mission dashboard renders eight graph dashlets from the mission models.
- [x] Read Only group can read all mission models but not create/update/delete.
- [x] Module installs cleanly on Odoo 18 with no module errors.

### Backlog / follow-ups

- ✅ Upgrade the running databases (`demo`) to `18.0.2.2.0` — done 2026-10-26 (was `2.0.0`).
- ⬜ Screenshots for the Mission dashboard under `screenshots/`.
- ⬜ Optional: public "Missions" page on the website (reuse `event.event` data).
- ⬜ Optional: auto-create `church.mission.participant` from `event.registration`.
- ⬜ Optional: currency conversion for support totals in multi-currency setups.
- ⬜ Optional: portal access so missionaries can see their own support progress.

---

## Milestone: v2.3.0 — Mobile API Controllers (Flutter)

**Request:** REST controllers under `controllers/` so the Flutter mobile client can read
mission master data, trips, missionaries, support and dashboard metrics — authenticated
with Odoo API keys, authorized through the standard Odoo ACLs.

Source breakdown: [TASK-FLUTTER-CONTROLLER.md](TASK-FLUTTER-CONTROLLER.md).

### Scope & tasks

All routes below are JSON `type='http'` endpoints (`auth='public'`, `csrf=False`) that
compose `@require_mobile_api_key` + `@handle_api_errors` and answer through
`success_response()` / `error_response()`.

#### 14. Security Infrastructure & API Key Authentication

- [x] **14.1 API Key Auth Decorator**
  - [x] Extract `X-Api-Key` and `X-Database` from incoming HTTP request headers.
  - [x] Authenticate key against `res.users.apikeys` via `sudo()._check_credentials()`.
  - [x] Return standard `401 Unauthorized` or `403 Forbidden` JSON if missing or invalid.
  - [x] Deliverable: [controllers/security.py](controllers/security.py) (`@require_mobile_api_key`).

- [x] **14.2 Execution Context Switcher**
  - [x] Switch environment user context (`request.update_env(user=user_id)`) to enforce Odoo ACL rules.
  - [x] Ensure Read Only security groups reject POST/PUT/DELETE operations with `403 Forbidden`.
  - [x] Deliverable: [controllers/security.py](controllers/security.py).

- [x] **14.3 Unified JSON Response & Error Envelope**
  - [x] Implement standardized response wrapper (`{"success": true, "data": ...}`).
  - [x] Implement exception handler capturing Odoo `AccessError`, `ValidationError`, and `UserError` without leaking tracebacks.
  - [x] Deliverable: [controllers/common.py](controllers/common.py).

- [x] **14.4 Mobile API Service User Data Setup**
  - [x] Define dedicated system user for API access with configurable access roles.
  - [x] Deliverable: [data/church_mission_api_user.xml](data/church_mission_api_user.xml).

#### 15. Mission Master Data Endpoints

- [ ] **15.1 Mission Types (`/api/v1/mobile/mission/master/types`)**
  - [ ] Implement `GET` endpoint returning active mission types (`church.mission.type`).
  - [ ] Support filter parameters: `active`.
  - [ ] Deliverable: `controllers/master_controller.py`.

- [ ] **15.2 Mission Fields (`/api/v1/mobile/mission/master/fields`)**
  - [ ] Implement `GET` endpoint returning geographic fields/regions (`church.mission.field`).
  - [ ] Support pagination parameters: `limit`, `offset`.
  - [ ] Deliverable: `controllers/master_controller.py`.

- [ ] **15.3 Status Records (`/api/v1/mobile/mission/master/statuses`)**
  - [ ] Implement `GET` endpoint returning trip statuses (`church.mission.status`) and missionary statuses (`church.missionary.status`).
  - [ ] Deliverable: `controllers/master_controller.py`.

- [ ] **15.4 Participant Roles (`/api/v1/mobile/mission/master/roles`)**
  - [ ] Implement `GET` endpoint returning available participant roles (`church.mission.role`).
  - [ ] Deliverable: `controllers/master_controller.py`.

#### 16. Mission Trips Endpoints (`/api/v1/mobile/mission/trips`)

- [ ] **16.1 Mission Trips List (`GET /`)**
  - [ ] Return paginated trips with status, mission field, date ranges, and funding progress.
  - [ ] Query domain filtering: by `field_id`, `status_id`, `date_begin`, `date_end`.
  - [ ] Deliverable: `controllers/trip_controller.py`.

- [ ] **16.2 Mission Trip Detail (`GET /<int:trip_id>`)**
  - [ ] Fetch complete trip payload including inherited `event.event` fields, budget, description, and coordinator details.
  - [ ] Deliverable: `controllers/trip_controller.py`.

- [ ] **16.3 Trip Participants List (`GET /<int:trip_id>/participants`)**
  - [ ] Return confirmed participants (`church.mission_participant`) linked to the trip.
  - [ ] Include partner details (name, phone, role).
  - [ ] Deliverable: `controllers/trip_controller.py`.

- [ ] **16.4 Trip Participant Registration (`POST /<int:trip_id>/register`)**
  - [ ] Handle registration payload (`partner_id`, `role_id`, `notes`).
  - [ ] Validate trip capacity and dates before creating participant record.
  - [ ] Deliverable: `controllers/trip_controller.py`.

#### 17. Missionaries & Agencies Endpoints (`/api/v1/mobile/missionaries`)

- [ ] **17.1 Missionaries List (`GET /`)**
  - [ ] Return active missionaries (`church.missionary`) with contact details from inherited `res.partner`.
  - [ ] Deliverable: `controllers/missionary_controller.py`.

- [ ] **17.2 Missionary Profile (`GET /<int:missionary_id>`)**
  - [ ] Return full missionary record, sending agency details, field assignment, and total support received.
  - [ ] Deliverable: `controllers/missionary_controller.py`.

- [ ] **17.3 Missionary Image Route (`GET /<int:missionary_id>/avatar`)**
  - [ ] Serve cached binary avatar from `res.partner.image_1920` / `image_256` with HTTP 304 support.
  - [ ] Deliverable: `controllers/missionary_controller.py`.

- [ ] **17.4 Mission Agencies Directory (`GET /agencies`)**
  - [ ] Return registered mission agencies (`church.mission_agency`) along with assigned active missionary counts.
  - [ ] Deliverable: `controllers/agency_controller.py`.

#### 18. Mission Support Endpoints (`/api/v1/mobile/mission/support`)

- [ ] **18.1 Support Metrics Summary (`GET /summary`)**
  - [ ] Compute funding metrics: total pledges, collected amounts, and target attainment percentages.
  - [ ] Deliverable: `controllers/support_controller.py`.

- [ ] **18.2 Submit Support Entry (`POST /pledge`)**
  - [ ] Validate payload: ensure positive amount, donor partner ID, and trip or missionary assignment.
  - [ ] Create record in `church.mission_support` with draft/pending status.
  - [ ] Deliverable: `controllers/support_controller.py`.

- [ ] **18.3 Support History Log (`GET /history`)**
  - [ ] Fetch paginated payment and support records filtered by donor partner or target entity.
  - [ ] Deliverable: `controllers/support_controller.py`.

#### 19. Mobile Dashboard Endpoint (`/api/v1/mobile/mission/dashboard`)

- [x] **19.1 Consolidated KPI & Chart Data (`GET /metrics`)**
  - [x] Aggregate data corresponding to the 8 web mission dashboard dashlets.
  - [x] Return KPI card counters (active trips, missionaries in field, total support raised, upcoming departures).
  - [x] Return pre-aggregated time-series and categorical data for Flutter chart rendering.
  - [x] Deliverable: [controllers/dashboard_controller.py](controllers/dashboard_controller.py).

#### 20. Sunday School Endpoints (`/api/v1/mobile/sunday-school`)

- [ ] **20.1 Sunday School Master Data (`GET /master`)**
  - [ ] Return the active levels, class statuses, session statuses, student statuses, teacher roles and attendance statuses in one payload.
  - [ ] Include `is_present` on attendance statuses so the app can compute presence locally.
  - [ ] Deliverable: `controllers/sunday_school_controller.py`.

- [ ] **20.2 Classes List (`GET /classes`)**
  - [ ] Return paginated classes with `level_id`, `status_id` and `teacher_id` names, `room`, `meeting_time` and `capacity`.
  - [ ] Include the computed `student_count`, `teacher_count`, `session_count` and `next_session_datetime`.
  - [ ] Filter by `level_id`, `status_id`, `teacher_id`, `active`; support `limit` / `offset`.
  - [ ] Deliverable: `controllers/sunday_school_controller.py`.

- [ ] **20.3 Class Detail (`GET /classes/<int:class_id>`)**
  - [ ] Return the class record plus its teachers (with `role_id` name), its students and the next 5 sessions.
  - [ ] Deliverable: `controllers/sunday_school_controller.py`.

- [ ] **20.4 Class Students (`GET /classes/<int:class_id>/students`)**
  - [ ] Return partner name, student `code`, `age`, student status name and `attendance_rate`.
  - [ ] Deliverable: `controllers/sunday_school_controller.py`.

- [ ] **20.5 Sessions List (`GET /sessions`)**
  - [ ] Return paginated sessions with class, teacher and status names, `start_datetime`, `end_datetime` and `lesson_summary`.
  - [ ] Filter by `class_id`, `status_id`, `date_from`, `date_to`; support `limit` / `offset`.
  - [ ] Deliverable: `controllers/sunday_school_controller.py`.

- [ ] **20.6 Session Attendance (`GET /sessions/<int:session_id>`)**
  - [ ] Return the session detail plus its attendance lines (student name, status name/code, `present`, `note`).
  - [ ] Include `attendance_count`, `present_count` and `absent_count`.
  - [ ] Deliverable: `controllers/sunday_school_controller.py`.

- [ ] **20.7 Capture Attendance (`POST /sessions/<int:session_id>/attendance`)**
  - [ ] Accept a list of `{student_id, status_id, note}` lines and create/update the `church.sunday.school.attendance` records.
  - [ ] Reject students that are not enrolled in the session's class with `400 validation_error`.
  - [ ] Keep the call idempotent for the same session/student pair (re-posting updates in place).
  - [ ] Deliverable: `controllers/sunday_school_controller.py`.

- [ ] **20.8 Students Directory (`GET /students`, `GET /students/<int:student_id>`)**
  - [ ] List/search students by `class_id`, `status_id` and name, with pagination.
  - [ ] Detail returns the guardian, enrollment date, `session_count`, `present_count`, `absent_count` and `attendance_rate`.
  - [ ] Deliverable: `controllers/sunday_school_controller.py`.

- [ ] **20.9 Sunday School Dashboard (`GET /dashboard/metrics`)**
  - [ ] Return KPI counters: active classes, enrolled students, sessions in the current month and average attendance rate.
  - [ ] Return per-level and per-status distributions plus a monthly attendance trend for Flutter charts.
  - [ ] Deliverable: `controllers/sunday_school_controller.py`.

#### 21. Church Calendar Endpoints (`/api/v1/mobile/calendar`)

- [x] **21.1 Calendar Activities (`GET /activities`)**
  - [x] Return `church.activity` rows (`event`, `baptism`, `marriage`, `care_cell`, `pray`, `sunday_school`) with `name`, `activity_type`, `start`, `stop`, `state` and `color`.
  - [x] Hide unconfirmed activities (`draft`, `review`, `cancel`) the same way the public `church-calendar` page does; pray requests are always shown.
  - [x] Filter by `type`, `date_from`, `date_to`, `state`; support `limit` / `offset`.
  - [x] Deliverable: [controllers/calendar_controller.py](controllers/calendar_controller.py).

- [x] **21.2 Activity Detail (`GET /activities/<int:activity_id>`)**
  - [x] Return the activity plus its source as `source_type` / `source_id` (`event_id`, `baptism_id`, `marriage_id`, `care_cell_id`, `pray_request_id`, `sunday_school_session_id`) so the app can drill down.
  - [x] Deliverable: [controllers/calendar_controller.py](controllers/calendar_controller.py).

- [x] **21.3 Agenda (`GET /agenda`)**
  - [x] Group activities per day with a month roll-up for the mobile agenda list.
  - [x] Support `group=day` (default) or `group=type` and the same filters as `/activities`.
  - [x] Deliverable: [controllers/calendar_controller.py](controllers/calendar_controller.py).

- [x] **21.4 Upcoming (`GET /upcoming`)**
  - [x] Return the next activities from now for the home screen, `limit` default 5 and capped at 50.
  - [x] Deliverable: [controllers/calendar_controller.py](controllers/calendar_controller.py).

- [x] **21.5 Calendar Metrics (`GET /metrics`)**
  - [x] Return activity counts per type and per month for the dashboard charts.
  - [x] Deliverable: [controllers/calendar_controller.py](controllers/calendar_controller.py).

- [ ] **21.6 Optional: iCal Export (`GET /export.ics`)**
  - [ ] Serve the filtered activities as `text/calendar` so the app can hand them to the device calendar.
  - [ ] Deliverable: `controllers/calendar_controller.py`.

### Backlog / follow-ups

- ⬜ **15–18** — Mission master data, trips, missionaries/agencies and support endpoints.
- ⬜ **20** — Sunday School endpoints (master data, classes, sessions, attendance, dashboard).
- ⬜ **21.6** — optional iCal export (`GET /export.ics`).
- ⬜ Write endpoints (`POST /sessions/<id>/attendance`, `POST /pledge`,
      `POST /register`) need a service user with **Write Only** or **Full Access**; the shipped
      `mobile_api` user is **Read Only** by default.
- ⬜ Currency conversion for monetary totals (mission dashboard and support endpoints) —
      amounts are currently summed in the company currency.
- ⬜ Revisit the model-wide `event.event` read grant added on 2026-10-26 (needed because
      mission trips inherit `event.event`); consider restricting it to the fields the app uses.

---

## Completed outside the milestone

- ✅ 2026-10-25 — License changed from **LGPL-3** to a **custom license**: free to use and
  free to distribute (verbatim copies); **any modification requires the owner's prior written
  approval**. Details in [LICENSE](LICENSE) and [progress.md](progress.md).
