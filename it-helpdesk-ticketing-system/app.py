import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "helpdesk.db"

st.set_page_config(
    page_title="HelpDesk Lite | IT Support",
    page_icon="🎫",
    layout="wide",
)
st.markdown("""
<style>
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #cbd9eb !important;
    border-radius: 14px !important;
    padding: 22px !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #334b68 !important;
    font-size: 16px !important;
    font-weight: 700 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #12345a !important;
    font-size: 32px !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    color: #167347 !important;
}
</style>
""", unsafe_allow_html=True)


STATUSES = ["Open", "In Progress", "Escalated", "Resolved", "Closed"]
PRIORITIES = ["Critical", "High", "Medium", "Low"]
CATEGORIES = [
    "Account / Password",
    "Network / Wi-Fi",
    "Hardware",
    "Software",
    "Email",
    "Printer",
    "Access / Permissions",
    "Other",
]

SAMPLE_TICKETS = [
    ("HD-1001", "Aarav Sharma", "Cannot connect to office Wi-Fi", "Network / Wi-Fi", "High", "Open", "Unable to access the internet from laptop.", "Check Wi-Fi status, confirm airplane mode is off, reconnect to the approved network, then run ipconfig and test the default gateway."),
    ("HD-1002", "Diya Verma", "Password reset request", "Account / Password", "Medium", "In Progress", "User cannot sign in after forgetting password.", "Verify the requester's identity using the organization's approved process. Follow the authorized password-reset workflow; never ask for or record the user's password."),
    ("HD-1003", "Kabir Singh", "Printer is not responding", "Printer", "Low", "Resolved", "Print jobs remain queued.", "Confirm printer power and network connection, check the selected printer, clear stuck jobs if authorized, and print a test page."),
    ("HD-1004", "Meera Gupta", "Application crashes on launch", "Software", "High", "Escalated", "Business application closes immediately after opening.", "Record the exact error and time, restart the application, check for approved updates, and escalate with logs if the issue persists."),
    ("HD-1005", "Ishaan Patel", "Request access to shared folder", "Access / Permissions", "Medium", "Closed", "User receives access denied message.", "Confirm business approval and folder path. Validate group membership with the authorized administrator; apply least-privilege access."),
]


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_no TEXT UNIQUE,
                requester TEXT NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                description TEXT NOT NULL,
                troubleshooting TEXT DEFAULT '',
                resolution TEXT DEFAULT '',
                assigned_to TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        if count == 0:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            for item in SAMPLE_TICKETS:
                ticket_no, requester, title, category, priority, status, description, troubleshooting = item
                conn.execute("""
                    INSERT INTO tickets
                    (ticket_no, requester, title, category, priority, status,
                     description, troubleshooting, resolution, assigned_to, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, '', 'L1 Support', ?, ?)
                """, (ticket_no, requester, title, category, priority, status,
                      description, troubleshooting, now, now))


def load_tickets():
    with get_connection() as conn:
        return pd.read_sql_query("SELECT * FROM tickets ORDER BY id DESC", conn)


def add_ticket(requester, title, category, priority, description):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with get_connection() as conn:
        next_id = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM tickets").fetchone()[0]
        ticket_no = f"HD-{1000 + next_id}"
        conn.execute("""
            INSERT INTO tickets
            (ticket_no, requester, title, category, priority, status, description,
             troubleshooting, resolution, assigned_to, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'Open', ?, '', '', 'Unassigned', ?, ?)
        """, (ticket_no, requester.strip(), title.strip(), category, priority,
              description.strip(), now, now))
    return ticket_no


def update_ticket(ticket_id, status, priority, assigned_to, troubleshooting, resolution):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with get_connection() as conn:
        conn.execute("""
            UPDATE tickets
            SET status = ?, priority = ?, assigned_to = ?, troubleshooting = ?,
                resolution = ?, updated_at = ?
            WHERE id = ?
        """, (status, priority, assigned_to.strip(), troubleshooting.strip(),
              resolution.strip(), now, int(ticket_id)))


init_db()

