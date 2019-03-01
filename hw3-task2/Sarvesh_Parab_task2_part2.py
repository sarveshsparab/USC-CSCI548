import json
import re
import csv

INPUT_FILE = 'Sarvesh_Parab_task2_sim.csv'
OUTPUT_FILE = 'Sarvesh_Parab_task2_ground_truth.csv'

RANDOM_NUMBERS = [17, 34, 48, 61, 105, 211, 214,
                  277, 289, 320, 371, 393, 421, 447,
                  476, 481, 493, 513, 556, 590, 618, 624, 628, 660, 668, 676,
                  700, 719, 727, 732, 733, 746, 792]

LIMIT = 20

out_fh = open(OUTPUT_FILE, 'w', newline='')
csv_writer = csv.writer(out_fh, delimiter=',')

data_list = list()

with open(INPUT_FILE, 'r') as in_file:
    reader = csv.reader(in_file)
    for row in reader:
        data_list.append(row)

item_count = 0
random_list_counter = 0
item_saved = 0

for data in data_list:
    item_count += 1

    if item_saved > LIMIT - 1:
        break

    if item_count == RANDOM_NUMBERS[random_list_counter]:
        random_list_counter += 1
        try:
            csv_writer.writerow([data[0], data[2]])
            item_saved += 1
        except Exception as e:
            print(e)

