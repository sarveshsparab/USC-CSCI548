#!/usr/bin/python

# assumes use of Python 3
import youtube_dl
import pandas as pd
import numpy as np
import json

from tqdm import tqdm
from time import sleep
from random import randint

QUERY_RESULTS_FILE = 'query_output.txt'

def gather_data(clean_links):
    data = dict()
    if len(clean_links) > 0:
        for l in tqdm(clean_links):
            yt_dl = youtube_dl.YoutubeDL({"writedescription": True,
                                              "writeinfojson": True,
                                              "writeannotation": True,
                                              "writesubtitles": True,
                                              "writeautomaticsub": True
                                          })
            try:
                with yt_dl:
                    content = yt_dl.extract_info(url=str(l), download=False)
            except youtube_dl.utils.DownloadError:
                pass
            else:
                video = dict()
                video['url'] = l
                video['title'] = content['title']
                video['description'] = content['description']
                video['created'] = content['upload_date']
                tylt = np.around(np.divide(content['duration'], 60.), 1)
                if tylt % 1 == 0:
                    if tylt != 1.0:
                        video['typical_learning_time'] = str(int(tylt))+' minutes'
                    else:
                        video['typical_learning_time'] = str(int(tylt)) + ' minute'
                else:
                    video['typical_learning_time'] = str(tylt) + ' minutes'
                video['view_count'] = content['view_count']
                video['like_count'] = content['like_count']
                video['dislike_count'] = content['dislike_count']
                if content['requested_subtitles'] is not None:
                    video['transcript'] = content['requested_subtitles']['en']['url']
                else:
                    video['transcript'] = None
                if content['automatic_captions'] is not None and \
                    len(content['automatic_captions']) > 0:
                    #print content['automatic_captions'].keys()
                    video['auto_caption'] = content['automatic_captions']['en'][1]['url']
                else:
                    video['auto_caption'] = None
                video['provider'] = content['uploader']
                if content['uploader_id'] is not None:
                    video['provider_url'] = 'https://www.youtube.com/channel/'+content['uploader_id']
                data[l] = video
                # Small delay to avoid hammering YouTube with requests.
                sleep(randint(2,5))
    return data

if __name__ == '__main__':
    urls = list()
    with open(QUERY_RESULTS_FILE, 'r') as f:
        for line in f:
            urls.append(line.strip())

    data_dict = gather_data(urls)

    with open('youtube-data.json', 'w') as fw:
        json.dump(data_dict, fw, sort_keys=True, indent=4)

