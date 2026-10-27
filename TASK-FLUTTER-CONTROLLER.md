# Task Board â€” Odoo Mobile API Controllers (`church_management`)

> **Status (2026-10-26):** this breakdown has been merged into
> [task.md](task.md) as milestone **v2.3.0** (groups 14â€“21). Section **1** is implemented as
> tasks **14.1â€“14.4** (`controllers/security.py`, `controllers/common.py`,
> `data/church_mission_api_user.xml`) and section **6.1** as task **19.1**
> (`controllers/dashboard_controller.py`). Sections **2â€“5** remain planned (task.md groups
> 15â€“18). The checkboxes below are kept in sync with the task board.

---

## 1. Security Infrastructure & API Key Authentication

- [x] **1.1 API Key Auth Decorator**
  - [x] Extract `X-Api-Key` and `X-Database` from incoming HTTP request headers.
  - [x] Authenticate key against `res.users.apikeys` via `sudo()._check_credentials()`.
  - [x] Return standard `401 Unauthorized` or `403 Forbidden` JSON if missing or invalid.
  - [x] Deliverable: [controllers/security.py](controllers/security.py) (`@require_mobile_api_key`).

- [x] **1.2 Execution Context Switcher**
  - [x] Switch environment user context (`request.update_env(user=user_id)`) to enforce Odoo ACL rules.
  - [x] Ensure Read Only security groups reject POST/PUT/DELETE operations with `403 Forbidden`.
  - [x] Deliverable: [controllers/security.py](controllers/security.py).

- [x] **1.3 Unified JSON Response & Error Envelope**
  - [x] Implement standardized response wrapper (`{"success": true, "data": ...}`).
  - [x] Implement exception handler capturing Odoo `AccessError`, `ValidationError`, and `UserError` without leaking tracebacks.
  - [x] Deliverable: [controllers/common.py](controllers/common.py).

- [x] **1.4 Mobile API Service User Data Setup**
  - [x] Define dedicated system user for API access with configurable access roles.
  - [x] Deliverable: [data/church_mission_api_user.xml](data/church_mission_api_user.xml).

---

## 2. Mission Master Data Endpoints

- [x] **2.1 Mission Types (`/api/v1/mobile/mission/master/types`)**
  - [x] Implement `GET` endpoint returning active mission types (`church.mission.type`).
  - [x] Support filter parameters: `active`.
  - [x] Deliverable: [controllers/master_controller.py](controllers/master_controller.py).

- [x] **2.2 Mission Fields (`/api/v1/mobile/mission/master/fields`)**
  - [x] Implement `GET` endpoint returning geographic fields/regions (`church.mission.field`).
  - [x] Support pagination parameters: `limit`, `offset`.
  - [x] Deliverable: [controllers/master_controller.py](controllers/master_controller.py).

- [x] **2.3 Status Records (`/api/v1/mobile/mission/master/statuses`)**
  - [x] Implement `GET` endpoint returning trip statuses (`church.mission.status`) and missionary statuses (`church.missionary.status`).
  - [x] Deliverable: [controllers/master_controller.py](controllers/master_controller.py).

- [x] **2.4 Participant Roles (`/api/v1/mobile/mission/master/roles`)**
  - [x] Implement `GET` endpoint returning available participant roles (`church.mission.role`).
  - [x] Deliverable: [controllers/master_controller.py](controllers/master_controller.py).

---

## 3. Mission Trips Endpoints (`/api/v1/mobile/mission/trips`)

- [x] **3.1 Mission Trips List (`GET /`)**
  - [x] Return paginated trips with status, mission field, date ranges, and funding progress.
  - [x] Query domain filtering: by `field_id`, `status_id`, `date_begin`, `date_end`.
  - [x] Deliverable: [controllers/trip_controller.py](controllers/trip_controller.py).

- [x] **3.2 Mission Trip Detail (`GET /<int:trip_id>`)**
  - [x] Fetch complete trip payload including inherited `event.event` fields, budget, description, and coordinator details.
  - [x] Deliverable: [controllers/trip_controller.py](controllers/trip_controller.py).

- [x] **3.3 Trip Participants List (`GET /<int:trip_id>/participants`)**
  - [x] Return confirmed participants (`church.mission_participant`) linked to the trip.
  - [x] Include partner details (name, phone, role).
  - [x] Deliverable: [controllers/trip_controller.py](controllers/trip_controller.py).

- [x] **3.4 Trip Participant Registration (`POST /<int:trip_id>/register`)**
  - [x] Handle registration payload (`partner_id`, `role_id`, `notes`).
  - [x] Validate trip capacity and dates before creating participant record.
  - [x] Deliverable: [controllers/trip_controller.py](controllers/trip_controller.py).

---

## 4. Missionaries & Agencies Endpoints (`/api/v1/mobile/missionaries`)

- [ ] **4.1 Missionaries List (`GET /`)**
  - [ ] Return active missionaries (`church.missionary`) with contact details from inherited `res.partner`.
  - [ ] Deliverable: `controllers/missionary_controller.py`.

- [ ] **4.2 Missionary Profile (`GET /<int:missionary_id>`)**
  - [ ] Return full missionary record, sending agency details, field assignment, and total support received.
  - [ ] Deliverable: `controllers/missionary_controller.py`.

- [ ] **4.3 Missionary Image Route (`GET /<int:missionary_id>/avatar`)**
  - [ ] Serve cached binary avatar from `res.partner.image_1920` / `image_256` with HTTP 304 support.
  - [ ] Deliverable: `controllers/missionary_controller.py`.

- [ ] **4.4 Mission Agencies Directory (`GET /agencies`)**
  - [ ] Return registered mission agencies (`church.mission_agency`) along with assigned active missionary counts.
  - [ ] Deliverable: `controllers/agency_controller.py`.

---

## 5. Mission Support Endpoints (`/api/v1/mobile/mission/support`)

- [ ] **5.1 Support Metrics Summary (`GET /summary`)**
  - [ ] Compute funding metrics: total pledges, collected amounts, and target attainment percentages.
  - [ ] Deliverable: `controllers/support_controller.py`.

- [ ] **5.2 Submit Support Entry (`POST /pledge`)**
  - [ ] Validate payload: ensure positive amount, donor partner ID, and trip or missionary assignment.
  - [ ] Create record in `church.mission_support` with draft/pending status.
  - [ ] Deliverable: `controllers/support_controller.py`.

- [ ] **5.3 Support History Log (`GET /history`)**
  - [ ] Fetch paginated payment and support records filtered by donor partner or target entity.
  - [ ] Deliverable: `controllers/support_controller.py`.

---

## 6. Mobile Dashboard Endpoint (`/api/v1/mobile/mission/dashboard`)

- [x] **6.1 Consolidated KPI & Chart Data (`GET /metrics`)**
  - [x] Aggregate data corresponding to the 8 web mission dashboard dashlets.
  - [x] Return KPI card counters (active trips, missionaries in field, total support raised, upcoming departures).
  - [x] Return pre-aggregated time-series and categorical data for Flutter chart rendering.
  - [x] Deliverable: [controllers/dashboard_controller.py](controllers/dashboard_controller.py).

