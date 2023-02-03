from django.urls import path

from . import views

app_name = 'livre'

urlpatterns = [ 

    path('recherche/', views.rechercher, name='recherche'),
    path('rechercheAvancee/', views.rechercher, name='rechercheAvancee'),

    path('indexation/', views.indexer, name='indexation'),







]