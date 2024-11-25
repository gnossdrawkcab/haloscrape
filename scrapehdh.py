import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import requests
from bs4 import BeautifulSoup

# Map player names to CSV file names
player_name_map = {
    "l 0cty l": "octy.csv",
    "Zaidster7": "zaidster7.csv",
    "l P1N1 l": "p1n1.csv",
    "l Jordo l": "jordo.csv",
    "l Viper18 l": "viper18.csv"
}

def load_existing_links(player_name):
    csv_file = f"csv/{player_name_map[player_name]}"
    existing_links = set()  # Use a set for faster lookups

    print(f"Checking if CSV file exists for {player_name}: {csv_file}")
    
    if os.path.exists(csv_file):
        print(f"File {csv_file} exists, reading data...")
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                if row:
                    # Extract and clean match ID
                    full_link = row[0].strip()
                    match_id = full_link.split("/")[-1].split("?")[0].lower()  # Ensure lowercase
                    print(f"Loaded existing match ID: {match_id}")  # Debug
                    existing_links.add(match_id)
    else:
        print(f"File {csv_file} does not exist.")
    
    print(f"Total existing links for {player_name}: {len(existing_links)}")
    return existing_links, csv_file


def get_links(base_url, player_name, pages_to_scrape):
    existing_links, _ = load_existing_links(player_name)
    links = []  # List to store all collected links

    print(f"Starting scraping for {player_name}...")

    for page in range(pages_to_scrape):
        if page == 0:
            url = base_url
        else:
            url = f"{base_url}?page={page}&filter=Matchmade"

        # Fetch the page content
        print(f"Fetching page {page + 1} of {pages_to_scrape}...")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
            continue

        # Parse the page
        soup = BeautifulSoup(response.text, 'html.parser')
        table_rows = soup.find_all('tr', attrs={'data-href': True})

        for row in table_rows:
            link = row['data-href'].strip()
            match_id = link.split("/")[-1].split("?")[0].lower()  # Ensure lowercase

            # Debugging: Log the scraped and extracted match ID
            print(f"Scraped link: {link}")
            print(f"Extracted match ID: {match_id}")

            if match_id in existing_links:
                print(f"Duplicate match ID found: {match_id}. Stopping scraping for {player_name}.")
                return links  # Return the links collected so far and stop scraping

            print(f"New match found: {match_id}")
            full_link = "https://halodatahive.com" + link
            links.append(full_link)

    print(f"Scraping completed for {player_name}, {len(links)} new links found.")
    return links

# Function to append new links to CSV
def append_to_csv(player_name, new_links):
    csv_file = f"csv/{player_name_map[player_name]}"
    
    print(f"Appending new links to {csv_file}...")
    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for link in new_links:
            writer.writerow([link])  # Write the new link

# Main execution
if __name__ == "__main__":
    print("Welcome to the Halo Data Hive Scraper!")

    # For each player, check if a CSV file exists, and scrape if needed
    for player_name in player_name_map.keys():
        print(f"Scraping data for {player_name}...")

        # Load existing links and scrape new ones
        existing_links, csv_file = load_existing_links(player_name)
        base_url = f"https://halodatahive.com/Player/Infinite/{player_name.replace(' ', '%20')}"
        
        print(f"Existing links for {player_name}: {len(existing_links)}")
        
        # Start scraping until a duplicate is found
        new_links = get_links(base_url, player_name, 75)  # 75 pages max
        
        # Append new links to the CSV
        if new_links:
            append_to_csv(player_name, new_links)
            print(f"Completed scraping for {player_name}. New links added: {len(new_links)}")
        else:
            print(f"No new links to add for {player_name}.")

    print("Scraping complete for all players!")
