# ⛪ Darash — Open Source Church Management System (ChMS)

> **Your church, beautifully managed.**

**Darash** is a free, open-source **Church Management System (ChMS)** built on the **Odoo 18** framework. It helps congregations manage **membership & family records**, **worship event scheduling**, **baptism & marriage registrations**, **tithing & donations**, **ministry / volunteer coordination**, **Sunday school classes, students & attendance**, **prayer requests**, and **church news** — all in a single application. No more physical books or scattered spreadsheets.

Whether you lead a small congregation or a growing ministry, Darash centralizes your church operations into one clean, modern dashboard so your team can focus on what matters most: people.

> Built with the assistance of **GitHub Copilot as a vibe coding assistant**.
> This module is **free to use, modify, and distribute** under the **LGPL-3** license.

![Odoo](https://img.shields.io/badge/Odoo-18.0-714B67?style=for-the-badge&logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10--3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14--16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![XML](https://img.shields.io/badge/Views-XML-8A2BE2?style=for-the-badge)
![OWL](https://img.shields.io/badge/UI-OWL%20JS-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![feedparser](https://img.shields.io/badge/RSS-feedparser-FF6600?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Copilot](https://img.shields.io/badge/Built%20with-GitHub%20Copilot-000000?style=for-the-badge&logo=githubcopilot&logoColor=white)
![License](https://img.shields.io/badge/License-LGPL--3-blue?style=for-the-badge)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)

## 📌 Why Darash?

- ✅ **100% free & open source** — no licensing fees, no vendor lock-in (LGPL-3).
- ✅ **Runs on the proven Odoo ERP platform** — extend it with 40,000+ Odoo apps.
- ✅ **Church-specific workflows** — baptism/marriage registration, care cells (small groups), Sunday school classes with attendance, musician scheduling, event rosters.
- ✅ **Public website out of the box** — themed homepage, public church calendar, prayer request form, and news aggregator.
- ✅ **Self-hosted** — keep your church data private with Docker or your own server.

## 🧱 Tech Stack & Architecture

| Layer | Technology |
|-------|------------|
| **Framework** | [Odoo 18](https://www.odoo.com) (Python-based ERP / CRM platform) |
| **Language** | Python 3.10 – 3.12 |
| **Database** | PostgreSQL 14 – 16 |
| **Views / UI** | XML views + OWL JS (Odoo Web Library) |
| **Web** | Odoo Website (QWeb templates) |
| **News / RSS** | `feedparser` |
| **Deployment** | Docker / Docker Compose |

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack & Architecture](#-tech-stack--architecture)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Docker Quick Start](#-docker-quick-start)
- [Menu Structure](#-menu-structure)
- [Documentation](#-documentation)
- [Version History](#-version-history)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🏠 Church Dashboard (interactive graphs)
- Built on Odoo's **Dashboards** app (`board`): the landing page is a grid of **graph boxes**, not text cards.
- Eight dashlets — congregants per member type, baptisms per month, marriages per month,
  prayer requests by status, Sunday School students & sessions per class, Sunday School
  attendance by status, and care cells by status.
- Every box is a live graph: switch it to **bar / line / pie**, change the measure it computes,
  or filter it using the controls inside the box.
- Personal per user: pick the column layout (**Change Layout**), fold or hide boxes, and add your
  own dashlets from any list, kanban, graph or pivot view.

### 🧑‍🤝‍🧑 Membership & Master Data
- **Member Types** (Simpatisan, Jemaat Tetap, Musisi, Pastur, ...).
- **Care Cells** (cell groups / komsel) with attendees and sessions.
- **Donation Types** and **Sacrament Types**.
- **Event Roles** and **Musician Roles**.

### 🗓️ Operations
- **Event Rosters** — assign officers (role + contact) to worship events.
- **Musician Schedule** — calendar-based scheduling with role and time slots.
- **Baptism Registrations** — kanban + calendar workflow (*Submit for Review → Approve → Mark Completed*), auto-calculated age, officiating minister (Pastor type only).
- **Marriage Registrations** — kanban + calendar workflow with groom/bride.
- **Pray Requests** — public web form (`/church-pray`) to submit prayer requests; backend with kanban/calendar/list/pivot views, status workflow, and prayer sessions (date, time, prayers, notes). Dashboard card + shortcut.
- **Church Calendar** — one unified calendar aggregating events, musician schedules, baptisms, marriages, and prayer requests (daily auto-refresh cron).
- **Public Church Calendar** — a public website page (`/church-calendar`) that shows **confirmed** activities (events, baptisms, marriages, care cells, prayer requests) with **type filters** and **month/type grouping**. Musician schedules and unconfirmed entries are excluded.

### 📖 Sunday School (Sekolah Minggu)
- **Classes** — one per class level (Toddler, Kindergarten, Primary, Teen, Youth) with room,
  weekly meeting time, capacity, head teacher, status and computed student/teacher/session counts.
- **Teachers** — delegate to `res.partner` (`_inherits`), so name, phone and email come straight
  from Contacts; roles (**Supervisor**, **Head Teacher**, **Assistant**, **Substitute**) are
  assigned per class.
- **Students** — also delegate to `res.partner`, with an auto-generated code (`SS/2026/0001`),
  birth date & computed age, class, status, guardian and a computed attendance rate.
- **Sessions** — dated class meetings (topic, teacher, start/end, status) that are also pushed
  to the Church Calendar.
- **Attendance** — one line per student per session (**Present / Late / Permission / Sick /
  Absent**) feeding per-student and per-class attendance rates.
- **Configuration** — class levels, teacher roles, and the class / student / session /
  attendance statuses.
- Ships with **sample data**: 5 classes × 20 students, 12 teachers, 15 sessions and
  200 attendance lines, so the graphs and dashboards are populated out of the box.

### 🚀 Missions
- **Mission Trips** — a trip **is an Event** (`event.event` via `_inherits`): name, dates, venue,
  registrations and calendar sync come from the Events app, plus mission type, field, sending
  agency, leader, budget and computed support/funding progress. Auto code `MT/2026/0001`.
- **Missionaries** — delegate to `res.partner` (`_inherits`) with mission field, sending agency,
  status, supervisor, support target and computed support progress. Auto code `MSN/2026/0001`.
- **Participants** — trip team members with a **Role** and confirmation flag; unique per trip.
- **Mission Support** — donor contributions per missionary/trip, reusing `church.donation.type`
  and optionally linked to `account.payment`; auto code `MSP/2026/0001`.
- **Mission Dashboard** — its own board with graphs: trips by status/type/field, missionaries by
  status, participants by role, and support per month/missionary/donation type.
- **Configuration** — mission fields, types, statuses, roles, missionary statuses and agencies
  (all master data, **no hard-coded selection fields**).
- Ships with **sample data**: 2 agencies, 5 missionaries, 5 trips, 9 participants, 8 support lines.

### 📰 News & Website
- **News articles, categories, and sources** with RSS/feed ingestion (`feedparser`).
- **Public Christianity News page** (`/christianity-news`) — category filters and article cards, linked from the homepage and the main website menu.

### 🌐 Public Website
- **Themed homepage** — hero, *What We Offer* feature cards, church calendar preview, and call-to-action sections.
- **Public Church Calendar** (`/church-calendar`) — confirmed activities with type filters & month/type grouping.
- **Prayer Request form** (`/church-pray`) — public submission without login.
- **Christianity News** (`/christianity-news`) — public news aggregator page.
- **SEO** — homepage title, meta description & meta keywords (e.g. "church management", "modern church", "digital church").

### 🔌 Integrations
- Extends **Contacts** (`res.partner`), **CRM Leads** (`crm.lead`), **Events** (`event.event`), and **Accounting Payments** (`account.payment`).
- Sunday School **students** and **teachers** inherit `res.partner` through Odoo's delegation
  inheritance (`_inherits`), so they reuse the contact's name, phone, email and address instead
  of duplicating them.
- **Mission** reuses the same delegation patterns: missionaries, participants and mission agencies
  inherit `res.partner`, while **mission trips inherit `event.event`** (so they are real Events and
  appear automatically in the Church Calendar).

---

## 📋 Requirements

| Requirement | Version / Value |
|-------------|-----------------|
| **Odoo** | 18.0+ |
| **Python** | `feedparser` |
| **Odoo apps** | `base`, `board`, `crm`, `event`, `account`, `website` |

> 🎨 **Optional companion:** [`church_theme`](#) — a separate website theme that provides the public homepage design (hero, feature cards, CTA). Install it if you want the themed homepage; without it the module still works fully but uses Odoo's default website theme.

---

## 🚀 Installation

> ⚠️ **Requires the `website` module** (plus `base`, `board`, `crm`, `event`, `account`). If `website` is not installed, Odoo reports `Unmet dependencies: website` and the module stays stuck in `to install`. Install the missing apps first.

1. Copy this folder into your Odoo addons directory.
2. Install the Python dependency:

   ```bash
   pip install feedparser
   ```

3. Update the module list in Odoo (**Apps → Update Apps List**).
4. Search for **Church Management** and click **Install**.

Alternatively, install everything from the CLI (auto-resolves the dependency graph):

```bash
odoo -i website,church_management -d <your_db> --stop-after-init
```

After installing, assign one of the **Church Management** groups (**Read Only** / **Write Only** / **Full Access**) to users under **Settings → Users → Access Rights**, or the menu will not appear.

---

## 🐳 Docker Quick Start

Run the whole stack (**Odoo 18 + PostgreSQL**) with **Docker Compose** — no local Odoo / Python / PostgreSQL install needed.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) with **Docker Compose v2** (bundled with Docker Desktop).

### 1. Clone the repository
```bash
git clone https://github.com/prihadi-r/church_management.git
cd church_management
```

> Default database credentials are `odoo` / `odoo` (defined in both `odoo.conf` and `docker-compose.yml`). If you change them, change them **together** — and use a strong password in production.

### 2. Build & start
```bash
docker compose up -d --build
```

- **Odoo web UI:** http://localhost:8069
- Data is stored in the named volumes `odoo-web-data` and `odoo-db-data` (persisted across restarts).

### 3. Create the database & install the module
1. Open http://localhost:8069 and create a database (Master Password: `admin` by default — change it in production).
2. Log in, then go to **Apps → Update Apps List**.
3. Search for **Church Management** and click **Install**.
   > The `website`, `crm`, `event`, and `account` apps install automatically as dependencies.

> 💡 **Automated install (CLI):** instead of the web UI, run
> ```bash
> docker compose exec web odoo -i website,church_management -d <your_db> --stop-after-init
> ```

After installing, assign one of the **Church Management** groups (**Read Only** / **Write Only** / **Full Access**) to users under **Settings → Users → Access Rights**, or the menu will not appear.

### Common commands
| Task | Command |
|------|---------|
| View logs | `docker compose logs -f web` |
| Stop services | `docker compose down` |
| Stop & wipe all data | `docker compose down -v` |
| Rebuild the image | `docker compose up -d --build` |
| Restart Odoo | `docker compose restart web` |
| Run a shell inside Odoo | `docker compose exec web odoo shell -d <your_db> --no-http` |

### Customising
- **Ports:** change `"8069:8069"` in `docker-compose.yml` (left side = host port).
- **Database credentials:** edit `odoo.conf` **and** the `db` service environment in `docker-compose.yml` together.
- **Module code:** the repo root is bind-mounted into `/mnt/extra-addons/church_management`, so code edits are picked up without rebuilding. Restart `web` (`docker compose restart web`) after model/field changes.
- **Configuration:** `odoo.conf` is mounted to `/etc/odoo/odoo.conf` inside the container.

> 🎨 **Optional companion:** the public themed homepage comes from the separate [`church_theme`](#) module — place it in `/mnt/extra-addons` (e.g. alongside this repo) if you want the designed homepage.

---

## 🗺️ Menu Structure

```
Church Management
├── Dashboard                       (graph board — Odoo Dashboards app)
├── Master Data
│   ├── Member Types
│   ├── Care Cells
│   ├── Donation Types
│   ├── Sacrament Types
│   ├── Event Roles
│   └── Musician Roles
├── Sunday School
│   ├── Classes
│   ├── Teachers
│   ├── Students
│   ├── Sessions
│   ├── Attendance
│   └── Configuration
│       ├── Class Levels
│       ├── Teacher Roles
│       ├── Class Statuses
│       ├── Student Statuses
│       ├── Attendance Statuses
│       └── Session Statuses
├── Mission                         (missions & missionaries)
│   ├── Dashboard                   (graph board)
│   ├── Mission Trips
│   ├── Missionaries
│   ├── Participants
│   ├── Mission Support
│   └── Configuration
│       ├── Mission Fields
│       ├── Mission Types
│       ├── Mission Statuses
│       ├── Mission Roles
│       ├── Missionary Statuses
│       └── Mission Agencies
└── Operations
    ├── Event Rosters
    ├── Musician Schedule
    ├── Baptism Registrations
    ├── Marriage Registrations
    ├── Pray Requests
    └── Church Calendar
```

---

## 📖 Documentation

- [Installation Guide](INSTALLATION_GUIDE.md) — requirements & step-by-step install.
- [User Guide](USER_GUIDE.md) — detailed usage instructions (in Indonesian).
- [Task Board](task.md) — scope, acceptance criteria and backlog of the current milestone.
- [Progress Log](progress.md) — completed work, verification evidence and open items.

## 🖥️ Live Demo

A live deployment of this Church Management System is available at [**cm.gosyen.love**](https://cm.gosyen.love) — explore the themed public homepage, the public church calendar, and the Christianity News aggregator without installing anything.

## 🧑‍🤝‍🧑 Contributing

Contributions, bug reports, and feature requests are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before getting started.

- 🐛 Found a bug? [Open an issue](https://github.com/prihadi-r/church_management/issues/new/choose).
- ✨ Want a feature? [Submit a feature request](https://github.com/prihadi-r/church_management/issues/new/choose).
- 🚀 Ready to help? Fork the repo and open a pull request.

> **Star ⭐ this repository** if you find it useful — it helps others discover this open-source church software.

---

## 📜 Version History

| Version | Date | Changes |
|---------|------|---------|
| **2.2.0** | 2026-10-25 | **Mission** — new **Mission** app: mission trips (inherit `event.event`), missionaries / participants / agencies (inherit `res.partner`), mission support (reuses donation types and `account.payment`), master data for fields/types/statuses/roles/missionary statuses (no selection fields), a dedicated **Mission Dashboard** board, and sample data. |
| **2.1.0** | 2026-10-24 | **Sunday School & graph dashboard** — new **Sunday School** app (classes, teachers, students, sessions, attendance + configuration masters; students & teachers inherit `res.partner`), sample data (5 classes × 20 students, 12 teachers, 15 sessions, 200 attendance lines), and the dashboard rebuilt on Odoo's **Dashboards** (`board`) app as eight interactive bar/pie graph dashlets instead of text cards. |
| **2.0.0** | 2026-08-09 | **Darash major release** — branded as **Darash**, themed public homepage, Christianity News page & nav link, homepage SEO, unified color theme across all public pages, and deployment tooling (`scripts/`). |
| **1.2.0** | 2026-08-09 | **Website polish** — themed homepage content, **Christianity News** section & main-menu link, **SEO** metadata for the homepage, and documented the optional companion `church_theme`. |
| **1.1.1** | 2026-08-08 | **Fixes & docs** — fixed menu load-order bug causing `ParseError` (`External ID not found: menu_church_operations`) on fresh installs by centralizing all menus in `church_parent_menu.xml`; hardened install/troubleshooting docs (requires `website`, security-group setup, Odoo 17→18 `vat_check_vies` cleanup). |
| **1.1.0** | 2026-08-08 | **Pray Requests** — new feature: public submission form (`/church-pray`), CRUD under **Operations → Pray Requests**, prayer sessions (date, time, prayers, notes), **Kanban / Calendar / List / Pivot / Form** views, **Dashboard** stat card + shortcut, automatic **Church Calendar** sync, and sample data. Also: cohort-style **Pivot** view replaces the grid view (unsupported in Odoo 18). |
| **1.0.2** | — | **Public Church Calendar** (`/church-calendar`) — type filters, month/type grouping, only confirmed activities shown. |

---

## 👤 Author

**Prihadi** — [prihadi.r@gmail.com](mailto:prihadi.r@gmail.com)

---

## 📄 License

**LGPL-3** — free to use, modify, and distribute.
