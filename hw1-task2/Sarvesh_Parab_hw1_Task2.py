import requests
import json
from bs4 import BeautifulSoup

# Primary page URL to scrape
PAGE_TO_SCRAPE = 'https://www.datacamp.com/courses/all'

# Other static values
SITE_PREFIX = "https://www.datacamp.com"

# Fields to extract and their corresponding json keys
ID = 'id'
URL = 'url'
TITLE = 'title'
AUTHORS_SUB_JSON = 'authors'
AUTHOR_NAME = 'name'
AUTHOR_ORG = 'organization'
AUTHOR_URL = 'url'
DESC = 'description'
DURATION = 'duration'
EXERCISES = 'exercises'
VIDEOS = 'videos'
PARTICIPANTS = 'participants'
DATASETS_SUB_JSON = 'datasets-used'
DATASET_NAME = 'name'
DATASET_URL = 'url'


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

        dataset_dict[DATASET_NAME] = dataset.find("a")['href']
        dataset_dict[DATASET_URL] = dataset.find("a").get_text()

        datasets_list.append(dataset_dict)

    return datasets_list


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

    temp = 0

    courses_dict = dict()
    # Iterate over every course article
    for course_article in courses_articles:
        courses_dict['course-'+course_article['data-id']+'-info'] = fetch_course_data(course_article)
        temp += 1
        if temp > 5:
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


