import json
import csv

INPUT_FILE = '../hw2-task2/Sarvesh_Parab_task2.csv'
OUTPUT_FILE_1 = 'Sarvesh_Parab_task1_sim.csv'
OUTPUT_FILE_2 = 'Sarvesh_Parab_task1_ground_truth.csv'

out_1_fh = open(OUTPUT_FILE_1, 'w', newline='')
out_2_fh = open(OUTPUT_FILE_2, 'w', newline='')

ENTITY = "Person"

data_list = list()

with open(INPUT_FILE, 'r') as in_file:
    reader = csv.reader(in_file)
    for row in reader:
        if row[1] == ENTITY:
            data_list.append(row[2])

print(len(data_list))

