from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

class MovieScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def scrape_movies(self, movie_category):
        # Create the URL based on the selected movie category
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
            return

        if category == "SAM-FTP-2/English Movies":
            url = urljoin(self.base_url, category)
            self._scrape_english_movies(url)
        else:
            url = urljoin(self.base_url, category)
            self._scrape_other_movies(url)

    def _scrape_english_movies(self, url):
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
                eng_url = year_url

                # Connect eng_url to url
                response_eng = requests.get(eng_url)
                html_content_eng = response_eng.text

                # Parse the English Movies page
                soup_eng = BeautifulSoup(html_content_eng, 'html.parser')

                # Extract the links
                links = soup_eng.select('.fb-n a')
                for link in links:
                    movie_name = link.text.strip()
                    movie_url = link['href']
                    full_url = urljoin(url, movie_url)

                    # Get the movie file URLs
                    response_full = requests.get(full_url)
                    soup_full = BeautifulSoup(response_full.text, 'html.parser')
                    file_links = soup_full.select('.fb-n a')

                    movie_file_url = None
                    movie_image_url = None

                    for file_link in file_links:
                        file_name = file_link.text.strip()
                        if file_name.endswith('.mkv') or file_name.endswith('.mp4') or file_name.endswith('.rar') or file_name.endswith('.AVI') or file_name.endswith('.avi'):
                            movie_file_url = urljoin(url, file_link['href'])
                        if file_name.endswith('.jpg'):
                            movie_image_url = urljoin(url, file_link['href'])

                    print(f"Movie: {movie_name}")
                    print(f"Movie File URL: {movie_file_url}")
                    print(f"Movie Image URL: {movie_image_url}")
                    print("----")

    def _scrape_other_movies(self, url):
        # Fetch the web page
        response = requests.get(url)
        html_content = response.text

        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the links
        links = soup.select('.fb-n a')
        for link in links:
            movie_name = link.text.strip()
            movie_url = link['href']
            full_url = urljoin(url, movie_url)

            # Get the movie file URLs
            response_full = requests.get(full_url)
            soup_full = BeautifulSoup(response_full.text, 'html.parser')
            file_links = soup_full.select('.fb-n a')

            movie_file_url = None
            movie_image_url = None

            for file_link in file_links:
                file_name = file_link.text.strip()
                if file_name.endswith('.mkv') or file_name.endswith('.mp4') or file_name.endswith('.rar') or file_name.endswith('.AVI') or file_name.endswith('.avi'):
                    movie_file_url = urljoin(url, file_link['href'])
                if file_name.endswith('.jpg'):
                    movie_image_url = urljoin(url, file_link['href'])

            print(f"Movie: {movie_name}")
            print(f"Movie File URL: {movie_file_url}")
            print(f"Movie Image URL: {movie_image_url}")
            print("----")


# Prompt user for movie category selection
movie_category = input("Enter the movie category (3D Movies, English Movies, Foreign Movies, IMDb Top-250 Movies, Tutorial): ")

# Create an instance of the MovieScraper class
base_url = "http://172.16.50.7/"
scraper = MovieScraper(base_url)

# Scrape movies based on the selected category
scraper.scrape_movies(movie_category)