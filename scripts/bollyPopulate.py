import csv
from itertools import islice

import requests

f = open("bollywoodMovie.csv")
reader = csv.reader(f)

last_successful = 0
i = 0
for row in islice(reader, 200, None):
    i += 1
    imdb_ID = row[0]
    imdb_ID = imdb_ID
    r = requests.get("http://localhost:5000/movie/search/id/{}".format(imdb_ID))
    print(str(i) + " : " + str(r.status_code))
    if r.status_code == 200:
        last_successful = imdb_ID
