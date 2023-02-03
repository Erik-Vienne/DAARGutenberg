from django.shortcuts import render

from livre.forms import *

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

    return render(request, 'livre/indexation.html')