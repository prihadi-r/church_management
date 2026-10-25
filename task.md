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

- ⬜ Upgrade the running databases (`demo`) to `18.0.2.2.0` — they are still on `2.0.0`.
- ⬜ Screenshots for the Mission dashboard under `screenshots/`.
- ⬜ Optional: public "Missions" page on the website (reuse `event.event` data).
- ⬜ Optional: auto-create `church.mission.participant` from `event.registration`.
- ⬜ Optional: currency conversion for support totals in multi-currency setups.
- ⬜ Optional: portal access so missionaries can see their own support progress.
