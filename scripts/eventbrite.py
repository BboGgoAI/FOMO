import json
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Sample JSON data
data = {"name": "John", "age": 30, "city": "New York"}

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def pretty_print(data):
    # Convert the data to a JSON formatted string with 4 spaces of indentation
    json_str = json.dumps(data, indent=4)
    # Print the pretty-printed JSON string
    print(json_str)


BASE_URL = "https://www.eventbrite.com/d/ca--san-francisco/all-events/?page="


def scrape_eventbrite_page(url):
    print(f"Scraping {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to load page: {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")
    events = []
    results = soup.find("div", class_="search-results-panel-content__events").find("section")
    if results is None:
        return events

    cards = results.find_all("li")
    for card in cards:
        event_details = card.find("section", class_="event-card-details").find("div")
        link = event_details.find("a", recursive=False).get("href")
        title = event_details.find("h3").get_text()
        details = event_details.find_all("p", recursive=False)
        date = ""
        location_brief = ""
        if len(details) == 2:
            date = details[0].get_text()
            location_brief = details[1].get_text()
        else:
            location_brief = details[0].get_text()

        # Fetch detailed address and geolocation
        full_address, latitude, longitude = fetch_event_details(link)

        events.append(
            {
                "Title": title,
                "Date": date,
                "Link": link,
                "LocationBrief": location_brief,
                "FullAddress": full_address,
                "Latitude": latitude,
                "Longitude": longitude,
            }
        )
    return events


# Function to upload events to Supabase
def upload_to_supabase(events):
    for event in events:
        data = {
            "name": event["Title"],
            "date": event["Date"],
            "url": event["Link"],
            "location_brief": event["LocationBrief"],
            "full_address": event["FullAddress"],
            "latitude": event["Latitude"],
            "longitude": event["Longitude"],
        }

        response = supabase.table("events").insert(data).execute()

        if response.data:
            print(f"Uploaded: {event['Title']}")
        elif response.error:
            print(f"Failed to upload: {event['Title']} - {response.error.message}")



def fetch_event_details(event_url):
    print(f"Fetching details for event: {event_url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    response = requests.get(event_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to load event details page: {response.status_code}")
        return None, None, None

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the full address
    address_div = soup.find("div", class_="location-info__address")
    if address_div:
        address_text = address_div.get_text(strip=True)
    else:
        address_text = None
        print("Address not found on event page.")

    # Extract latitude and longitude from meta tags
    latitude_meta = soup.find("meta", {"property": "event:location:latitude"})
    longitude_meta = soup.find("meta", {"property": "event:location:longitude"})

    latitude = float(latitude_meta["content"]) if latitude_meta else None
    longitude = float(longitude_meta["content"]) if longitude_meta else None

    return address_text, latitude, longitude

# Main function to scrape and upload all events
def scrape_and_upload():
    events = []
    i = 1  # Start pagination at 1
    while True:
        events_from_page = scrape_eventbrite_page(BASE_URL + str(i))
        if not events_from_page:
            break
        events.extend(events_from_page)
        i += 1

    # pretty_print(events)
    upload_to_supabase(events)
    print(f"Uploaded {len(events)} events to Supabase.")

# Run the script
if __name__ == "__main__":
    scrape_and_upload()