# ⛪ Church Management

A comprehensive **Odoo 18** module for managing church membership, events, donations, sacraments, and news — all in a single application. No more physical books or scattered spreadsheets.

> Built with the assistance of **GitHub Copilot as a vibe coding assistant**.
> This module is **free to use and modify**.

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
- **News articles, categories, and sources** with RSS/feed ingestion (`feedparser`), published to the website.

### 🔌 Integrations
- Extends **Contacts** (`res.partner`), **CRM Leads** (`crm.lead`), **Events** (`event.event`), and **Accounting Payments** (`account.payment`).

---

## 📋 Requirements

| Requirement | Version / Value |
|-------------|-----------------|
| **Odoo** | 18.0+ |
| **Python** | `feedparser` |
| **Odoo apps** | `base`, `crm`, `event`, `account`, `website` |

---

## 🚀 Installation

1. Copy this folder into your Odoo addons directory.
2. Install the Python dependency:

   ```bash
   pip install feedparser
   ```

3. Update the module list in Odoo (**Apps → Update Apps List**).
4. Search for **Church Management** and click **Install**.

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

## � Version History

| Version | Date | Changes |
|---------|------|---------|
| **1.1.0** | 2026-08-08 | **Pray Requests** — new feature: public submission form (`/church-pray`), CRUD under **Operations → Pray Requests**, prayer sessions (date, time, prayers, notes), **Kanban / Calendar / List / Pivot / Form** views, **Dashboard** stat card + shortcut, automatic **Church Calendar** sync, and sample data. Also: cohort-style **Pivot** view replaces the grid view (unsupported in Odoo 18). |
| **1.0.2** | — | **Public Church Calendar** (`/church-calendar`) — type filters, month/type grouping, only confirmed activities shown. |

---

## �👤 Author

**Prihadi** — [prihadi.r@gmail.com](mailto:prihadi.r@gmail.com)

---

## 📄 License

**LGPL-3** — free to use, modify, and distribute.
