from bs4 import BeautifulSoup
import requests

# Prompt user for movie type selection
movie_type = input("Enter the movie type (3D Movies or English Movies): ")

# Create the URL based on the selected movie type
base_url = "http://172.16.50.7/SAM-FTP-2/"
if movie_type.lower() == "3d movies":
    url = base_url + "3D Movies"
elif movie_type.lower() == "english movies":
    url = base_url + "English Movies"
else:
    print("Invalid movie type.")
    exit()

# Fetch the web page
response = requests.get(url)
html_content = response.text

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the links for the selected movie type
links = soup.select('.fb-n a')
for link in links:
    movie_name = link.text.strip()
    movie_url = link['href']
    print(f"Movie: {movie_name}, URL: {movie_url}")
