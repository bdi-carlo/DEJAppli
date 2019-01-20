from django.urls import path
from . import views

urlpatterns = [
    path('', views.connexion, name='connexion'),
    path('deconnexion', views.deconnexion, name='deconnexion'),
    path('creercompte', views.creercompte, name='creercompte'),
]
