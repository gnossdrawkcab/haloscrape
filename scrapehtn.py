from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import csv

# Function to scrape player stats for Player 1 (Table 1)
def scrape_player_1_stats(match_id):
    # Start a virtual display (visibility 0)
    display = Display(visible=0, size=(1024, 768))
    display.start()

    CHROMEDRIVER_PATH = "./chromedriver/chromedriver"
    chrome_options = Options()
    chrome_options.binary_location = "./chrome/chrome"
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=chrome_options)
    player_stats = []

    try:
        # Navigate to the match URL
        url = f"https://halotracker.com/halo-infinite/match/{match_id}"
        print(f"Navigating to URL: {url}")
        driver.get(url)

        # Click dropdown for Player 1
        dropdown_selector = ".match-scoreboard--team-1 > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(10)"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown_selector))).click()
        print("Dropdown clicked for Player 1")

        # Scrape stats for Player 1 using CSS selectors
        player_selector = ".match-scoreboard--team-1 > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(1) > a:nth-child(1)"
        rating_selector = ".match-scoreboard--team-1 > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1) > span:nth-child(2)"
        dealt_selector = ".match-scoreboard--team-1 > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(4)"
        taken_selector = ".match-scoreboard--team-1 > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(6)"
        kills_selector = ".match-scoreboard--team-1 > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(8)"
        deaths_selector = ".match-scoreboard--team-1 > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(9)"

        # Additional stats (score, rounds won, rounds lost, assists)
        score_selector = "div.drawer-category:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)"
        rounds_won_selector = "div.drawer-category:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2)"
        rounds_lost_selector = "div.drawer-category:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(3)"
        assists_selector = "div.drawer-category:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(4)"

        # Additional stats (grenade kills, headshot kills, melee kills, etc.)
        grenade_kills_selector = "div.drawer-category:nth-child(1) > div:nth-child(2) > div:nth-child(6) > div:nth-child(2)"
        headshot_kills_selector = "div.drawer-category:nth-child(1) > div:nth-child(2) > div:nth-child(6) > div:nth-child(7)"
        melee_kills_selector = "div.drawer-category:nth-child(1) > div:nth-child(2) > div:nth-child(6) > div:nth-child(8)"
        fired_selector = "div.drawer-category:nth-child(1) > div:nth-child(2) > div:nth-child(6) > div:nth-child(9)"
        hit_selector = "div.drawer-category:nth-child(1) > div:nth-child(2) > div:nth-child(6) > div:nth-child(10)"
        accuracy_selector = "div.drawer-category:nth-child(1) > div:nth-child(2) > div:nth-child(6) > div:nth-child(11)"
        callout_assists_selector = "div.drawer-category:nth-child(1) > div:nth-child(2) > div:nth-child(6) > div:nth-child(12)"
        max_spree_selector = "div.drawer-category:nth-child(1) > div:nth-child(2) > div:nth-child(6) > div:nth-child(13)"

        # Extract values
        player = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, player_selector))
        ).text

        rating = driver.find_element(By.CSS_SELECTOR, rating_selector).text
        dealt = driver.find_element(By.CSS_SELECTOR, dealt_selector).text
        taken = driver.find_element(By.CSS_SELECTOR, taken_selector).text
        kills = driver.find_element(By.CSS_SELECTOR, kills_selector).text
        deaths = driver.find_element(By.CSS_SELECTOR, deaths_selector).text

        # Extract additional stats
        score = driver.find_element(By.CSS_SELECTOR, score_selector).text
        rounds_won = driver.find_element(By.CSS_SELECTOR, rounds_won_selector).text
        rounds_lost = driver.find_element(By.CSS_SELECTOR, rounds_lost_selector).text
        assists = driver.find_element(By.CSS_SELECTOR, assists_selector).text

        # Extract new stats
        grenade_kills = driver.find_element(By.CSS_SELECTOR, grenade_kills_selector).text
        headshot_kills = driver.find_element(By.CSS_SELECTOR, headshot_kills_selector).text
        melee_kills = driver.find_element(By.CSS_SELECTOR, melee_kills_selector).text
        fired = driver.find_element(By.CSS_SELECTOR, fired_selector).text
        hit = driver.find_element(By.CSS_SELECTOR, hit_selector).text
        accuracy = driver.find_element(By.CSS_SELECTOR, accuracy_selector).text
        callout_assists = driver.find_element(By.CSS_SELECTOR, callout_assists_selector).text
        max_spree = driver.find_element(By.CSS_SELECTOR, max_spree_selector).text

        print(f"Player: {player}, Rating: {rating}, Dealt: {dealt}, Taken: {taken}, Kills: {kills}, Deaths: {deaths}")
        print(f"Score: {score}, Rounds Won: {rounds_won}, Rounds Lost: {rounds_lost}, Assists: {assists}")
        print(f"Grenade Kills: {grenade_kills}, Headshot Kills: {headshot_kills}, Melee Kills: {melee_kills}")
        print(f"Fired: {fired}, Hit: {hit}, Accuracy: {accuracy}, Callout Assists: {callout_assists}, Max Spree: {max_spree}")

        # Save stats to list
        player_stats.append({
            "match_id": match_id,
            "player": player,
            "rating": rating,
            "dealt": dealt,
            "taken": taken,
            "kills": kills,
            "deaths": deaths,
            "score": score,
            "rounds_won": rounds_won,
            "rounds_lost": rounds_lost,
            "assists": assists,
            "grenade_kills": grenade_kills,
            "headshot_kills": headshot_kills,
            "melee_kills": melee_kills,
            "fired": fired,
            "hit": hit,
            "accuracy": accuracy,
            "callout_assists": callout_assists,
            "max_spree": max_spree
        })

    except Exception as e:
        print(f"Error processing match {match_id}: {e}")

    finally:
        print("Closing Selenium browser...")
        driver.quit()
        display.stop()

    return player_stats

# Save to CSV
def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

# Test with one match ID
match_id = "2d8d9e44-c012-43d5-8310-e0f12cd6859b"
player_stats = scrape_player_1_stats(match_id)
if player_stats:
    save_to_csv(player_stats, "./csv/player_1_stats.csv")
    print("Data saved to player_1_stats.csv")
