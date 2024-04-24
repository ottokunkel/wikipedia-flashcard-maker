import requests
from bs4 import BeautifulSoup
import os

download_headers = { 
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    
}

def get_wikipedia_image_url(page):
   
    #grabs the link for the image given that it auto-redirects
    response = requests.get(f"https://en.wikipedia.org/w/index.php?search={page}")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    imglink = ""
   

    imgbox = soup.find('a', class_='mw-file-description')

    # if an image was found, then it grabs the image link
    if (imgbox == None):

        # grabs the first link from the search list
        newLink = soup.find('div', class_='mw-search-result-heading').a['href']

        # if there is a search result, grabs the link, else returns none
        if newLink:
            r2 = requests.get(f"https://en.wikipedia.org/{newLink}")
            
            soup = BeautifulSoup(r2.text, 'html.parser')

            # f = open('debug', 'w')
            # f.write(str(soup))
            
            imgbox = soup.find('a', class_='mw-file-description')
        else:
            return None
        
    
    # grabs the img link from the main page
    imglink = str(imgbox['href'])
    
    
    # returns the image link
    if (imglink != ""):
        response = requests.get(f"https://en.wikipedia.org/{imglink}")
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup:
            link = soup.find('div', class_='fullImageLink').a['href']
            link = link[2:]
            return f"https://{link}"
    

    return None


def download_image(url, filename):
    
    #downloads an image
    response = requests.get(url, headers=download_headers, stream=True)
    #print(response)
    #print(response.headers)
    with open(f"./img/{filename}", 'wb') as file:
        file.write( (response.content) )
    

def main(search_items):
    """Main function to process list of search items."""
    for item in search_items:
        image_url = get_wikipedia_image_url(item)
        if image_url:
            filename = f"{item.replace(' ', '_')}"
            filename = f"{filename.replace(',', '')}.png"
            download_image(image_url, filename)
            print(f"Downloaded {filename}")
        else:
            print(f"No image found for {item}")

if __name__ == "__main__":
    # Example list of items to search on Wikipedia
    items_to_search = [
        # "Pantheon, Rome", "Arch of Constantine", "Hagia Sophia",
        # "St. Peter's Basilica", "Step Pyramid of Djoser", "Stonehenge",
        # "Katsura Imperial Villa", "Chigi Chapel", "Il Redentore",
        # "Santa Maria della Salute", "Süleymaniye Mosque",
        # "Mosque-Cathedral of Córdoba", "Dome of Santa Maria del Fiore",
        # "Laurentian Library", "Sant'Andrea al Quirinale",
        # "St. Carlo alle Quattro Fontane", "Palazzo Carignano",
        # "Church of San Giuseppe, Ragusa Ibla", "Painted dome at Sant'Ignazio",
        # "Ceiling of the Chiesa del Gesú", "Court Library, Vienna",
        # "Basilica of St. John of God, Granada", "Karlskirche", "Sheldonian Theatre",
        # "Clarendon Building", "Radcliffe Camera", 
        "Syon House",
        "Project for Newton's Cenotaph"
        # "Dome of Santa Maria del Fiore",
    ]

    # items_to_search = [
    #    "Arch of Constantine"]

    main(items_to_search)
