# importing the requests library
import requests
import csv


my_list = []

with open("list.csv") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        name = row[0]
        link = row[1]
        id = link[30:]
        my_list.append(id)

# api-endpoint
URL = "https://aoe4world.com/api/v0/leaderboards/rm_1v1?profile_id="

id_list = []
urls = []

for id in my_list:
    if len(id_list) == 50:
        concat = ''
        first = True
        for sub_id in id_list:
            if not first:
                concat = concat + ','
            first = False
            concat = concat + sub_id
        urls.append(URL+concat)
        id_list =  []
    id_list.append(id)

concat = ''
first = True
for sub_id in id_list:
    if not first:
        concat = concat + ','
    first = False
    concat = concat + sub_id
urls.append(URL+concat)


# location given here
location = "aoe4world"

# defining a params dict for the parameters to be sent to the API
PARAMS = {'address':location}

for sub_url in urls:
    print(sub_url)

# printing the output
print("name,rank,id")

for sub_url in urls:
    # sending get request and saving the response as response object
    r = requests.get(url = sub_url, params = PARAMS)
    # extracting data in json format
    data = r.json()

    for player in data['players']:

        # extracting latitude, longitude and formatted address
        # of the first matching location
        name = player['name']
        id = player['profile_id']
        rank = 0
        if 'rating' in player:
            rank = player['rating']

        info = {}

        info['name'] = name
        info['id'] = id
        info['rank'] = rank

        print("%s,%s,%s"
            %(info['name'], info['rank'], info['id']))
