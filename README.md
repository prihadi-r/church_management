# ⛪ Church Management

A comprehensive **Odoo 18** module for managing church membership, events, donations, sacraments, and news — all in a single application. No more physical books or scattered spreadsheets.

> Built with the assistance of **GitHub Copilot as a vibe coding assistant**.
> This module is **free to use and modify**.

![Odoo](https://img.shields.io/badge/Odoo-18.0-714B67?style=for-the-badge&logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10--3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14--16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![XML](https://img.shields.io/badge/Views-XML-8A2BE2?style=for-the-badge)
![OWL](https://img.shields.io/badge/UI-OWL%20JS-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![feedparser](https://img.shields.io/badge/RSS-feedparser-FF6600?style=for-the-badge)
![GitHub Copilot](https://img.shields.io/badge/Built%20with-GitHub%20Copilot-000000?style=for-the-badge&logo=githubcopilot&logoColor=white)
![License](https://img.shields.io/badge/License-LGPL--3-blue?style=for-the-badge)

---

## ✨ Features

### 🏠 Dashboard
- Live statistic cards: **congregants**, **baptisms**, **marriages**, and **worship schedule** (this month / last month / pending).
- **Congregants per member type** breakdown.
- Quick-access shortcuts to Baptism Registrations, Marriage Registrations, and Church Calendar.

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

---

## 📋 Requirements

| Requirement | Version / Value |
|-------------|-----------------|
| **Odoo** | 18.0+ |
| **Python** | `feedparser` |
| **Odoo apps** | `base`, `crm`, `event`, `account`, `website` |

> 🎨 **Optional companion:** [`church_theme`](#) — a separate website theme that provides the public homepage design (hero, feature cards, CTA). Install it if you want the themed homepage; without it the module still works fully but uses Odoo's default website theme.

---

## 🚀 Installation

> ⚠️ **Requires the `website` module** (plus `base`, `crm`, `event`, `account`). If `website` is not installed, Odoo reports `Unmet dependencies: website` and the module stays stuck in `to install`. Install the missing apps first.

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

## 🗺️ Menu Structure

```
Church Management
├── Dashboard
├── Master Data
│   ├── Member Types
│   ├── Care Cells
│   ├── Donation Types
│   ├── Sacrament Types
│   ├── Event Roles
│   └── Musician Roles
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

---

## 📜 Version History

| Version | Date | Changes |
|---------|------|---------|
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
