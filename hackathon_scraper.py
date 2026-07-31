import requests
from bs4 import BeautifulSoup
import re

def scrape_hackathons():
    url = "https://devpost.com/hackathons?utf8=%E2%9C%93&search=Pakistan"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        print(f"Status code: {response.status_code}")
        print(f"Page title: {BeautifulSoup(response.text, 'html.parser').title.string}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    # Debug: print number of elements with class "challenge-listing"
    cards = soup.select(".challenge-listing")
    print(f"Found {len(cards)} challenge listings.")

    for card in cards:
        try:
            # Try different selectors (common patterns)
            name_elem = card.select_one(".title a") or card.select_one("h2 a")
            name = name_elem.text.strip() if name_elem else "Unknown"

            org_elem = card.select_one(".organization-name a") or card.select_one(".company a")
            organizer = org_elem.text.strip() if org_elem else "Unknown"

            # Dates: often in <time> tags
            date_elem = card.select_one(".start-date time") or card.select_one(".date time")
            hackathon_date = date_elem.text.strip() if date_elem else "TBD"

            deadline_elem = card.select_one(".deadline time") or card.select_one(".deadline-date time")
            deadline = deadline_elem.text.strip() if deadline_elem else "TBD"

            loc_elem = card.select_one(".location")
            location = loc_elem.text.strip() if loc_elem else "Online"

            fee_elem = card.select_one(".entry-fee")
            fee = fee_elem.text.strip() if fee_elem else "Free"

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