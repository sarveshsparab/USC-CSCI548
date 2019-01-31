import json
import requests
import csv

INPUT_FILE = '../hw1-task1/youtube-data.json'
OUTPUT_FILE = 'Sarvesh_Parab_task2.csv'

CALAIS_URL = 'https://api.thomsonreuters.com/permid/calais'
CALAIS_ACCESS_TOKEN = 'IBTm4SETGTZhqgN8xiqAuZ3PZeGY0zr5'
HEADERS = {'X-AG-Access-Token': CALAIS_ACCESS_TOKEN, 'Content-Type': 'text/raw', 'outputformat': 'application/json'}

out_fh = open(OUTPUT_FILE, 'w', newline='')
csv_writer = csv.writer(out_fh, delimiter=',')

with open(INPUT_FILE) as json_file:
    youtube_json_data = json.load(json_file)


def query_calais(content_to_query_calais):
    response = requests.post(CALAIS_URL, data=content_to_query_calais, headers=HEADERS, timeout=80)

    content = response.text
    print('Results received: %s' % content)
    if response.status_code == 200:
        return content
    else:
        return "ERROR"


for youtube_url in youtube_json_data:
    youtube_title = youtube_json_data[youtube_url]['title']
    youtube_desc = youtube_json_data[youtube_url]['description']

    content_to_query_calais = youtube_title + "\n" + youtube_desc

    try:
        query_response = query_calais(content_to_query_calais.encode('utf-8'))
    except Exception as e:
        print("Error in connect")
        print(e)

    break

    #csv_writer.writerow([youtube_url, REGEX_PATTERN, ''.join(url)])

print("-------------------------------------------------")

