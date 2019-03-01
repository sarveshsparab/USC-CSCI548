import json
import re
import csv

INPUT_FILE = 'Sarvesh_Parab_task1_sim.csv'
OUTPUT_FILE = 'Sarvesh_Parab_task1_ground_truth.csv'

RANDOM_NUMBERS = [7, 16, 28, 68, 72, 73, 80, 81, 86, 87, 90, 95,
                  100, 102, 106, 107, 133, 135, 137, 155, 164, 175, 177, 182, 194, 196, 199, 205, 216, 218,
                  229, 234, 248, 263, 275, 280, 283, 296, 309, 317, 338, 342, 345, 350]

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

