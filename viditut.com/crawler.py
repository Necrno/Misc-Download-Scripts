import requests
import bs4
import json

URL = "https://viditut.com"

# https://viditut.com/ajax/course/573135/675578/play

def get_categories():

    categories = []

    r = requests.get(URL)
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    for i in soup.find_all("i"):
        if i.get("class") is not None and len(i.get("class")) > 1 and "cat-" in i.get("class")[1]:
            category_id = i.get("class")[1][4:]
            category_name = i.get("title")[:i.get("title").find("-") - 1]

            categories.append((category_name, category_id))

    return categories


def get_courses(category):
    last_len = 0
    courses = []
    page = 0
    while True:

        page += 1
        r = requests.get("https://viditut.com/ajax/category/" + category[1] + "/courses?page=" + str(page))
        soup = bs4.BeautifulSoup(json.loads(r.text)["html"], "html.parser")

        for link in soup.find_all("a"):
            if link.get("href") is not None:
                if link.find("h3") is not None:
                    course_link = link.get("href")
                    course_name = link.find("h3").string
                    course_id = course_link.split("/")[-1:][0][:-7]

                    courses.append((course_name, course_id, course_link))

        print("Page " + str(page) + " (" + str(len(courses)) + ")")

        if last_len == len(courses):
            break

        last_len = len(courses)

    return courses


def get_videos(course):

    videos = []
    r = requests.get(course[2])
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    for link in soup.find_all("a"):

        if link.get("class") is not None and str(link.get("class")) == "['item-name', 'video-name', 'ga']":
            video_id = link.get("data-ga-value")
            video_name = link.text.strip()

            videos.append((video_name, video_id))

    return videos


def get_links(course, video):

    links = []
    r = requests.get("https://viditut.com/ajax/course/" + course[1] + "/" + video[1] + "/play")
    json_obj = json.loads(r.text)[0]

    for quality in json_obj["qualities"]:
        links.append((quality, json_obj["urls"][quality]))

    return links


file = open("links.txt", "w")

for category in get_categories():
    print(category)
    for course in get_courses(category):

        print(course[0])

        for video in get_videos(course):
            for link in get_links(course, video):
                file.write(category[0] + "/" + course[0] + "/" + video[0] + "\0" + link[0] + "\0" + link[1] + "\n")


file.close()