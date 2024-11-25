import requests
from bs4 import BeautifulSoup

# Function to scrape eagle_score from the specified selector
def scrape_eagle_score():
    # Define the URL
    url = "https://halodatahive.com/Infinite/Match/4ef86b53-48b2-41f5-b0e9-2ab08bc3b17d?gamertag=l%200cty%20l&type=Matchmade&page=0"

    # Send an HTTP GET request to fetch the HTML content
    print(f"Fetching data from URL: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Target the eagle_score using the provided CSS selector
    eagle_score_element = soup.select_one('.match-header > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h2:nth-child(2)')

    # Check if the element exists and return the eagle_score
    if eagle_score_element:
        eagle_score = eagle_score_element.get_text(strip=True)
        return eagle_score
    else:
        print("eagle_score element not found.")
        return None

# Call the function to scrape the eagle_score
eagle_score = scrape_eagle_score()

# Print the result
if eagle_score:
    print(f"Eagle Score: {eagle_score}")
else:
    print("Failed to scrape the eagle score.")
