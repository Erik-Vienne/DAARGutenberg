from django.shortcuts import render

from livre.forms import *


from livre.models import Livre, Index, Mot
#import requests
import time


# Create your views here.


def rechercher(request):
    if request.method == 'POST' :
        form = RecupereRequeteForm(request.POST)
        if form.is_valid() :
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

            return render(request, 'livre/recherche.html', {'form': form, 'contenu':contenu})

    else:
        form = RecupereRequeteForm(request.POST)
    return render(request, 'livre/recherche.html', {'form' : form, 'contenu': ""})




def indexer(request):
    if request.method == 'POST' :        
        print("coucou")
        # lancer l'indexation

        Livre.objects.create(
                idLivre = 12,
                titre = "blabla",
                auteur = "blabla",
                lien = "blabla",
            )

    return render(request, 'livre/indexation.html')