import json
import re
import csv

INPUT_FILE = 'Sarvesh_Parab_task1_sim.csv'
OUTPUT_FILE = 'Sarvesh_Parab_task1_ground_truth.csv'

RANDOM_NUMBERS = [10, 46, 64, 68, 73, 112, 117, 123, 127, 137, 151, 154, 212, 213,
                  217, 240, 262, 273, 277, 282, 284, 299, 301, 314, 317]

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

