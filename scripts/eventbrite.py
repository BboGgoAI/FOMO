import json

import requests
from bs4 import BeautifulSoup

# Sample JSON data
data = {"name": "John", "age": 30, "city": "New York"}


def pretty_print(data):
    # Convert the data to a JSON formatted string with 4 spaces of indentation
    json_str = json.dumps(data, indent=4)
    # Print the pretty-printed JSON string
    print(json_str)


BASE_URL = "https://www.eventbrite.com/d/ca--san-francisco/all-events/?page="


def scrape_eventbrite_page(url):
    print(f"scraping {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to load page: {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")
    events = []
    results = soup.find("div", class_="search-results-panel-content__events").find(
        "section"
    )
    if results is None:
        return events
    cards = results.find_all("li")
    for card in cards:
        event_details = card.find("section", class_="event-card-details").find("div")
        link = event_details.find("a", recursive=False).get("href")
        title = event_details.find("h3").get_text()
        details = event_details.find_all("p", recursive=False)
        date = ""
        location = ""
        if len(details) == 2:
            date = details[0].get_text()
            location = details[1].get_text()
        else:
            location = details[0].get_text()
        events.append(
            {"Title": title, "Date": date, "Link": link, "Location": location}
        )
    return events


events = []
i = 0
while True:
    events_from_page = scrape_eventbrite_page(BASE_URL + str(i))
    if len(events_from_page) == 0:
        break
    events.append(events_from_page)
    pretty_print(events)
    i += 1
