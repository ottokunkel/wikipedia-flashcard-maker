import requests
from bs4 import BeautifulSoup
import os

def get_wikipedia_image_url(page):
    """Retrieve the main image URL from a Wikipedia page."""
    response = requests.get(f"https://en.wikipedia.org/w/index.php?search={page}")
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    searchRes = soup.find('li', class_='mw-search-result mw-search-result-ns-0')  # Targets the infobox where main images usually reside
    print(searchRes)
    if searchRes:
        
        href = searchRes.find('href')
        response2 = requests.get(f"https://en.wikipedia.org/{href}")
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        imglink = soup2.find('infobox-image')
        
        if imglink:
            
            return imglink
    return None

def download_image(url, filename):
    """Download an image from a given URL."""
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

def main(search_items):
    """Main function to process list of search items."""
    for item in search_items:
        image_url = get_wikipedia_image_url(item)
        if image_url:
            filename = f"{item.replace(' ', '_')}.jpg"
            download_image(image_url, filename)
            print(f"Downloaded {filename}")
        else:
            print(f"No image found for {item}")

if __name__ == "__main__":
    # Example list of items to search on Wikipedia
    items_to_search = ["Albert Einstein", "Eiffel Tower", "Python (programming language)"]
    main(items_to_search)
