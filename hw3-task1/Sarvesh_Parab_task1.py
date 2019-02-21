import json
import csv
import requests
import urllib.parse

INPUT_FILE = '../hw2-task2/Sarvesh_Parab_task2.csv'
OUTPUT_FILE_1 = 'Sarvesh_Parab_task1_sim.csv'
OUTPUT_FILE_2 = 'Sarvesh_Parab_task1_ground_truth.csv'

out_1_fh = open(OUTPUT_FILE_1, 'w', newline='')
out_2_fh = open(OUTPUT_FILE_2, 'w', newline='')

ENTITY = "Person"

API_URL_PREFIX = "https://dblp.org/search/author/api?q="
API_URL_SUFFIX = "&format=json"

data_list = list()

with open(INPUT_FILE, 'r') as in_file:
    reader = csv.reader(in_file)
    for row in reader:
        if row[1] == ENTITY:
            data_list.append(row[2])


def query_api(api_url):
    response = requests.get(api_url)
    content = response.text
    if response.status_code == 200:
        return content
    else:
        return "ERROR"


def parse_result(q_json):
    res = list()
    if 'hit' in q_json['result']['hits'] and len(q_json['result']['hits']['hit']) > 0:
        for hit in q_json['result']['hits']['hit']:
            res.append((hit['info']['author'], hit['info']['url']))

    return res


for ent in data_list:
    api_url = API_URL_PREFIX + urllib.parse.quote_plus(ent) + API_URL_SUFFIX

    try:
        query_result = query_api(api_url)
        query_result_json = json.loads(query_result)

        parsed_result = parse_result(query_result_json)
        print(parsed_result)
    except Exception as e:
        print("Error in handling : " + ent)
        print(e)

    #break




