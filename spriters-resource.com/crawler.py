import requests
import bs4
import os

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

URL = "https://www.spriters-resource.com"


def get_consoles():

    consoles = []

    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    for console in soup.find(id="leftnav-consoles"):
        if type(console) == bs4.element.Tag and console.get("href") is not None:
            consoles.append((console.text, URL + console.get("href")))

    return consoles


def get_games(console, letter):

    games = []

    print(console[0] + " - " + letter)

    print(console[1] + letter + ".html")
    response = requests.get(console[1] + letter + ".html")
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a"):
        for child in link.findChildren():
            if child.get("class") is not None and child.get("class") == ['gameiconcontainer']:
                game_name = child.find("div").find("span").string

                games.append((game_name, URL + link.get("href")))

    return games


def get_sheets(game):

    sheets = []

    response = requests.get(game[1])
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a"):

        for div in link.find_all("div"):
            if div.get("class") == ["iconcontainer"]:

                sheet_url = div.find("div", attrs={"class": "iconbody"}).find("img").get("src").replace("sheet_icons",
                                                                                                        "sheets")
                sheet_name = div.find("div").find("span").string
                sheets.append((sheet_name, URL + sheet_url))

    return sheets

file = open("links.txt", "w")

for console in get_consoles():
    for letter in "0ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        for game in get_games(console, letter):
            for sheet in get_sheets(game):

                extension = os.path.splitext(sheet[1])[1]

                file.write(console[0] + os.sep + game[0] + os.sep + sheet[0] + extension + "\0" + sheet[1] + "\n")


file.close()