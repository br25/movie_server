from bs4 import BeautifulSoup
import requests

# Fetch the web page
url = "http://172.16.50.7/SAM-FTP-2/3D Movies"
response = requests.get(url)
html_content = response.text

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the links for 3D movies
links = soup.select('.fb-n a')
for link in links:
    movie_name = link.text.strip()
    movie_url = link['href']
    print(f"Movie: {movie_name}, URL: {movie_url}")

