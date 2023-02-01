
from django import forms




class RecupereRequeteForm(forms.Form):
    champ = forms.CharField(label='Entrez votre requête', max_length=200)