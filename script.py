import requests
from bs4 import BeautifulSoup
import os

def get_wikipedia_image_url(page):
   
    #grabs the link for the image given that it auto-redirects
    response = requests.get(f"https://en.wikipedia.org/w/index.php?search={page}")
    soup = BeautifulSoup(response.text, 'html.parser')
    soup = soup.find('table', class_='infobox').find('a', class_='mw-file-description')
    

    if soup:
        link = "https://upload.wikimedia.org/wikipedia/commons/e/ef/" + (soup['href'].split(':')[1])

        #closes the previous reponse
        response.close()
        return link

    return None


def download_image(url, filename):
    
    #downloads an image
    response = requests.get(url)
    with open(f"./img/{filename}", 'wb') as file:
        file.write(response.content)

def main(search_items):
    """Main function to process list of search items."""
    for item in search_items:
        image_url = get_wikipedia_image_url(item)
        # if image_url:
        #     filename = f"{item.replace(' ', '_')}.jpg"
        #     filename = f"{filename.replace(',', '')}"
        #     download_image(image_url, filename)
        #     print(f"Downloaded {filename}")
        # else:
        #     print(f"No image found for {item}")

if __name__ == "__main__":
    # Example list of items to search on Wikipedia
    # items_to_search = [
    #     "Pantheon, Rome", "Arch of Constantine", "Hagia Sophia",
    #     "St. Peter's Basilica", "Step Pyramid of Djoser", "Stonehenge",
    #     "Katsura Imperial Villa", "Chigi Chapel", "Il Redentore",
    #     "Santa Maria della Salute", "Süleymaniye Mosque",
    #     "Mosque-Cathedral of Córdoba", "Dome of Santa Maria del Fiore",
    #     "Laurentian Library", "Sant'Andrea al Quirinale",
    #     "St. Carlo alle Quattro Fontane", "Palazzo Carignano",
    #     "Church of San Giuseppe, Ragusa Ibla", "Painted dome at Sant'Ignazio",
    #     "Ceiling of the Chiesa del Gesú", "Court Library, Vienna",
    #     "Basilica of St. John of God, Granada", "Karlskirche", "Sheldonian Theatre",
    #     "Clarendon Building", "Radcliffe Camera", "Syon House",
    #     "Project for Newton's Cenotaph"
    # ]

    items_to_search = [
        "Pantheon, Rome"]

    main(items_to_search)
