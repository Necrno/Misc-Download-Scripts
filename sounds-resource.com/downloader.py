import pathlib
import requests
import os

file = open("links.txt", "r")


for line in file.read().splitlines():

    path, link = line.split("\0")

    print("sounds/" + path)

    pathlib.Path("sounds/" + path).mkdir(parents=True, exist_ok=True)

    while True:
        try:
            response = requests.get(link, stream=True, timeout=5)

            file_extension = os.path.splitext(response.headers["Content-Disposition"])[1][:-2]

            with open("sounds/" + path + path.split("/")[-2:-1][0] + file_extension, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            break
        except:
            print("!", end="", flush=True)
            continue