# Hackathon Tracker – Pakistan

Automatically scrapes upcoming hackathons in Pakistan, updates a Google Sheet, and emails the list daily – all for free.

## How it works
- Python script scrapes Devpost for hackathons tagged with "Pakistan".
- Data is sent to a Google Apps Script Web App that writes to a Google Sheet.
- An email is sent via Gmail SMTP to the configured address.
- GitHub Actions runs the script daily on a schedule.

## Setup
1. Create a Google Sheet and deploy an Apps Script Web App with the provided `doPost` function.
2. Set the environment variables (`GMAIL_USER`, `GMAIL_APP_PASSWORD`, `WEB_APP_URL`, `WEB_APP_TOKEN`).
3. Push to GitHub and add the secrets in the repository settings.

## Files
- `hackathon_scraper.py` – scrapes data
- `update_sheet.py` – sends to Google Sheet
- `send_email.py` – sends email
- `main.py` – orchestrator
- `.github/workflows/daily_update.yml` – automation schedule