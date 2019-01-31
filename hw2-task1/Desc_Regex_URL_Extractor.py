import json
import re
import csv

INPUT_FILE = '../hw1-task1/youtube-data.json'
OUTPUT_FILE = 'Sarvesh_Parab_task1.csv'

REGEX_PATTERN = r'(http)(s?)(:\/\/)(www\.)?([-a-zA-Z0-9@:%._\+~#=]{2,256})(\.)([a-z]{2,4})(\b)([-a-zA-Z0-9@:%_\+~#?&//=]*)'
# regexr.com/47eto  <<-- tested here

REGEX_PATTERN1 = 'http'

out_fh = open(OUTPUT_FILE, 'w', newline='')
csv_writer = csv.writer(out_fh, delimiter=',')

with open(INPUT_FILE) as json_file:
    youtube_json_data = json.load(json_file)

for youtube_url in youtube_json_data:
    youtube_desc = youtube_json_data[youtube_url]['description']
    url_pattern = re.compile(REGEX_PATTERN)
    matched_urls = url_pattern.findall(youtube_desc)
    for url in matched_urls:
        csv_writer.writerow([youtube_url, REGEX_PATTERN, ''.join(url)])



