import xmltodict
import csv
import requests
import urllib.parse
from nltk.metrics.distance import jaro_winkler_similarity

NA_FLAG = True

INPUT_FILE = '../hw2-task2/Sarvesh_Parab_task2.csv'
if NA_FLAG:
    OUTPUT_FILE_1 = 'Sarvesh_Parab_task2_sim.csv'
    LOG_FILE = 'log_noNA.txt'
else:
    OUTPUT_FILE_1 = 'Sarvesh_Parab_task2_sim_noBlank.csv'
    LOG_FILE = 'log.txt'

out_1_fh = open(OUTPUT_FILE_1, 'w', newline='')
log_fh = open(LOG_FILE, 'w+', newline='')

csv_writer_1 = csv.writer(out_1_fh, delimiter=',')

ENTITY = ["Organization", "Company"]

API_URL_PREFIX = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryClass=Organisation&QueryString="
API_URL_SUFFIX = ""

data_list = list()

with open(INPUT_FILE, 'r') as in_file:
    reader = csv.reader(in_file)
    for row in reader:
        if row[1] in ENTITY:
            data_list.append(row[2])


def log(data):
    log_fh.write(data + '\n')
    print(data)


def query_api(api_url):
    response = requests.get(api_url)
    content = response.text
    if response.status_code == 200:
        return content
    else:
        return "ERROR"


def parse_result(q_xml):
    res = list()
    if 'Result' in q_xml['ArrayOfResult'] and len(q_xml) > 0:
        if isinstance(q_xml['ArrayOfResult']['Result'], list):
            for x in q_xml['ArrayOfResult']['Result']:
                res.append((x['Label'], x['URI']))
        else:
            res.append((q_xml['ArrayOfResult']['Result']['Label'], q_xml['ArrayOfResult']['Result']['URI']))

    return res


def get_best_match(ent, p_list):
    max_val = -1
    max_entity = ""
    max_list = list()
    for p in p_list:
        sim_val = jaro_winkler_similarity(ent, p[0])
        log("\t\tSim value between : " + ent + " | " + p[0] + "   =>   " + str(sim_val))
        if max_val < sim_val:
            max_val = sim_val
            max_entity = p

    for p in p_list:
        sim_val = jaro_winkler_similarity(ent, p[0])
        if sim_val == max_val:
            max_list.append([max_val, p])

    return max_list


for ent in data_list:
    log("--------------------------------------------------------------------------------------------")
    api_url = API_URL_PREFIX + urllib.parse.quote_plus(ent) + API_URL_SUFFIX

    log("API URL : " + api_url)

    try:
        query_result = query_api(api_url)
        query_result_xml = xmltodict.parse(query_result)

        parsed_result = parse_result(query_result_xml)

        if len(parsed_result) > 0:
            best_match_list = get_best_match(ent, parsed_result)

            for best_match in best_match_list:
                log("\tBest match for : " + ent + "  =>  " + str(best_match[1][0])
                + " [ " + str(best_match[0]) + " ]")

                csv_writer_1.writerow([ent, best_match[1][0], best_match[1][1], str(best_match[0])])
        else:
            log("\tNo match for : " + ent + " found.")
            if NA_FLAG:
                csv_writer_1.writerow([ent, "", "", "0"])

    except Exception as e:
        log("Error in handling : " + ent)
        print(e)

