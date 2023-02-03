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