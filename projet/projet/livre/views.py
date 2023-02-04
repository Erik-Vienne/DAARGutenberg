from django.shortcuts import render
from django.utils.datastructures import MultiValueDict

from livre.forms import *

import os
import json
import string
import re

from livre.models import Livre, Index, Mot
# import requests
import time


# Create your views here.


def rechercher(request):
    if request.method == 'POST':
        form = RecupereRequeteForm(request.POST)
        if form.is_valid():
            contenu = form.cleaned_data['champ']
            contenuListe = contenu.split()

            listeTotale = [] 

            for i in contenuListe:
                #mot = Mot.objects.filter(mot=i)
                mot = Mot.objects.filter(mot__regex=i)
                listeIdMot = []
                for j in mot :
                    listeIdMot.append(j.id)
                
                print("listeidmot " ,listeIdMot)
                listeIdLivre = []
                
                for k in listeIdMot :
                    index = Index.objects.filter(idMot=k) 
                    for l in index :
                        listeIdLivre.append(l.idLivre.idLivre)
                        print("listeidLivre " , listeIdLivre)

                # Sinon cas de depart ou pas de correspondance
                if listeTotale != [] :
                    listeTotale = list(set(listeTotale) & set(listeIdLivre))
                else :
                    listeTotale = listeIdLivre


            print(listeTotale)

            livres = []

            for m in listeTotale :
                livres.append(Livre.objects.get(pk = m) )

            return render(request, 'livre/recherche.html', {'form': form, 'contenu': contenu, 'livres': livres})

    else:
        form = RecupereRequeteForm(request.POST)
    return render(request, 'livre/recherche.html', {'form': form, 'contenu': ""})



def exempleDic(request) :
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

        # jsonfile = request.FILES['indexation'].read()
        # print(jsonfile)
        # print(request.FILES.getlist('indexation'))

        print("################################")
        mdict = MultiValueDict(request.FILES)

        #print(mdict.getlist('file_field'))

        for file in mdict.getlist('file_field'):
            if str(file).endswith('.json'):
                jsontoDB = open(file.temporary_file_path())
                jsonBooks = json.loads(jsontoDB.read())
                for book in jsonBooks:
                    if 'id' in book.keys() and 'title' in book.keys() and 'author' in book.keys() and 'link' in book.keys():
                        #if len(Livre.objects.filter(idLivre=book['id'])) == 0:
                            
                        if len(book['author']) == 0 :
                            auteur = ""
                        else:
                            auteur = book['author'][0]['name']

                        Livre.objects.create(
                            idLivre=book['id'],
                            titre=book['title'],
                            auteur= auteur,
                            lien=book['link'],
                        )
                print("upload des livres ok")
                break

        for file in mdict.getlist('file_field'):
            print("indexation : " + str(file))
            if str(file).endswith('.txt'):
                book = open(file.temporary_file_path(), encoding="utf8").read()
                tmp = ' '.join(book.splitlines())
                tmp = tmp.translate(str.maketrans('', '', string.punctuation))
                tmp = tmp.replace('"', ' ')
                tmp = tmp.replace('“', ' ')
                tmp = tmp.replace('”', ' ')

                # enleve tout ce qui n'est pas une lettre, un chiffre ou un espace
                tmp = re.sub(r'[^a-zA-Z0-9\s]+', '', tmp)

                # creation de la liste de mot
                res = tmp.split(' ')

                # les mots sont mis en minuscules.
                res = [x.lower() for x in res]

                # On retire certains des mots les plus courants de la langue anglaise
                motFrequent = ['got', 'gone', 'had', 'such', 'did', 'been', 'were','are', 'is','the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us', 'was']
                for i in motFrequent :
                    res = list(filter(lambda a: a != i, res))

                
                occ = dict()
                for w in res:
                    if w in occ:
                        occ[w] += 1
                    else:
                        occ[w] = 1
                
                

                idlivre = int(str(file).split('-')[0])
                livre = Livre.objects.filter(idLivre=idlivre)[0]

    
                listeMots = Mot.objects.filter()
                dicMots = dict()        
                for w in listeMots:            
                    dicMots[w.mot] = w


                for w in occ.keys():
                    if w not in dicMots:
                        Mot.objects.create(
                            mot=w
                        )

                listeMots = Mot.objects.filter()
                dicMots = dict()        
                for w in listeMots:            
                    dicMots[w.mot] = w

                
                for w in occ.keys():
                    idMot = dicMots[w]

                    Index.objects.create(
                        idLivre=livre,
                        idMot=idMot,
                        nbOccurrence=occ[w],
                    )



                # for w in occ.keys():
                #     if len(Mot.objects.filter(mot=w)) == 0:
                #         #print("Nouveau Mot")
                #         Mot.objects.create(
                #             mot=w
                #         )
                #     #idlivre = int(str(file).split('-')[0])
                #     mot = Mot.objects.filter(mot=w)[0]

                #     #if len(Index.objects.filter(idLivre=livre, idMot=mot)) == 0:
                #         #print("nouvel index")
                #     Index.objects.create(
                #         idLivre=livre,
                #         idMot=mot,
                #         nbOccurrence=occ[w],
                #     )

            else:
                print("probleme pas un txt : " + file)

        print("################################")

    return render(request, 'livre/indexation.html')
