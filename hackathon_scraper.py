import requests
from bs4 import BeautifulSoup
import re

def scrape_hackathons():
    url = "https://devpost.com/hackathons?utf8=%E2%9C%93&search=Pakistan"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        print(f"✅ Status code: {response.status_code}")
        print(f"📄 Page title: {BeautifulSoup(response.text, 'html.parser').title.string}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    # ----- DEBUG: Find all possible card containers -----
    # Try several common classes used by Devpost
    possible_selectors = [
        ".challenge-listing",      # old
        ".hackathon-card",         # new?
        ".challenge-card", 
        ".card",
        "article",
        ".hackathon-item",
        ".listing-card"
    ]
    
    for selector in possible_selectors:
        cards = soup.select(selector)
        if cards:
            print(f"✅ Found {len(cards)} elements with selector: {selector}")
            break
    else:
        # If none match, show first few divs for manual inspection
        print("⚠️ No known selectors matched. Showing first 5 divs with class attributes:")
        for i, div in enumerate(soup.find_all("div", class_=True)[:5]):
            classes = " ".join(div.get("class", []))
            print(f"  {i+1}. <div class='{classes}'> ... </div>")
        # Also show all divs with 'hackathon' in class
        print("\n🔎 Divs with 'hackathon' in class:")
        for div in soup.find_all("div", class_=True):
            classes = " ".join(div.get("class", []))
            if "hackathon" in classes.lower():
                print(f"  <div class='{classes}'>")
        return []

    # Use the first selector that matched
    card_selector = selector
    cards = soup.select(card_selector)
    print(f"Processing {len(cards)} cards...")

    for card in cards:
        try:
            # Name
            name_elem = card.select_one(".title a") or card.select_one("h2 a") or card.select_one("a[class*='title']")
            name = name_elem.text.strip() if name_elem else "Unknown"
            
            # Organizer
            org_elem = card.select_one(".organization-name a") or card.select_one(".company a") or card.select_one(".host a")
            organizer = org_elem.text.strip() if org_elem else "Unknown"

            # Dates (look for any element containing 'date' in class)
            date_elem = card.select_one(".start-date time") or card.select_one(".date time") or card.select_one("[class*='date'] time")
            hackathon_date = date_elem.text.strip() if date_elem else "TBD"

            deadline_elem = card.select_one(".deadline time") or card.select_one(".deadline-date time") or card.select_one("[class*='deadline'] time")
            deadline = deadline_elem.text.strip() if deadline_elem else "TBD"

            # Location
            loc_elem = card.select_one(".location") or card.select_one("[class*='location']")
            location = loc_elem.text.strip() if loc_elem else "Online"

            # Fee
            fee_elem = card.select_one(".entry-fee") or card.select_one("[class*='fee']") or card.select_one("[class*='prize']")
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
            print(f"Skipping a card: {e}")
            continue

    print(f"✅ Extracted {len(events)} hackathons.")
    return events