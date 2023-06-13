from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

# Prompt user for movie category selection
movie_category = input("Enter the movie category (3D Movies, English Movies, Foreign Movies, IMDb Top-250 Movies, Tutorials): ")

# Create the URL based on the selected movie category
base_url = "http://172.16.50.7/SAM-FTP-2/"
category_mapping = {
    "3d movies": "3D Movies",
    "english movies": "English Movies",
    "foreign movies": "Foreign Language Movies",
    "imdb top-250 movies": "IMDb Top-250 Movies",
    "tutorials": "Tutorial"
}
category = category_mapping.get(movie_category.lower())
if category is None:
    print("Invalid movie category.")
    exit()

url = urljoin(base_url, category)

# Fetch the web page
response = requests.get(url)
html_content = response.text

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the links for the selected movie category
links = soup.select('.fb-n a')
for link in links:
    movie_name = link.text.strip()
    movie_url = link['href']
    full_url = urljoin(base_url, movie_url)
    print(f"Movie: {movie_name}, URL: {full_url}")
