import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def scrape_hackathons():
    """
    Scrapes upcoming hackathons from Devpost filtered for Pakistan.
    Returns a list of dictionaries with keys:
    name, organizer, hackathon_date, deadline, max_members, fee, location
    """
    url = "https://devpost.com/hackathons?utf8=%E2%9C%93&search=Pakistan"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    # Each hackathon card on Devpost has class "challenge-listing"
    for card in soup.select(".challenge-listing"):
        try:
            # Name
            name_elem = card.select_one(".title a")
            name = name_elem.text.strip() if name_elem else "Unknown"

            # Organizer
            org_elem = card.select_one(".organization-name a")
            organizer = org_elem.text.strip() if org_elem else "Unknown"

            # Start date and deadline (often displayed as text like "Starts on Apr 10, 2026")
            date_elem = card.select_one(".start-date")
            hackathon_date = date_elem.text.strip() if date_elem else "TBD"

            deadline_elem = card.select_one(".deadline")
            deadline = deadline_elem.text.strip() if deadline_elem else "TBD"

            # Location
            loc_elem = card.select_one(".location")
            location = loc_elem.text.strip() if loc_elem else "Online"

            # Fee – often says "Free" or shows a price
            fee_elem = card.select_one(".entry-fee")
            fee = fee_elem.text.strip() if fee_elem else "Free"

            # Max team members – not always shown; default to "4"
            max_members = "4"

            events.append({
                "name": name,
                "organizer": organizer,
                "hackathon_date": hackathon_date,
                "deadline": deadline,
                "max_members": max_members,
                "fee": fee,
                "location": location
            })
        except Exception as e:
            print(f"Skipping one card: {e}")
            continue

    return events

# For quick testing
if __name__ == "__main__":
    data = scrape_hackathons()
    print(f"Found {len(data)} hackathons.")
    for item in data[:3]:
        print(item)