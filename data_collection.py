from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

# Prompt user for movie category selection
movie_category = input("Enter the movie category (3D Movies, English Movies, Foreign Movies, IMDb Top-250 Movies, Tutorial): ")

# Create the URL based on the selected movie category
base_url = "http://172.16.50.7/"
category_mapping = {
    "3d movies": "SAM-FTP-2/3D Movies",
    "english movies": "SAM-FTP-2/English Movies",
    "foreign movies": "SAM-FTP-2/Foreign Language Movies",
    "imdb top-250 movies": "SAM-FTP-2/IMDb Top-250 Movies",
    "tutorial": "SAM-FTP-2/Tutorial"
}
category = category_mapping.get(movie_category.lower())
if category is None:
    print("Invalid movie category.")
    exit()

if category == "SAM-FTP-2/English Movies":
    url = urljoin(base_url, category)
    # Fetch the web page
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all links with the specified years
    year_links = soup.select('a[href*="/SAM-FTP-2/English%20Movies/"]')
    for link in year_links:
        year_url = urljoin(url, link['href'])
        if "Parent Directory" not in link.text:
            print(year_url)