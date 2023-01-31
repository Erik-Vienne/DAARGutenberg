import asyncio
import os
import urllib.request
import requests

MIN_WORDS = 10000

NB_BOOKS = 1664

DUMP_URL = "https://gutendex.com/books/?page="

DL_PATH = "books/"


def makeBooksDir():
    if not os.path.isdir("books"):
        os.makedirs("books")


def countBooks(dir):
    cpt = 0
    for path in os.listdir(dir):
        if os.path.isfile(path):
            cpt += 1
    return cpt


def getBooksFromUrl(url):
    return requests.get(url).json()


def getBooks(url):
    jsonResponse = getBooksFromUrl(url)
    if "results" in jsonResponse:
        return jsonResponse["results"]


def getBook(url, id):
    json = getBooks(url)[id]
    if "formats" in json:
        if "text/plain" in json["formats"]:
            return json["formats"]["text/plain"]


def saveTxtFile(path, url, name):
    urllib.request.urlretrieve(str(url), path + str(name) + ".txt")


def countWords(url, id):
    text = getBook(url, id)
    if text is not None:
        res = requests.get(text)
        strtext = res.text
        return len(strtext.split())
    else:
        print(text)
        return -1


async def downloadTxtFiles(url, gutenpage):
    cpt = 0
    index = 0
    page = gutenpage
    url = url + str(page)
    try:
        books = getBooks(url)
        for book in books:
            if index < len(books):
                # if len(book["title"]) < 255:
                title = book["title"]
                # else:
                #     title = book["id"]
                nbwords = countWords(url, index)
                print("Book : " + str(title) + " has ", nbwords, " words")
                if nbwords >= MIN_WORDS:
                    saveTxtFile(DL_PATH, getBook(url, index), title)
                    index += 1
                    cpt += 1
            index += 1
        print("Page : " + str(page))
        print("nbBooks : ", cpt)
    except:
        print("error while retrieving books, please check the url")


makeBooksDir()
i = 123

print("Dumping Gutendex....")
while countBooks(DL_PATH) < NB_BOOKS:
    asyncio.run(downloadTxtFiles(DUMP_URL, i))
    print("There is : " + str(countBooks(DL_PATH)) + " downloaded from url page ", i)
    i += 1

print("Gutendex Dumped :)")
