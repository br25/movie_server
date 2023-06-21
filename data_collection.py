from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

class MovieAndOtherfileScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.sql_file = open("data.sql", "w")
        self.category = None
        self.year = None
        self.current_sequence = 17627

    def __del__(self):
        self.sql_file.close()

    def prompt_category_selection(self):
        print("----------------- Only Admin Can Do It -------------------")
        print("Please select a movie or category from the following options:")

        categories = self.get_categories()  # Retrieve categories dynamically
        for i, category in enumerate(categories, start=1):
            print(f"{i}. {category}")

        category_num = input("Enter the number corresponding to your desired category: ")
        self.scrape_files(category_num)

    def get_categories(self):
        url = urljoin(self.base_url, "SAM-FTP-2/")  # Modify the URL accordingly
        session = requests.Session()
        soup = self._fetch_page(url, session)
        links = soup.select('.fb-n a')

        categories = []
        for link in links:
            category = link.text.strip()
            if category != "Parent Directory":
                categories.append(category)

        session.close()
        return categories

    def scrape_files(self, category_num):
        categories = self.get_categories()  # Retrieve categories dynamically

        try:
            category_index = int(category_num) - 1
            self.category = categories[category_index]  # Assign the selected category
        except (IndexError, ValueError):
            print("Invalid category number. Please try again.")
            return

        print(f"You have selected: {self.category}")

        if self.category == "English Movies":
            category = self.category.replace(" ", "%20")  # Replace space with %20
            self.prompt_year_selection(category)
        else:
            url = urljoin(self.base_url, f"SAM-FTP-2/{self.category}")
            session = requests.Session()
            self._scrape_page_files(url, session)
            session.close()

    def prompt_year_selection(self, category):
        years = self.get_years(category)  # Retrieve years dynamically

        print(f"Please select a year from the following options for {category}:")
        for i, year in enumerate(years, start=1):
            print(f"{i}. {year}")

        while True:
            year_num = input("Enter the number corresponding to your desired year: ")
            if year_num.isdigit() and int(year_num) <= len(years):
                break
            print("Invalid year number. Please try again.")

        self.year = years[int(year_num) - 1]  # Assign the selected year
        self.scrape_files_by_year(category, self.year)


    def get_years(self, category):
        url = urljoin(self.base_url, f"SAM-FTP-2/{category}")
        session = requests.Session()
        soup = self._fetch_page(url, session)
        links = soup.select('.fb-n a')

        years = []
        for link in links:
            year = link.text.strip()
            if year != "Parent Directory":
                years.append(year)

        session.close()
        return years

    def scrape_files_by_year(self, category, year):
        print(f"You have selected: {year}")

        self.year = year  # Assign the selected year

        url = urljoin(self.base_url, f"SAM-FTP-2/{category}/{year}")
        session = requests.Session()
        self._scrape_page_files(url, session)
        session.close()


    def _fetch_page(self, url, session):
        response = session.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup

    def _insert_file_data(self, file_id, file_name, file_url, image_url, category, year):
        category = category.replace(" ", "_")  # Replace spaces with underscores
        if year is not None:
            year = year.replace("(", "").replace(")", "")  # Remove parentheses from the year value
        file_name = file_name.replace("'", "''") # Replace ' to ''
        sql_statement = f"INSERT INTO movie_app_FileData (id, file_name, file_url, image_url, category, year) VALUES ({file_id}, '{file_name}', '{file_url}', '{image_url}', '{category}', '{year}');\n"
        self.sql_file.write(sql_statement)


    def _generate_file_id(self):
        self.current_sequence += 1
        file_id = str(self.current_sequence).zfill(8)  # Pad the sequence number with leading zeros if necessary
        return file_id


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

            # Generate movie ID
            file_id = self._generate_file_id()

            # Print statements for debugging
            print(f"Category: {self.category}")
            print(f"Year: {self.year}")

            # Insert movie data into SQL file
            self._insert_file_data(file_id, movie_or_file_name, file_url, image_url, self.category, self.year)

            print(f"File id: {file_id}")
            print(f"File Name: {movie_or_file_name}")
            print(f"File URL: {file_url}")
            print(f"Image URL: {image_url}")
            print("----")



# Create an instance of the MovieAndOtherfileScraper class
base_url = "http://172.16.50.7/"
scraper = MovieAndOtherfileScraper(base_url)

# Prompt user for category selection and scrape files
scraper.prompt_category_selection()
