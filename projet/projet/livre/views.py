from django.shortcuts import render

from livre.forms import *

import os
import json

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

            return render(request, 'livre/recherche.html', {'form': form, 'contenu': contenu})

    else:
        form = RecupereRequeteForm(request.POST)
    return render(request, 'livre/recherche.html', {'form': form, 'contenu': ""})


def indexer(request):
    if request.method == 'POST':
        print("coucou")
        # lancer l'indexation

        print("################################")
        jsonfile = request.FILES['DB_jsonfile'].read()
        # jsonfile = jsonfile.decode('utf-8')
        jsonBooks = json.loads(jsonfile)
        for book in jsonBooks:
            if 'id' in book.keys() and 'title' in book.keys() and 'author' in book.keys() and 'link' in book.keys():
                Livre.objects.create(
                    idLivre=book['id'],
                    titre=book['title'],
                    auteur=book['author'][0]['name'],
                    lien=book['link'],
                )

        print("################################")
    return render(request, 'livre/indexation.html')
