import json
import re
import csv

INPUT_FILE = '../hw1-task1/youtube-data.json'
OUTPUT_FILE = 'Sarvesh_Parab_task3.csv'

RANDOM_NUMBERS = [15, 23, 30, 43, 45, 66, 69, 92, 102, 105, 118, 123, 125, 136, 152, 156, 172, 174, 175, 178, 183,
                  189, 236, 250, 269, 271, 273, 274, 277, 287, 303, 304, 306, 310, 338, 341, 344, 357, 403, 421, 423,
                  442, 451, 454, 463, 467, 495, 507, 514, 516, 519, 522, 537, 546, 570, 592, 602, 604, 615, 618, 630,
                  661, 666, 672, 679, 682, 713, 714, 727, 743, 748, 775, 776, 780, 788, 802, 813, 819, 828, 829, 836,
                  845, 847, 855, 863, 893, 895, 898, 909, 938, 946, 958, 959, 961, 963, 967, 972, 974, 979, 985]

LIMIT = 50

out_fh = open(OUTPUT_FILE, 'w', newline='')
csv_writer = csv.writer(out_fh, delimiter=',')

with open(INPUT_FILE) as json_file:
    youtube_json_data = json.load(json_file)

vid_count = 0
random_list_counter = 0
vid_saved = 0

for youtube_url in youtube_json_data:
    vid_count += 1

    if vid_saved > LIMIT:
        break

    if vid_count == RANDOM_NUMBERS[random_list_counter]:
        random_list_counter += 1
        try:
            if len(youtube_json_data[youtube_url]['description']) != 0:
                csv_writer.writerow([str(vid_count), youtube_url, youtube_json_data[youtube_url]['description']])
                vid_saved += 1
        except Exception as e:
            print(e)

