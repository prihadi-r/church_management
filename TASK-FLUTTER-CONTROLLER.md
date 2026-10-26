# Task Board — Odoo Mobile API Controllers (`church_management`)

---

## 1. Security Infrastructure & API Key Authentication

- [ ] **1.1 API Key Auth Decorator**
  - [ ] Extract `X-Api-Key` and `X-Database` from incoming HTTP request headers.
  - [ ] Authenticate key against `res.users.apikeys` via `sudo()._check_credentials()`.
  - [ ] Return standard `401 Unauthorized` or `403 Forbidden` JSON if missing or invalid.
  - [ ] Deliverable: `controllers/security.py` (`@require_mobile_api_key`).

- [ ] **1.2 Execution Context Switcher**
  - [ ] Switch environment user context (`request.update_env(user=user_id)`) to enforce Odoo ACL rules.
  - [ ] Ensure Read Only security groups reject POST/PUT/DELETE operations with `403 Forbidden`.
  - [ ] Deliverable: `controllers/security.py`.

- [ ] **1.3 Unified JSON Response & Error Envelope**
  - [ ] Implement standardized response wrapper (`{"success": true, "data": ...}`).
  - [ ] Implement exception handler capturing Odoo `AccessError`, `ValidationError`, and `UserError` without leaking tracebacks.
  - [ ] Deliverable: `controllers/common.py`.

- [ ] **1.4 Mobile API Service User Data Setup**
  - [ ] Define dedicated system user for API access with configurable access roles[cite: 1].
  - [ ] Deliverable: `data/church_mission_api_user.xml`.

---

## 2. Mission Master Data Endpoints

- [ ] **2.1 Mission Types (`/api/v1/mobile/mission/master/types`)**
  - [ ] Implement `GET` endpoint returning active mission types (`church.mission.type`)[cite: 1].
  - [ ] Support filter parameters: `active`.
  - [ ] Deliverable: `controllers/master_controller.py`.

- [ ] **2.2 Mission Fields (`/api/v1/mobile/mission/master/fields`)**
  - [ ] Implement `GET` endpoint returning geographic fields/regions (`church.mission.field`)[cite: 1].
  - [ ] Support pagination parameters: `limit`, `offset`.
  - [ ] Deliverable: `controllers/master_controller.py`.

- [ ] **2.3 Status Records (`/api/v1/mobile/mission/master/statuses`)**
  - [ ] Implement `GET` endpoint returning trip statuses (`church.mission.status`) and missionary statuses (`church.missionary.status`)[cite: 1].
  - [ ] Deliverable: `controllers/master_controller.py`.

- [ ] **2.4 Participant Roles (`/api/v1/mobile/mission/master/roles`)**
  - [ ] Implement `GET` endpoint returning available participant roles (`church.mission.role`)[cite: 1].
  - [ ] Deliverable: `controllers/master_controller.py`.

---

## 3. Mission Trips Endpoints (`/api/v1/mobile/mission/trips`)

- [ ] **3.1 Mission Trips List (`GET /`)**
  - [ ] Return paginated trips with status, mission field, date ranges, and funding progress.
  - [ ] Query domain filtering: by `field_id`, `status_id`, `date_begin`, `date_end`.
  - [ ] Deliverable: `controllers/trip_controller.py`.

- [ ] **3.2 Mission Trip Detail (`GET /<int:trip_id>`)**
  - [ ] Fetch complete trip payload including inherited `event.event` fields, budget, description, and coordinator details[cite: 1].
  - [ ] Deliverable: `controllers/trip_controller.py`.

- [ ] **3.3 Trip Participants List (`GET /<int:trip_id>/participants`)**
  - [ ] Return confirmed participants (`church.mission_participant`) linked to the trip[cite: 1].
  - [ ] Include partner details (name, phone, role)[cite: 1].
  - [ ] Deliverable: `controllers/trip_controller.py`.

- [ ] **3.4 Trip Participant Registration (`POST /<int:trip_id>/register`)**
  - [ ] Handle registration payload (`partner_id`, `role_id`, `notes`).
  - [ ] Validate trip capacity and dates before creating participant record.
  - [ ] Deliverable: `controllers/trip_controller.py`.

---

## 4. Missionaries & Agencies Endpoints (`/api/v1/mobile/missionaries`)

- [ ] **4.1 Missionaries List (`GET /`)**
  - [ ] Return active missionaries (`church.missionary`) with contact details from inherited `res.partner`[cite: 1].
  - [ ] Deliverable: `controllers/missionary_controller.py`.

- [ ] **4.2 Missionary Profile (`GET /<int:missionary_id>`)**
  - [ ] Return full missionary record, sending agency details, field assignment, and total support received.
  - [ ] Deliverable: `controllers/missionary_controller.py`.

- [ ] **4.3 Missionary Image Route (`GET /<int:missionary_id>/avatar`)**
  - [ ] Serve cached binary avatar from `res.partner.image_1920` / `image_256` with HTTP 304 support.
  - [ ] Deliverable: `controllers/missionary_controller.py`.

- [ ] **4.4 Mission Agencies Directory (`GET /agencies`)**
  - [ ] Return registered mission agencies (`church.mission_agency`) along with assigned active missionary counts[cite: 1].
  - [ ] Deliverable: `controllers/agency_controller.py`.

---

## 5. Mission Support Endpoints (`/api/v1/mobile/mission/support`)

- [ ] **5.1 Support Metrics Summary (`GET /summary`)**
  - [ ] Compute funding metrics: total pledges, collected amounts, and target attainment percentages.
  - [ ] Deliverable: `controllers/support_controller.py`.

- [ ] **5.2 Submit Support Entry (`POST /pledge`)**
  - [ ] Validate payload: ensure positive amount, donor partner ID, and trip or missionary assignment[cite: 1].
  - [ ] Create record in `church.mission_support` with draft/pending status[cite: 1].
  - [ ] Deliverable: `controllers/support_controller.py`.

- [ ] **5.3 Support History Log (`GET /history`)**
  - [ ] Fetch paginated payment and support records filtered by donor partner or target entity.
  - [ ] Deliverable: `controllers/support_controller.py`.

---

## 6. Mobile Dashboard Endpoint (`/api/v1/mobile/mission/dashboard`)

- [ ] **6.1 Consolidated KPI & Chart Data (`GET /metrics`)**
  - [ ] Aggregate data corresponding to the 8 web mission dashboard dashlets[cite: 1].
  - [ ] Return KPI card counters (active trips, missionaries in field, total support raised, upcoming departures).
  - [ ] Return pre-aggregated time-series and categorical data for Flutter chart rendering.
  - [ ] Deliverable: `controllers/dashboard_controller.py`.
```<FollowUp>
Would you like me to generate the complete implementation code for the Odoo API key authentication decorator (`controllers/security.py`) or the Flutter Riverpod networking client (`dio_client.dart`) next?
</FollowUp>