st.title("🎫 HelpDesk Lite")
st.caption("IT Help Desk Ticketing & Troubleshooting System | Portfolio demo with fictional data")
st.info("Demo only: do not enter real personal data, passwords, confidential company information, or production incidents.")

tickets = load_tickets()

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Choose a view", ["Dashboard", "All Tickets", "Create Ticket", "Troubleshooting KB"])
    st.divider()
    st.caption("Built with Python · Streamlit · SQLite")
    st.caption("Sample records are fictional.")

if page == "Dashboard":
    st.markdown("## 📊 Support Overview")
    st.caption("Monitor ticket volume, priorities, and resolution progress at a glance.")

    tickets = load_tickets()
    total = len(tickets)
    open_count = int(tickets["status"].isin(["Open", "In Progress", "Escalated"]).sum())
    resolved_count = int(tickets["status"].isin(["Resolved", "Closed"]).sum())
    critical_count = int((tickets["priority"] == "Critical").sum())

    st.markdown("### 📈 Ticket Summary")
    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        st.metric("🎫 Total Tickets", total)
    with c2:
        st.metric("🟠 Active Tickets", open_count)
    with c3:
        st.metric("✅ Resolved / Closed", resolved_count)
    with c4:
        st.metric("🔴 Critical Priority", critical_count)

    st.metric("🔴 Critical Priority", critical_count)


    left, right = st.columns(2)
    with left:
        st.markdown("#### Tickets by status")
        if total:
            status_counts = tickets["status"].value_counts().rename_axis("Status").reset_index(name="Tickets")
            st.bar_chart(status_counts.set_index("Status"))
        else:
            st.write("No tickets yet.")
    with right:
        st.markdown("#### Tickets by priority")
        if total:
            priority_order = [p for p in PRIORITIES if p in tickets["priority"].unique()]
            priority_counts = tickets["priority"].value_counts().reindex(priority_order, fill_value=0)
            st.bar_chart(priority_counts)
        else:
            st.write("No tickets yet.")

    st.markdown("#### Recently updated")
    if total:
        display_cols = ["ticket_no", "title", "requester", "category", "priority", "status", "updated_at"]
        st.dataframe(tickets[display_cols], use_container_width=True, hide_index=True)
    else:
        st.success("No tickets available. Create your first ticket.")

elif page == "All Tickets":
    st.subheader("Ticket queue")
    tickets = load_tickets()
    f1, f2, f3 = st.columns(3)
    with f1:
        status_filter = st.multiselect("Filter by status", STATUSES, default=[])
    with f2:
        priority_filter = st.multiselect("Filter by priority", PRIORITIES, default=[])
    with f3:
        search_text = st.text_input("Search tickets", placeholder="Ticket number, title, requester...")

    filtered = tickets.copy()
    if status_filter:
        filtered = filtered[filtered["status"].isin(status_filter)]
    if priority_filter:
        filtered = filtered[filtered["priority"].isin(priority_filter)]
    if search_text:
        mask = (
            filtered["ticket_no"].str.contains(search_text, case=False, na=False)
            | filtered["title"].str.contains(search_text, case=False, na=False)
            | filtered["requester"].str.contains(search_text, case=False, na=False)
        )
        filtered = filtered[mask]

    cols = ["ticket_no", "title", "requester", "category", "priority", "status", "assigned_to", "created_at", "updated_at"]
    st.dataframe(filtered[cols], use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(filtered)} of {len(tickets)} tickets.")

    if not tickets.empty:
        st.markdown("#### Update a ticket")
        ticket_options = {
            f"{row['ticket_no']} — {row['title']}": int(row["id"])
            for _, row in tickets.iterrows()
        }
        selected_label = st.selectbox("Select ticket", list(ticket_options.keys()))
        selected_id = ticket_options[selected_label]
        selected = tickets[tickets["id"] == selected_id].iloc[0]

        with st.form("update_ticket_form"):
            a, b = st.columns(2)
            with a:
                new_status = st.selectbox("Status", STATUSES, index=STATUSES.index(selected["status"]))
                new_priority = st.selectbox("Priority", PRIORITIES, index=PRIORITIES.index(selected["priority"]))
                assigned_to = st.text_input("Assigned to", value=selected["assigned_to"] or "")
            with b:
                troubleshooting = st.text_area("Troubleshooting notes", value=selected["troubleshooting"] or "", height=100)
                resolution = st.text_area("Resolution / next action", value=selected["resolution"] or "", height=100)
            submitted = st.form_submit_button("Save ticket update", type="primary")
            if submitted:
                update_ticket(selected_id, new_status, new_priority, assigned_to, troubleshooting, resolution)
                st.success(f"{selected['ticket_no']} updated.")
                st.rerun()

    if not filtered.empty:
        csv = filtered[cols].to_csv(index=False).encode("utf-8")
        st.download_button("Download filtered tickets as CSV", csv, "helpdesk_tickets.csv", "text/csv")

