import csv
from itertools import islice

import requests

f = open("ids1.csv")
reader = csv.reader(f)

i = 0
last_successful = 0
for row in islice(reader, 0, None):
    i += 1
    imdb_ID = row[0]
    r = requests.get(
        "http://localhost:5000/movie/search/id/{}".format(imdb_ID))
    print(str(i) + " : " + str(r.status_code))
    if r.status_code == 200:
        last_successful = imdb_ID
