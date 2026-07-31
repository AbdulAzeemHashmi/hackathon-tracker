from hackathon_scraper import scrape_hackathons
from update_sheet import update_google_sheet
from send_email import send_email

def main():
    print("🔍 Scraping hackathons...")
    events = scrape_hackathons()
    print(f"Found {len(events)} events.")

    if not events:
        print("No events to process. Still sending email with empty list.")
        # Optionally still send an email to inform that none were found.
        send_email(events)
        return

    # Update Google Sheet
    update_google_sheet(events)

    # Send email
    send_email(events)

if __name__ == "__main__":
    main()