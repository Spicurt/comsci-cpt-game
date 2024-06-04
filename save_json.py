import json

data = {
    "Highscore" : 1000,
    "Chips" : 1000
}

with open('test_data.txt', 'w') as test_file:
    json.dump(data, test_file)