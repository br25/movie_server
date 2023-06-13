from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

class MovieAndOtherfileScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def scrape_files(self, category):
        # Create the URL based on the selected movie category
        category_mapping = {
            "3d movies": "SAM-FTP-2/3D Movies",
            "english movies": "SAM-FTP-2/English Movies",
            "foreign movies": "SAM-FTP-2/Foreign Language Movies",
            "imdb top-250 movies": "SAM-FTP-2/IMDb Top-250 Movies",
            "tutorial": "SAM-FTP-2/Tutorial"
        }
        category = category_mapping.get(category.lower())
        if category is None:
            print("Invalid movie category.")
            return

        if category == "SAM-FTP-2/English Movies":
            url = urljoin(self.base_url, category)

            # Fetch and parse the web page
            soup = self._fetch_page(url)

            # Find all links with the specified years
            links = soup.select('.fb-n a')
            for link in links:
                year_url = urljoin(url, link['href'])
                if year_url != self.base_url:
                    url = year_url
                    self._scrape_page_files(url)
        else:
            url = urljoin(self.base_url, category)
            self._scrape_page_files(url)

    def _fetch_page(self, url):
        # Fetch the web page
        response = requests.get(url)
        html_content = response.text

        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup

    def _scrape_page_files(self, url):
        # Fetch and parse the web page
        soup = self._fetch_page(url)

        # Extract the links
        links = soup.select('.fb-n a')
        for link in links:
            movie_or_file_name = link.text.strip()
            file_url = link['href']
            full_page_url = urljoin(self.base_url, file_url)

            if movie_or_file_name == "Parent Directory":
                continue

            # Fetch and parse the web page
            soup = self._fetch_page(full_page_url)
            file_links = soup.select('.fb-n a')

            file_url = None
            image_url = None

            for file_link in file_links:
                file_name = file_link.text.strip()
                if file_name.endswith(('.mkv', '.mp4', '.rar', '.AVI', '.avi')):
                    file_url = urljoin(url, file_link['href'])
                if file_name.endswith('.jpg'):
                    image_url = urljoin(url, file_link['href'])

            print(f"File Name: {movie_or_file_name}")
            print(f"File URL: {file_url}")
            print(f"Image URL: {image_url}")
            print("----")


# Prompt user for category selection
print("-----------------Only Admin Do it-------------------")
print("Do not missed spelling bellows format data")
print("3D Movies, English Movies, Foreign Movies, IMDb Top-250 Movies, Tutorial")
category = input("Enter the movie or other category (3D Movies, English Movies, Foreign Movies, IMDb Top-250 Movies, Tutorial): ")

# Create an instance of the MovieAndOtherfileScraper class
base_url = "http://172.16.50.7/"
scraper = MovieAndOtherfileScraper(base_url)

# Scrape files based on the selected category
scraper.scrape_files(category)
