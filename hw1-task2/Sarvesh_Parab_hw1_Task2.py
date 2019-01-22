import requests
import json
from bs4 import BeautifulSoup

# Primary page URL to scrape
PAGE_TO_SCRAPE = 'https://www.datacamp.com/courses/all'

# Other static values
SITE_PREFIX = "https://www.datacamp.com"
COURSES_TO_SCRAPE = -1                  # Number of courses to scrape (-1 for all possible courses)

# Fields to extract and their corresponding json keys
# Mandatory Fields
TITLE = 'title'                         # Title for the course
URL = 'url'                             # URL for the course
DESC = 'description'                    # A brief description about the course
AUTHOR_NAME = 'name'                    # Name of the author/instructor
AUTHOR_ORG = 'organization'             # Designation and organization of the author

# Sub-level JSON fields
AUTHORS_SUB_JSON = 'authors'
DATASETS_SUB_JSON = 'datasets-used'

# Add-on fields
ID = 'id'                               # Course ID as per the datacamp website
AUTHOR_URL = 'url'                      # Page on author for the course
DURATION = 'duration'                   # Duration of the course
EXERCISES = 'exercises'                 # Number of exercises
VIDEOS = 'videos'                       # Number of videos
PARTICIPANTS = 'participants'           # Number of participants who have taken this course
DATASET_NAME = 'name'                   # Dataset name used in the course if any
DATASET_URL = 'url'                     # CSV file of the Dataset
CHAPTERS = 'chapters'                   # List of chapters or topics covered in the course


# This function fetches the details about the authors/instructors
def fetch_course_instructors(authors_divs):
    authors_list = list()
    author_count = 0
    for author in authors_divs:
        author_dict = dict()

        author_dict[AUTHOR_NAME] = author.find("h5", class_="course__instructor-name").string
        author_dict[AUTHOR_ORG] = author.find("p", class_="course__instructor-occupation").string
        author_dict[AUTHOR_URL] = SITE_PREFIX + author.find("a")['href']

        authors_list.append(author_dict)

        author_count += 1

        if author_count == len(authors_divs)/2:
            break

    return authors_list


# This function fetches details about the datasets being used the course
def fetch_course_datasets(datasets_divs):
    datasets_list = list()
    for dataset in datasets_divs:
        dataset_dict = dict()

        dataset_dict[DATASET_NAME] = dataset.find("a").get_text().strip()
        dataset_dict[DATASET_URL] = dataset.find("a")['href']

        datasets_list.append(dataset_dict)

    return datasets_list


# This function fetches the chapters or topics covered in the course
def fetch_course_chapters(chapters_h4s):
    chapters_list = list()
    chapter_count = 0
    for chapter in chapters_h4s:
        chapters_list.append(chapter.get_text().strip())

        chapter_count += 1

        if chapter_count == len(chapters_h4s) / 2:
            break

    return chapters_list


# This function browses the specific course web pages and parses them
def fetch_course_nested_data(course_dict, course_url):
    nested_web_page = requests.get(course_url)
    nested_soup = BeautifulSoup(nested_web_page.content, 'html.parser')

    course_dict[EXERCISES] = nested_soup.find("li", class_="header-hero__stat header-hero__stat--exercises")\
        .get_text().split(" ")[0]
    course_dict[VIDEOS] = nested_soup.find("li", class_="header-hero__stat header-hero__stat--videos") \
        .get_text().split(" ")[0]
    course_dict[PARTICIPANTS] = nested_soup.find("li", class_="header-hero__stat header-hero__stat--participants") \
        .get_text().split(" ")[0]
    course_dict[DESC] = nested_soup.find("p", class_="course__description") \
        .get_text()

    course_dict[AUTHORS_SUB_JSON] = fetch_course_instructors(nested_soup.find_all("div", class_="course__instructor"))

    course_dict[DATASETS_SUB_JSON] = fetch_course_datasets(nested_soup.find_all("li", class_="course__dataset"))

    course_dict[CHAPTERS] = fetch_course_chapters(nested_soup.find_all("h4", class_="chapter__title"))


# Function to fetch the fields from the base page and navigate further
def fetch_course_data(article_div):
    course_dict = dict()
    course_dict[ID] = article_div['data-id']
    course_dict[URL] = SITE_PREFIX + article_div.div.a['href']
    course_dict[TITLE] = article_div.find("h4", class_="course-block__title").string
    course_dict[DURATION] = article_div.find("span", class_="course-block__length").get_text().strip()

    fetch_course_nested_data(course_dict, course_dict[URL])

    return course_dict


# Main Function
if __name__ == '__main__':
    # Requesting the HTML content of the page
    web_page = requests.get(PAGE_TO_SCRAPE)

    # Creating the beautiful soup instance
    soup = BeautifulSoup(web_page.content, 'html.parser')

    # Fetching the div element which houses the courses list
    courses_explore_div = soup.find("div", class_="courses__explore-list row")

    # Fetching every child article for every course
    courses_articles = courses_explore_div.find_all("article")

    courses_count = 0

    courses_dict = dict()
    # Iterate over every course article
    for course_article in courses_articles:
        courses_dict['course-'+course_article['data-id']+'-info'] = fetch_course_data(course_article)

        courses_count += 1
        if COURSES_TO_SCRAPE != -1 and courses_count > COURSES_TO_SCRAPE:
            break

    data_dict = dict()
    data_dict['courses-info'] = courses_dict

    # Disclaimer information
    data_dict['misc-info'] = {
        "Author": "Sarvesh Parab",
        "Purpose": "Scrapped for the USC CSCI 548 course",
        "Assignment": "HW1 - Task 2",
        "Term": "Spring 2019",
        "Date": "1/21/2019"
    }

    with open('Sarvesh_Parab_Task2_data.json', 'w') as fw:
        json.dump(data_dict, fw, sort_keys=True, indent=4)


