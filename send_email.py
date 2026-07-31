import smtplib
from email.mime.text import MIMEText
import os

def send_email(events, to_email="mrx18751@gmail.com"):
    """
    Sends a plain-text email with the hackathon list.
    Requires environment variables:
      GMAIL_USER – your Gmail address
      GMAIL_APP_PASSWORD – an App Password (not your regular password)
    """
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_password:
        print("❌ Missing Gmail credentials in environment.")
        return

    subject = "📅 Pakistan Hackathons Update"
    body = "Here are the latest hackathons in Pakistan:\n\n"
    if not events:
        body += "No hackathons found at this time."
    else:
        for e in events:
            body += (f"• {e['name']} | {e['organizer']} | "
                     f"Date: {e['hackathon_date']} | "
                     f"Deadline: {e['deadline']} | "
                     f"Team: {e['max_members']} | "
                     f"Fee: {e['fee']} | {e['location']}\n")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, [to_email], msg.as_string())
        print("📧 Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")