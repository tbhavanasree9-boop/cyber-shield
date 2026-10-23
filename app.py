import streamlit as st
import re
import random
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be the very first command)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CyberSec Analyzer",
    page_icon="🔐",
    layout="centered",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS  –  dark dashboard theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* Overall dark background */
[data-testid="stAppViewContainer"] {
    background-color: #0d1117;
    color: #c9d1d9;
}
[data-testid="stHeader"] { background-color: #0d1117; }
[data-testid="stSidebar"] { background-color: #161b22; }

/* Card / panel style */
.card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 18px 22px;
    margin-bottom: 16px;
}

/* Big title */
.hero-title {
    font-size: 2rem;
    font-weight: 700;
    color: #58a6ff;
    margin-bottom: 4px;
}
.hero-sub {
    color: #8b949e;
    font-size: 0.95rem;
    margin-bottom: 24px;
}

/* Strength badge colours */
.badge-weak   { color: #f85149; font-weight: 700; }
.badge-fair   { color: #e3b341; font-weight: 700; }
.badge-good   { color: #58a6ff; font-weight: 700; }
.badge-strong { color: #3fb950; font-weight: 700; }

/* Metric numbers */
.metric-num { font-size: 1.6rem; font-weight: 700; color: #58a6ff; }
.metric-lbl { font-size: 0.8rem; color: #8b949e; }

/* Login bar labels */
.login-label { font-size: 0.85rem; color: #8b949e; margin-bottom: 2px; }

/* Divider */
hr { border-color: #30363d; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def check_strength(password: str) -> dict:
    """
    Returns a dict with:
      score   : 0-4
      label   : Weak / Fair / Good / Strong
      checks  : list of (description, passed) tuples
    """
    checks = [
        ("At least 8 characters",          len(password) >= 8),
        ("At least 12 characters",         len(password) >= 12),
        ("Contains uppercase letter (A-Z)", bool(re.search(r"[A-Z]", password))),
        ("Contains lowercase letter (a-z)", bool(re.search(r"[a-z]", password))),
        ("Contains a number (0-9)",         bool(re.search(r"\d",    password))),
        ("Contains a special character",    bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))),
    ]
    score = sum(passed for _, passed in checks)

    if score <= 2:
        label = "Weak"
    elif score == 3:
        label = "Fair"
    elif score in (4, 5):
        label = "Good"
    else:
        label = "Strong"

    return {"score": score, "max": len(checks), "label": label, "checks": checks}


def simulate_login_stats(genuine_base: int = 320, fake_base: int = 47) -> dict:
    """
    Simulates a small random fluctuation around base values so the
    dashboard feels live each time the page refreshes.
    """
    genuine = genuine_base + random.randint(-10, 10)
    fake    = fake_base    + random.randint(-5,  5)
    total   = genuine + fake
    return {"genuine": genuine, "fake": fake, "total": total}


def generate_scan_history(n: int = 30) -> list:
    """
    Generates n fake password scan history entries.
    Each entry has: timestamp, masked password, strength label, status (genuine/fake).
    """
    random.seed(42)          # fixed seed → same list every load
    sample_passwords = [
        "abc123", "P@ssw0rd!", "hello", "Qx9#mL2!vT", "iloveyou",
        "Admin2024!", "123456", "Tr0ub4dor&3", "qwerty", "C0mpl3x#Key",
        "password", "S3cur3P@ss!", "letmein", "Dragon$7Fire", "monkey",
        "7Hg!xQ2@Lp", "sunshine", "N0tEasy#99", "football", "Zk#8mW!2qR",
        "shadow", "Br1ght!Star9", "master", "xK3$pL9!vM", "welcome",
        "Vy7!mN3@qZ", "michael", "J8#rT2!kWs", "superman", "Gp5@Xn1!zL",
    ]
    strengths = ["Weak", "Fair", "Good", "Strong"]
    history = []
    base_time = datetime(2025, 10, 23, 9, 0, 0)
    for i, pwd in enumerate(sample_passwords[:n]):
        result = check_strength(pwd)
        label  = result["label"]
        # Fake logins tend to be weak/fair; genuine ones spread across all
        if label in ("Weak", "Fair") and random.random() < 0.75:
            status = "Fake"
        else:
            status = "Genuine"
        timestamp = base_time + timedelta(minutes=i * 4 + random.randint(0, 3))
        masked    = pwd[0] + "*" * (len(pwd) - 2) + pwd[-1] if len(pwd) > 2 else "***"
        history.append({
            "time":     timestamp.strftime("%H:%M:%S"),
            "password": masked,
            "strength": label,
            "status":   status,
        })
    random.seed()            # restore true randomness for the rest of the app
    return history


# ─────────────────────────────────────────────
#  SESSION STATE  – stable until page re-run
# ─────────────────────────────────────────────
if "login_stats" not in st.session_state:
    st.session_state.login_stats = simulate_login_stats()

if "scan_history" not in st.session_state:
    st.session_state.scan_history = generate_scan_history(30)

stats = st.session_state.login_stats


# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-title">🔐 CyberSec Password Analyzer</div>
<div class="hero-sub">
    A security dashboard to test password strength and monitor login activity.
    Enter a password below to get an instant security report.
</div>
<hr/>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  LOGIN ACTIVITY BAR  (top of dashboard)
# ─────────────────────────────────────────────
st.markdown("### 📊 Login Activity Monitor")
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-num">{stats["total"]}</div>'
                f'<div class="metric-lbl">Total Logins</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-num" style="color:#3fb950">{stats["genuine"]}</div>'
                f'<div class="metric-lbl">✅ Genuine Logins</div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-num" style="color:#f85149">{stats["fake"]}</div>'
                f'<div class="metric-lbl">🚨 Fake / Suspicious</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Progress bars for genuine vs fake
genuine_pct = stats["genuine"] / stats["total"]
fake_pct    = stats["fake"]    / stats["total"]

st.markdown('<p class="login-label">✅ Genuine logins</p>', unsafe_allow_html=True)
st.progress(genuine_pct)

st.markdown('<p class="login-label">🚨 Fake / suspicious logins</p>', unsafe_allow_html=True)
st.progress(fake_pct)

st.caption(
    f"Genuine: {genuine_pct*100:.1f}%  |  Fake: {fake_pct*100:.1f}%  — "
    "Refresh the page to simulate new data."
)

st.markdown("<hr/>", unsafe_allow_html=True)

# Button to refresh login stats
if st.button("🔄 Refresh Login Data"):
    st.session_state.login_stats = simulate_login_stats()
    st.rerun()


# ─────────────────────────────────────────────
#  PASSWORD STRENGTH ANALYZER
# ─────────────────────────────────────────────
st.markdown("### 🛡️ Password Strength Analyzer")

password = st.text_input(
    "Enter a password to analyze:",
    type="password",
    placeholder="Type your password here…",
)

if password:
    result = check_strength(password)
    score  = result["score"]
    label  = result["label"]

    # Colour map
    colour_map = {
        "Weak":   ("#f85149", "badge-weak"),
        "Fair":   ("#e3b341", "badge-fair"),
        "Good":   ("#58a6ff", "badge-good"),
        "Strong": ("#3fb950", "badge-strong"),
    }
    bar_colour, badge_class = colour_map[label]

    # Score bar (use native progress so it respects the theme)
    st.markdown(
        f'Strength: <span class="{badge_class}">{label}</span> '
        f'({score}/{result["max"]} checks passed)',
        unsafe_allow_html=True,
    )
    st.progress(score / result["max"])

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Security checklist:**")
    for description, passed in result["checks"]:
        icon = "✅" if passed else "❌"
        st.markdown(f"{icon} {description}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Tips
    if label in ("Weak", "Fair"):
        st.warning(
            "💡 **Tips to improve your password:**\n"
            "- Use **12+ characters**\n"
            "- Mix **UPPER and lower** case letters\n"
            "- Add **numbers** and **special characters** like `!@#$%`\n"
            "- Avoid common words or names"
        )
    else:
        st.success("✅ Great password! Make sure you never reuse it on other sites.")

else:
    st.info("👆 Type a password above to see your security score.")


# ─────────────────────────────────────────────
#  SCAN HISTORY TABLE  – 30 password logins
# ─────────────────────────────────────────────
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown("### 🕵️ Password Login Scan History (Last 30 Logins)")

# Colour coding helpers
def status_badge(status: str) -> str:
    if status == "Genuine":
        return '<span style="color:#3fb950;font-weight:700;">✅ Genuine</span>'
    return '<span style="color:#f85149;font-weight:700;">🚨 Fake</span>'

def strength_badge(label: str) -> str:
    colours = {"Weak": "#f85149", "Fair": "#e3b341", "Good": "#58a6ff", "Strong": "#3fb950"}
    return f'<span style="color:{colours.get(label,"#c9d1d9")};font-weight:600;">{label}</span>'

# Build HTML table rows
rows_html = ""
for entry in st.session_state.scan_history:
    rows_html += (
        f"<tr>"
        f"<td style='padding:6px 10px;color:#8b949e;'>{entry['time']}</td>"
        f"<td style='padding:6px 10px;font-family:monospace;color:#c9d1d9;'>{entry['password']}</td>"
        f"<td style='padding:6px 10px;'>{strength_badge(entry['strength'])}</td>"
        f"<td style='padding:6px 10px;'>{status_badge(entry['status'])}</td>"
        f"</tr>"
    )

table_html = f"""
<div class="card" style="overflow-x:auto;">
<table style="width:100%;border-collapse:collapse;">
  <thead>
    <tr style="border-bottom:1px solid #30363d;">
      <th style="padding:8px 10px;text-align:left;color:#58a6ff;font-size:0.85rem;">Time</th>
      <th style="padding:8px 10px;text-align:left;color:#58a6ff;font-size:0.85rem;">Password (masked)</th>
      <th style="padding:8px 10px;text-align:left;color:#58a6ff;font-size:0.85rem;">Strength</th>
      <th style="padding:8px 10px;text-align:left;color:#58a6ff;font-size:0.85rem;">Status</th>
    </tr>
  </thead>
  <tbody>
    {rows_html}
  </tbody>
</table>
</div>
"""
st.markdown(table_html, unsafe_allow_html=True)

# Quick summary counts for the history
genuine_count = sum(1 for e in st.session_state.scan_history if e["status"] == "Genuine")
fake_count    = len(st.session_state.scan_history) - genuine_count
st.caption(f"History summary — ✅ Genuine: {genuine_count}  |  🚨 Fake: {fake_count}  |  Total: {len(st.session_state.scan_history)}")


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center; color:#8b949e; font-size:0.8rem;">'
    "🔐 CyberSec Analyzer — for educational purposes only. "
    "Never enter real passwords into unknown tools."
    "</p>",
    unsafe_allow_html=True,
)