elif page == "Create Ticket":
    st.subheader("Log a new incident or service request")
    with st.form("create_ticket_form", clear_on_submit=True):
        requester = st.text_input("Requester name", placeholder="e.g., Alex Kumar")
        title = st.text_input("Short description", placeholder="e.g., Laptop cannot connect to Wi-Fi")
        a, b = st.columns(2)
        with a:
            category = st.selectbox("Category", CATEGORIES)
        with b:
            priority = st.selectbox("Priority", PRIORITIES, index=2)
        description = st.text_area("Issue details", placeholder="Describe the symptoms, error message, and when it started.", height=120)
        submitted = st.form_submit_button("Create ticket", type="primary")
        if submitted:
            if not requester.strip() or not title.strip() or not description.strip():
                st.error("Please complete requester, short description, and issue details.")
            else:
                ticket_no = add_ticket(requester, title, category, priority, description)
                st.success(f"Ticket {ticket_no} created successfully.")
                st.caption("The ticket starts with Open status and Unassigned ownership.")

elif page == "Troubleshooting KB":
    st.subheader("Troubleshooting knowledge base")
    st.write("Use this checklist as a starting point. Follow your organization's approved procedures and permissions.")
    kb = [
        ("Wi-Fi / network connectivity", [
            "Confirm Wi-Fi is enabled and airplane mode is off.",
            "Check whether other approved websites or services are reachable.",
            "Run ipconfig to inspect IP address, gateway, and DNS configuration.",
            "Test connectivity to the default gateway with ping where permitted.",
            "Use nslookup to investigate DNS resolution issues.",
            "Record results and escalate with timestamps and error messages if unresolved.",
        ]),
        ("Password / account sign-in", [
            "Confirm the exact error and whether the issue affects one or multiple services.",
            "Verify user identity using the organization's approved process.",
            "Check account lockout or password-expiry status only if authorized.",
            "Never ask the user to disclose their password or store it in a ticket.",
            "Use the approved reset process and confirm sign-in works.",
        ]),
        ("Printer issue", [
            "Check printer power, paper, toner, and displayed errors.",
            "Confirm the correct printer is selected.",
            "Check connectivity and whether other users are affected.",
            "Inspect the print queue and clear stuck jobs only when authorized.",
            "Print a test page and document the outcome.",
        ]),
        ("Application crash", [
            "Record application name, device, time, and exact error message.",
            "Check whether the issue is reproducible and affects other users.",
            "Restart the app or device only after saving work and following policy.",
            "Check approved updates and capture relevant logs if permitted.",
            "Escalate with impact, steps tried, and evidence.",
        ]),
        ("Access denied", [
            "Confirm the exact resource and the business reason for access.",
            "Check whether access approval has been granted.",
            "Validate permissions or group membership only with authorization.",
            "Apply least privilege; do not grant broad access to bypass the issue.",
            "Record approval, changes, validation, and closure notes.",
        ]),
    ]
    for heading, steps in kb:
        with st.expander(heading):
            for step in steps:
                st.markdown(f"- {step}")

st.divider()
st.caption("Portfolio project for learning and demonstration. Not intended for production use without authentication, access controls, backups, and security review.")
