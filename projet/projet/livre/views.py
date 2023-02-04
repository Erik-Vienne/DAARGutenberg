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
                        if len(Livre.objects.filter(idLivre=book['id'])) == 0:
                            
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
            if str(file).endswith('.txt'):
                book = open(file.temporary_file_path()).read()
                tmp = ' '.join(book.splitlines())
                tmp = tmp.translate(str.maketrans('', '', string.punctuation))
                tmp = tmp.replace('"', ' ')
                tmp = tmp.replace('“', ' ')
                tmp = tmp.replace('”', ' ')
                res = tmp.split(' ')
                occ = dict()
                for w in res:
                    if w in occ:
                        occ[w] += 1
                    else:
                        occ[w] = 1
                for w in occ.keys():
                    if len(Mot.objects.filter(mot=w)) == 0:
                        print("Nouveau Mot")
                        Mot.objects.create(
                            mot=w
                        )
                    idlivre = int(str(file).split('-')[0])
                    livre = Livre.objects.filter(idLivre=idlivre)[0]

                    mot = Mot.objects.filter(mot=w)[0]

                    if len(Index.objects.filter(idLivre=livre, idMot=mot)) == 0:
                        print("nouvel index")
                        Index.objects.create(
                            idLivre=livre,
                            idMot=mot,
                            nbOccurrence=occ[w],
                        )

            else:
                print("probleme pas un txt : " + file)

        print("################################")

    return render(request, 'livre/indexation.html')
