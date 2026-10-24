{
    'name': 'Darash - Church Management',
    'version': '2.1.0',
    'summary': 'Open-source Church Management System (ChMS): membership, tithing & donations, worship event scheduling, baptism & marriage registration, ministry and news for Odoo 18.',
    'author': 'Prihadi <prihadi.r@gmail.com>',
    'description': """
# ⛪ Darash - Church Management

> **Your church, beautifully managed.**

A comprehensive **Odoo 18** module for managing church membership, events,
donations, sacraments, and news in a single application — no more physical
books or scattered spreadsheets.

Built with the assistance of **GitHub Copilot as a vibe coding assistant**.
This module is **free to use and modify**.

---

## ✨ Features

### Dashboard
- Home page with live statistic cards: **congregants**, **baptisms**,
  **marriages**, and **worship schedule** (this month / last month / pending).
- **Congregants per member type** breakdown and quick-access shortcuts.

### Membership & Master Data
- **Member Types** (Simpatisan, Jemaat Tetap, Musisi, Pastur, ...).
- **Care Cells** (cell groups / komsel) with attendees and sessions.
- **Donation Types** and **Sacrament Types**.
- **Event Roles** and **Musician Roles**.

### Operations
- **Event Rosters** — assign officers (role + contact) to worship events.
- **Musician Schedule** — calendar-based scheduling with role and time slots.
- **Baptism Registrations** — kanban + calendar workflow
  (*Submit for Review → Approve → Mark Completed*), auto-calculated age,
  officiating minister (Pastor type only).
- **Marriage Registrations** — kanban + calendar workflow with groom/bride.
- **Church Calendar** — one unified calendar aggregating events, musician
  schedules, baptisms, and marriages (daily auto-refresh cron).

### News & Website
- **News articles, categories, and sources** with RSS/feed ingestion
  (`feedparser`), published to the website.

### Integrations
- Extends **Contacts** (`res.partner`), **CRM Leads** (`crm.lead`),
  **Events** (`event.event`), and **Accounting Payments** (`account.payment`).

---

## 📋 Requirements

- **Odoo 18.0+**
- **Python**: `feedparser`
- **Odoo apps**: `base`, `crm`, `event`, `account`, `website`

---

## 🚀 Installation

1. Copy this folder into your Odoo addons directory.
2. Install the Python dependency: `pip install feedparser`.
3. Update the module list in Odoo (Apps → Update Apps List).
4. Search for **Church Management** and click **Install**.

---

## 🗺️ Menu Structure

```
Church Management
├── Dashboard
├── Master Data
│   ├── Member Types / Care Cells / Donation Types
│   ├── Sacrament Types / Event Roles / Musician Roles
└── Operations
    ├── Event Rosters / Musician Schedule
    ├── Baptism Registrations / Marriage Registrations
    └── Church Calendar
```

---

## 👤 Author

**Prihadi** — [prihadi.r@gmail.com](mailto:prihadi.r@gmail.com)

---

## 📄 License

**LGPL-3** — free to use, modify, and distribute.
""",
    'category': 'Services/Church',
    'depends': ['base', 'board', 'crm', 'event', 'account', 'website'],

    'external_dependencies': {
        'python': ['feedparser'],
    },

    'post_init_hook': 'post_init_hook',
    'data': [
        'security/church_security.xml',
        'security/ir.model.access.csv',
        'data/church_sunday_school_data.xml',
        # Sample data: 5 classes x 20 students. Loaded right after the master
        # data it references (levels, statuses, teacher roles, student sequence).
        'data/church_sunday_school_sample.xml',
        'data/church_care_cell_status_sample.xml',
        'data/church_care_cell_type_sample.xml',   
        'data/church_member_type_sample.xml',
        'data/church_donation_type_sample.xml',
        'data/church_sacrament_type_sample.xml',
        'data/res_partner_sample.xml',
        'data/crm_lead_sample.xml',
        'data/church_baptism_registration_sample.xml',
        'data/event_event_sample.xml',
        'data/church_musician_role_sample.xml',
        'data/church_marriage_registration_sample.xml',
        # 56 congregations (Indonesian names) involved in marriage, baptism,
        # and care-cell events from the current month (Aug 2026) up to two
        # months ahead (Oct 2026).
        'data/church_congregation_sample.xml',
        'data/church_news_initial_sources_data.xml',
        'data/church_news_categories_data.xml',
        'data/church_news_cron_data.xml',
        'views/church_activity_views.xml',
        'views/church_care_cell_views.xml',
        'views/church_menu_and_views.xml',
        'views/church_baptism_registration_views.xml',
        'views/church_musician_role_views.xml',
        'views/church_marriage_registration_views.xml',
        'views/church_pray_request_views.xml',
        # Sample data loaded AFTER the pray views so the seq_church_pray_request
        # ir.sequence is defined before records are created (create() calls
        # ir.sequence.next_by_code).
        'data/church_pray_request_sample.xml',
        # Dashboard is a board (Odoo "Dashboards" app) built from graph
        # dashlets. Its arch references only the actions declared in the same
        # file, so it does not depend on the load order of the other views.
        'views/church_dashboard_board_views.xml',
        'views/musician_schedule_view.xml',
        'views/church_inherited_views.xml',
        'views/crm_sacrament_kanban.xml',
        'views/church_parent_menu.xml',
        'views/church_sunday_school_master_views.xml',
        'views/church_sunday_school_views.xml',
        'views/church_sunday_school_menu.xml',
        'views/church_news_source_views.xml',
        'views/church_news_article_views.xml',
        'views/church_news_category_views.xml',
        'views/church_news_menu_views.xml',
        'views/church_news_website_templates.xml',
        'views/church_homepage_news.xml',
        'views/church_calendar_website_templates.xml',
        'views/church_pray_website_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'church_management/static/src/css/church_news_style.css',
        ],
    },
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
