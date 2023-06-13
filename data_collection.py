from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

class MovieAndOtherfileScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def prompt_category_selection(self):
        print("----------------- Only Admin Can Do It -------------------")
        print("Please select a movie or category from the following options:")
        print("1. 3D Movies")
        print("2. English Movies")
        print("3. Foreign Movies")
        print("4. IMDb Top-250 Movies")
        print("5. Tutorial")

        category_num = input("Enter the number corresponding to your desired category: ")
        self.scrape_files(category_num)

    def scrape_files(self, category_num):
        # Map category number to category name
        category_mapping = {
            "1": "SAM-FTP-2/3D Movies",
            "2": "SAM-FTP-2/English Movies",
            "3": "SAM-FTP-2/Foreign Movies",
            "4": "SAM-FTP-2/IMDb Top-250 Movies",
            "5": "SAM-FTP-2/Tutorial"
        }

        # Validate and retrieve the category name
        category = category_mapping.get(category_num)
        if category is None:
            print("Invalid category number. Please try again.")
            return

        print(f"You have selected: {category}")

        if category == "SAM-FTP-2/English Movies":
            url = urljoin(self.base_url, category)
            session = requests.Session()
            soup = self._fetch_page(url, session)
            links = soup.select('.fb-n a')
            for link in links:
                year_url = urljoin(url, link['href'])
                if year_url != self.base_url:
                    url = year_url
                    self._scrape_page_files(url, session)
            session.close()
        else:
            url = urljoin(self.base_url, category)
            session = requests.Session()
            self._scrape_page_files(url, session)
            session.close()

    def _fetch_page(self, url, session):
        response = session.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup

    def _scrape_page_files(self, url, session):
        soup = self._fetch_page(url, session)
        links = soup.select('.fb-n a')

        for link in links:
            movie_or_file_name = link.text.strip()
            file_url = link['href']
            full_page_url = urljoin(self.base_url, file_url)

            if movie_or_file_name == "Parent Directory":
                continue

            soup = self._fetch_page(full_page_url, session)
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


# Create an instance of the MovieAndOtherfileScraper class
base_url = "http://172.16.50.7/"
scraper = MovieAndOtherfileScraper(base_url)

# Prompt user for category selection and scrape files
scraper.prompt_category_selection()
