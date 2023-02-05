from django.shortcuts import render
from django.utils.datastructures import MultiValueDict

from livre.forms import *

import os
import json
import string
import re

from livre.models import Livre, Index, Mot, Jaccard
# import requests
import time
from datetime import timedelta

from livre.graphs import jaccard


# Create your views here.

def rechercher(request):
    if request.method == 'POST':
        form = RecupereRequeteForm(request.POST)
        if form.is_valid():
            contenu = form.cleaned_data['champ']
            contenuListe = contenu.split()

            listeTotale = []

            for i in contenuListe:
                # mot = Mot.objects.filter(mot=i)
                mot = Mot.objects.filter(mot__regex='^' + i)
                listeIdMot = []
                for j in mot:
                    listeIdMot.append(j.id)

                listeIdMot = list(set(listeIdMot))

                # print("listeidmot ", listeIdMot)
                listeIdLivre = []

                for k in listeIdMot:
                    index = Index.objects.filter(idMot=k)
                    for l in index:
                        listeIdLivre.append(l.idLivre.idLivre)
                        print("listeidLivre ", listeIdLivre)

                # Sinon cas de depart ou pas de correspondance
                if listeTotale != []:
                    listeTotale = list(set(listeTotale) & set(listeIdLivre))
                else:
                    listeTotale = listeIdLivre

            livres = []

            # CreerJaccard()

            # enleve les doublons :
            listeTotale = list(set(listeTotale))
            # print(listeTotale)

            listeTotale = jaccard(listeTotale)

            for m in listeTotale:
                livres.append(Livre.objects.get(pk=m[0]))

            return render(request, 'livre/recherche.html', {'form': form, 'livres': livres})

    else:
        form = RecupereRequeteForm(request.POST)
    return render(request, 'livre/recherche.html', {'form': form, 'contenu': ""})


def exempleDic(request):
    listeMots = []
    for i in range(1):
        listeMots = Mot.objects.filter()
        dic = dict()

        for w in listeMots:
            dic[w.mot] = w.id

    return render(request, 'livre/indexation.html')


def indexer(request):
    if request.method == 'POST':

        # lancer l'indexation

        print("################################")
        mdict = MultiValueDict(request.FILES)
        file_list = mdict.getlist('file_field')
        books = []
        cpt = 1
        total = len(file_list)
        start = time.time()

        jsonname = "jsontoDB.json"

        print("Recherche du json...")
        jsonfile = filter(lambda x: x.name == jsonname, file_list)
        jsonfile = list(jsonfile)

        if jsonfile:
            jsonfile = jsonfile[0]
            print("json trouvé !")
            jsontoDB = open(jsonfile.temporary_file_path())
            jsonBooks = json.loads(jsontoDB.read())
            for book in jsonBooks:
                if 'id' in book.keys() and 'title' in book.keys() and 'author' in book.keys() and 'link' in book.keys():
                    if len(book['author']) == 0:
                        auteur = ""
                    else:
                        auteur = book['author'][0]['name']

                    books.append(Livre(
                        idLivre=book['id'],
                        titre=book['title'],
                        auteur=auteur,
                        lien=book['link'],
                    ))
            Livre.objects.bulk_create(books)
            print("upload des livres ok")
        else:
            print("jsonNotFound")
            messages.info(request, "Le fichier JSON n'a pas été trouvé")
            return render(request, 'livre/indexation.html')

        print("analyse des livres")

        # Récupération de tous les mots sous forme de dictionnaire pour minimiser les appels à la DB
        mots_dict = {}
        for m in Mot.objects.all():
            mots_dict[m.mot] = m

        for file in file_list:
            print("indexation : " + str(file))
            if str(file).endswith('.txt'):
                book = open(file.temporary_file_path(), encoding="utf8", errors='ignore').read()
                tmp = ' '.join(book.splitlines())
                tmp = tmp.translate(str.maketrans('', '', string.punctuation))
                tmp = tmp.replace('"', ' ')
                tmp = tmp.replace('“', ' ')
                tmp = tmp.replace('”', ' ')
                tmp = tmp.replace('’', ' ')

                # enleve tout ce qui n'est pas une lettre, un chiffre ou un espace
                tmp = re.sub(r'[^a-zA-Z0-9\s]+', '', tmp)

                # creation de la liste de mot
                res = tmp.split(' ')

                # les mots sont mis en minuscules.
                res = [x.lower() for x in res]

                # On retire certains des mots les plus courants de la langue anglaise
                motFrequent = ['got', 'gone', 'had', 'such', 'did', 'been', 'were', 'are', 'is', 'the', 'be', 'to',
                               'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he',
                               'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
                               'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so',
                               'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can',
                               'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your',
                               'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only',
                               'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our',
                               'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give',
                               'day', 'most', 'us', 'was']
                for i in motFrequent:
                    res = list(filter(lambda a: a != i, res))

                occ = dict()
                for w in res:
                    if w in occ:
                        occ[w] += 1
                    else:
                        occ[w] = 1

                idlivre = int(str(file).split('-')[0])
                livre = Livre.objects.filter(idLivre=idlivre).first()

                mots = Mot.objects.values_list('mot', flat=True)
                dicMots = dict.fromkeys(mots, None)

                for w in occ.keys():
                    if w not in dicMots:
                        mot = Mot.objects.create(mot=w)
                        dicMots[w] = mot.id
                    else:
                        dicMots[w] = Mot.objects.filter(mot=w)[0].id

                Index.objects.bulk_create([
                    Index(idLivre=livre, idMot_id=dicMots[w], nbOccurrence=occ[w])
                    for w in occ.keys() if w in dicMots
                ])

                print("########## Livre " + str(cpt) + " sur " + str(total-1) + " Ok")
                print("########## Durrée de l'indexation : " + str(timedelta(seconds=(time.time() - start))))
                cpt += 1

            else:
                print("probleme pas un txt : " + str(file))

        print("################################")

    return render(request, 'livre/indexation.html')


