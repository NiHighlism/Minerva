import csv
from itertools import islice

import requests

f = open("links.csv")
reader = csv.reader(f)

last_successful = 0
for row in islice(reader, 5705, None):
    imdb_ID = row[1]
    imdb_ID = "tt" + imdb_ID
    r = requests.get(
        "http://localhost:5000/movie/search/id/{}".format(imdb_ID))
    print(r.status_code)
    if r.status_code == 200:
        last_successful = imdb_ID
