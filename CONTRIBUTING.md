# 🤝 Contributing to Darash — Church Management

Thank you for your interest in contributing to this **Church Management System (ChMS)**! 🎉

Contributions of all kinds are welcome: code, bug reports, feature requests, documentation, translations, and design.

## 📌 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Getting Started](#-getting-started)
- [How to Contribute](#-how-to-contribute)
  - [Report a Bug](#-report-a-bug)
  - [Request a Feature](#-request-a-feature)
  - [Submit a Pull Request](#-submit-a-pull-request)
- [Development Setup](#-development-setup)
- [Project Structure](#-project-structure)
- [Code Style & Conventions](#-code-style--conventions)
- [Commit Guidelines](#-commit-guidelines)
- [License](#-license)

## 📜 Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful, inclusive, and constructive.

## 🚀 Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:

   ```bash
   git clone https://github.com/<your-username>/church_management.git
   cd church_management
   ```

3. Set up a development environment (see [Development Setup](#-development-setup)).
4. Create a new branch for your work:

   ```bash
   git checkout -b feat/your-feature-name
   ```

## 🛠️ How to Contribute

### 🐛 Report a Bug

If you find a bug, please [open an issue](https://github.com/prihadi-r/church_management/issues/new/choose) using the **Bug Report** template and include:

- Steps to reproduce.
- Expected vs. actual behaviour.
- Odoo version, OS, and any relevant logs.
- Screenshots if applicable.

### ✨ Request a Feature

Use the **Feature Request** template to describe:

- The problem you're trying to solve.
- The proposed solution.
- Any alternatives you've considered.

### 🧑‍💻 Submit a Pull Request

1. Make your changes in a dedicated branch.
2. Test your changes locally (install the module, restart the Odoo service, verify no errors).
3. Commit with a clear, descriptive message (see [Commit Guidelines](#-commit-guidelines)).
4. Push and open a Pull Request against the `main` branch.
5. Reference any related issue in your PR description.
6. Respond to review feedback promptly.

## 🧑‍🔧 Development Setup

This is an **Odoo 18** module, so you need a running Odoo 18 instance.

### Option A — Docker (easiest)

```bash
docker compose up -d --build
```

Then open http://localhost:8069, create a database, and install **Church Management**.

### Option B — Local Odoo

1. Install Odoo 18 and its Python dependencies.
2. Install the module's Python dependency:

   ```bash
   pip install feedparser
   ```

3. Symlink or copy this folder into your Odoo `addons` directory.
4. Update the apps list and install **Church Management**.

> **Tip:** after changing model/field code, restart the Odoo server — Odoo caches imported model code in the running process and a registry reload alone does not re-import it.

## 📂 Project Structure

```
church_management/
├── __manifest__.py        # Module metadata, dependencies, data/views list
├── models/                # Odoo model definitions (Python)
├── controllers/           # Website controllers & HTTP routes
├── views/                 # XML views, menus, website templates
├── data/                  # Sample / seed data (XML)
├── security/              # Access rules (CSV + XML)
├── static/                # Static assets (CSS, JS, images)
├── migrations/            # Version-specific migration scripts
├── scripts/               # Deployment / maintenance scripts
└── docs                  # INSTALLATION_GUIDE.md, USER_GUIDE.md
```

## 🎨 Code Style & Conventions

- **Python:** follow [PEP 8](https://peps.python.org/pep-0008/) and Odoo's [development guidelines](https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html).
- **XML:** follow Odoo XML view conventions.
- **Do not use HTML entities** like `&mdash;` in XML view files — they are invalid XML entities. Use the literal UTF-8 character (`—`) instead.
- Keep changes focused and minimal; avoid unrelated refactoring.
- Add or update tests/sample data where appropriate.

## 📝 Commit Guidelines

Use clear, imperative commit messages. Example:

```text
feat: add musician schedule reminder emails

- Add cron job to send reminders before scheduled events
- Add email template and notification settings
```

Common prefixes: `feat:`, `fix:`, `docs:`, `refactor:`, `style:`, `test:`, `chore:`.

## 📄 License

This project uses a [custom license](LICENSE): it is free to use and to distribute, but **every change must be approved by the owner**. By opening a pull request or sending a patch you agree that your contribution may be merged under that license, and that no change is considered accepted until the owner has approved it in writing.

---

Thanks again for helping make **Darash** a great, free church management system! 🙏