def CreerJaccard(request):
    if request.method == 'POST':
        print("debut mot")
        livre = Livre.objects.all()
        nbLivre = len(livre)

        dicIdIndice = dict()
        dicIndiceId = dict()
        indice = 0
        livres = Livre.objects.all()

        # deuxieme element = retenue
        for w in livres:
            dicIdIndice[w.idLivre] = (indice, 0)
            dicIndiceId[indice] = w.idLivre
            indice = indice + 1

        table = [[(0, 0) for x in range(nbLivre)] for y in range(nbLivre)]
        print("table cree")

        compteur = 0

        mot = Mot.objects.all()
        mot = mot[:20000]
        print(mot)
        for i in mot:

            compteur = compteur + 1
            if (compteur % 1000) == 0:
                print(compteur)

            # print(i.id)
            ind = Index.objects.filter(idMot_id=2191187)

            print(ind)
            print(len(ind))

            # print(i.mot, " :" , len(ind) )
            for j in ind:
                livre = Livre.objects.filter(idLivre=j.idLivre_id)
                if len(livre) > 0:
                    livre = livre[0]
                dicIdIndice[j.idLivre_id] = (
                    (dicIdIndice[livre.idLivre])[0], (dicIdIndice[livre.idLivre])[1] + j.nbOccurrence)
                for k in ind:
                    livre2 = Livre.objects.filter(idLivre=k.idLivre_id)
                    if len(livre2) > 0:
                        livre2 = livre2[0]
                    if livre.idLivre != livre2.idLivre:
                        # on enlève j.nbOccurence car on le rajoutera après partout
                        num = table[j][k][0] + max(j.nbOccurrence, k.nbOccurrence) - min(j.nbOccurrence,
                                                                                         k.nbOccurrence) - j.nbOccurrence
                        denom = table[j][k][0] + max(j.nbOccurrence, k.nbOccurrence) - j.nbOccurrence
                        table[j][k] = (num, denom)

                        print(num)
                        print(denom)

        print("fin mot")

        for x in range(nbLivre):
            for y in range(nbLivre):

                # comparaison entre deux idLivre en miroir avec le calcul précédent (la case inverse est vide)
                if dicIndiceId[x] > dicIndiceId[y]:
                    idLivre1 = dicIndiceId[x]
                    idLivre2 = dicIndiceId[y]

                    numerateur = table[x][y][0] + dicIdIndice[idLivre1][1] + dicIdIndice[idLivre2][1]
                    denominateur = table[x][y][1] + dicIdIndice[idLivre1][1] + dicIdIndice[idLivre2][1]
                    Jaccard.objects.create(
                        idLivre1=idLivre1,
                        idLivre2=idLivre2,
                        distance=(numerateur / denominateur)
                    )

        print("fin index jaccard")
        return render(request, 'livre/CreerJaccard.html')
    else:
        return render(request, 'livre/CreerJaccard.html')
