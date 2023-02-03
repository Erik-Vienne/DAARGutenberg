import asyncio
import aiohttp
import os
import json

TOTAL_BOOKS = 1664

jsontoDB = []


async def download_book(book_id, semaphore):
    if len(os.listdir("books/")) >= TOTAL_BOOKS:
        print("Le nombre de livre attendu à été atteint !")
        return

    async with semaphore:
        async with aiohttp.ClientSession() as session:
            url = "http://gutendex.com/books/?language=en&min_words=10000&page={}".format(book_id)
            print("Dumping page", book_id)
            async with session.get(url) as response:
                if response.status == 200:
                    response_text = await response.text()
                    if response_text:
                        book_info = json.loads(response_text)
                        for book in book_info['results']:
                            title = str(str(book['id']) + "-" + book['title'])
                            title = title.replace(' ', '_')
                            if not os.path.exists("books/" + title + ".txt") and (
                                    'text/plain' in book['formats'].keys()) and len(title) <= 249:
                                dl_url = book['formats']['text/plain']

                                currentBook = {
                                    'title': book['title'],
                                    'id': book['id'],
                                    'link': "https://www.gutenberg.org/ebooks/" + str(book['id']),
                                    'author': book['authors']
                                }
                                jsontoDB.append(currentBook)

                                async with session.get(dl_url) as download_response:
                                    if download_response.status == 200:
                                        content = await download_response.read()
                                        book_path = os.path.join("books", "{}.txt".format(title))
                                        with open(book_path, "wb") as f:
                                            f.write(content)
                                        print(f"Livre {title} téléchargé avec succès dans le dossier books.")
                                    else:
                                        print(
                                            f"Echec du téléchargement du livre {title}, veuillez vérifier votre connexion internet ou l'ID du livre.")
                    else:
                        print(f"Réponse vide pour le livre {book_id}.")
                else:
                    print(f"Echec de la récupération des informations du livre {book_id}.")


async def main():
    semaphore = asyncio.Semaphore(5)
    os.makedirs("books", exist_ok=True)
    tasks = [download_book(book_id, semaphore) for book_id in range(1, 2)]
    await asyncio.gather(*tasks)


asyncio.run(main())

with open("books/jsontoDB.json", "w") as res:
    json.dump(jsontoDB, res, indent=3)
