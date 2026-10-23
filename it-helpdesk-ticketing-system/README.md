# HelpDesk Lite — IT Help Desk Ticketing & Troubleshooting System

A beginner-friendly portfolio project that simulates a Level 1 IT support workflow using Python, Streamlit, and SQLite.

## Features

- Dashboard showing total, active, resolved/closed, and critical tickets
- Create, search, filter, and update support tickets
- Track priority, status, assignee, troubleshooting notes, and resolution
- Download filtered tickets as CSV
- Troubleshooting knowledge base for Wi-Fi, accounts, printers, applications, and access issues
- Fictional sample tickets for demonstration

## Tech stack

- Python
- Streamlit
- SQLite
- Pandas
- Git and GitHub

## Run locally (Windows)

1. Install Python 3.10 or newer from https://www.python.org/downloads/ and enable **Add Python to PATH** during installation.
2. Install Git from https://git-scm.com/downloads.
3. Download or clone this repository and open a terminal in the project folder.
4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run:

   ```bat
   .venv\Scripts\activate.bat
   ```

5. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Start the app:

   ```powershell
   python -m streamlit run app.py
   ```

7. Open the local URL shown in the terminal, usually http://localhost:8501.

## Publish to GitHub

Create an empty public repository named `it-helpdesk-ticketing-system` on GitHub. Do not initialize it with a README if you already have this project's README locally. In the project folder, run:

```powershell
git init
git add .
git commit -m "Build HelpDesk Lite ticketing system"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/it-helpdesk-ticketing-system.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. GitHub may ask you to sign in using a browser or credential manager. Never put a password or access token in the repository.

## Deploy the live demo

1. Push this repository to GitHub.
2. Open https://share.streamlit.io/ and sign in with GitHub.
3. Select **Create app**.
4. Choose this repository, branch `main`, and main file path `app.py`.
5. Deploy and wait for the build to finish.
6. Copy the generated `*.streamlit.app` URL into your resume and GitHub README.

Official guide: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## Suggested test cases

- Create a ticket with all required fields; confirm it appears in the ticket queue.
- Submit a ticket with a required field blank; confirm validation appears.
- Filter by status and priority.
- Search by ticket number, requester, or title.
- Change a ticket's status and add troubleshooting notes.
- Download the filtered ticket list as CSV.
- Open each troubleshooting knowledge-base section.

## Resume wording (use after you build and test it)

**HelpDesk Lite — IT Help Desk Ticketing & Troubleshooting System**
- Built a Python-based help desk application to log, prioritize, search, and track incident tickets using Streamlit and SQLite.
- Implemented ticket status updates, assignment fields, troubleshooting/resolution notes, dashboard metrics, and CSV export.
- Documented common L1 troubleshooting workflows for network connectivity, account access, printers, and application issues.

## Important limitations

- This is a learning/demo app, not a production service desk.
- It has no user authentication or role-based access control.
- SQLite is local to the running environment. On hosted platforms, local files may not be durable across all restarts/redeployments, so use fictional demo data only.
- Do not enter real names, passwords, confidential data, or real company tickets.
- Sample tickets are fictional and are inserted when the database is first created.
