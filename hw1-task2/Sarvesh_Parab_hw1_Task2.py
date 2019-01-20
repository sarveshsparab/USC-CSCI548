import requests
from bs4 import BeautifulSoup

# Primary page URL to scrape
PAGE_TO_SCRAPE = 'https://www.datacamp.com/courses/all'

# Requesting the HTML content of the page
web_page = requests.get(PAGE_TO_SCRAPE)

# Creating the beautiful soup instance
soup = BeautifulSoup(web_page.content, 'html.parser')

# Fetching the html element
html = list(soup.children)[2]

print(html)
