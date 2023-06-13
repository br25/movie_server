from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

# Fetch the web page
url = "http://172.16.50.7/SAM-FTP-2/3D Movies"
response = requests.get(url)
html_content = response.text

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the links for the 3D movies
links = soup.select('.fb-n a')
for link in links:
    movie_name = link.text.strip()
    movie_url = link['href']
    full_url = urljoin(url, movie_url)

    # Get the movie file URL
    response_full = requests.get(full_url)
    soup_full = BeautifulSoup(response_full.text, 'html.parser')
    file_links = soup_full.select('.fb-n a')

    for file_link in file_links:
        file_name = file_link.text.strip()
        if file_name.endswith('.mkv'):
            movie_file_url = urljoin(url, file_link['href'])
            print(f"Movie: {movie_name}")
            print(f"Movie File: {file_name}")
            print(f"Movie File URL: {movie_file_url}")
            break