import pathlib
import requests
import os

file = open("links.txt", "r")


for line in file.read().splitlines():

    file, link = line.split("\0")

    if os.path.isfile(file):
        continue

    print(file)

    pathlib.Path(file[:file.rfind("/")]).mkdir(parents=True, exist_ok=True)

    while True:
        try:
            response = requests.get(link, stream=True, timeout=5)

            with open(file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            break
        except:
            print("!", end="", flush=True)
            continue

