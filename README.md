# 🔐 CyberSec Password Strength & Security Analyzer

A beginner-friendly cybersecurity dashboard built with **Python** and **Streamlit**. It simulates a real-world security monitoring tool with password strength analysis, login activity monitoring, and a 30-entry scan history table — all in a clean, modern dark theme.

---

## 📸 Features

- **🛡️ Password Strength Analyzer** — Real-time scoring with 6 security checks and colour-coded feedback (Weak / Fair / Good / Strong)
- **📊 Login Activity Monitor** — Metric cards and progress bars showing genuine vs. fake/suspicious logins
- **🕵️ Scan History Table** — Last 30 password login attempts with timestamps, masked passwords, strength labels, and Genuine/Fake classification
- **🔄 Refresh Button** — Simulates new incoming login data on demand
- **🌑 Dark Dashboard Theme** — Custom CSS for a professional security-tool look

---

## 🗂️ Project Structure

```
cybersec-analyzer/
│
├── app.py              ← Single-file Streamlit application (all code here)
├── README.md           ← This file
└── project_report.docx ← Full project report in Word format
```

---

## ⚙️ Requirements

| Requirement | Detail |
|---|---|
| Python | 3.8 or higher |
| Streamlit | `pip install streamlit` |
| re | Built-in (no install needed) |
| random | Built-in (no install needed) |
| datetime | Built-in (no install needed) |

---

## 🚀 Getting Started

### 1. Clone or Download the Project

```bash
git clone https://github.com/your-username/cybersec-analyzer.git
cd cybersec-analyzer
```

Or simply download `app.py` and place it in a folder.

### 2. Install Streamlit

```bash
pip install streamlit
```

> If `pip` is not recognised, use `python -m pip install streamlit` instead.

### 3. Run the App

```bash
streamlit run app.py
```

The app will open automatically in your default browser at:

```
http://localhost:8501
```

---

## 🔍 How It Works

### Password Strength Checker

The [`check_strength()`](app.py) function runs **6 binary checks** on the entered password:

| # | Check | Points |
|---|---|---|
| 1 | At least 8 characters | +1 |
| 2 | At least 12 characters | +1 |
| 3 | Contains uppercase letter (A–Z) | +1 |
| 4 | Contains lowercase letter (a–z) | +1 |
| 5 | Contains a number (0–9) | +1 |
| 6 | Contains a special character (`!@#$%^&*`) | +1 |

**Score → Label mapping:**

| Score | Label | Colour |
|---|---|---|
| 0–2 | Weak | 🔴 Red |
| 3 | Fair | 🟡 Yellow |
| 4–5 | Good | 🔵 Blue |
| 6 | Strong | 🟢 Green |

### Login Activity Monitor

The [`simulate_login_stats()`](app.py) function generates randomised login counts around realistic base values:
- **~320** genuine logins
- **~47** fake / suspicious logins

Values fluctuate slightly on each refresh to simulate live data.

### Scan History

The [`generate_scan_history()`](app.py) function produces 30 pre-seeded login records. Each record contains:

- **Time** — Simulated timestamp (HH:MM:SS)
- **Password (masked)** — First and last character visible; rest replaced with `***`
- **Strength** — Weak / Fair / Good / Strong
- **Status** — ✅ Genuine or 🚨 Fake

> Fake logins are those where the password scored Weak or Fair, as a genuine user is unlikely to choose such a simple password.

---

## 🧠 Code Overview (`app.py`)

```
app.py
├── Page config            ← st.set_page_config()
├── Custom CSS             ← Dark theme via st.markdown()
├── check_strength()       ← 6-rule password evaluator
├── simulate_login_stats() ← Random login telemetry
├── generate_scan_history()← 30 login history entries
├── Session state          ← Stable data across re-runs
├── Header section         ← Title + description
├── Login Activity bar     ← Metrics + progress bars + refresh
├── Password Analyzer      ← Text input + checklist + tips
├── Scan History table     ← HTML table with colour coding
└── Footer
```

---

## 💡 Tips for Beginners

- All code is in **one file** — open `app.py` and read top to bottom.
- Every section is clearly **commented** so you know what each part does.
- Try changing the `genuine_base` and `fake_base` values in `simulate_login_stats()` to see different numbers on the dashboard.
- Add your own passwords to `sample_passwords` inside `generate_scan_history()` to customise the scan history.

---

## ⚠️ Disclaimer

> This application is built **for educational purposes only**.  
> Never enter real passwords into any unknown tool or website.  
> All login data shown is entirely simulated and does not represent real users.

---

## 📄 License

This project is open-source and free to use for learning and educational purposes.

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io) — for making Python web apps incredibly simple
- [OWASP](https://owasp.org) — password security guidelines
- [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html) — digital identity standards
