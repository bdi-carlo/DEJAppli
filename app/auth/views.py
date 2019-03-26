from django.shortcuts import render, redirect
from .forms import ConnexionForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from calculdej.models import Dossier

def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                # return HttpResponseRedirect("/imc/")
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    dossier = Dossier.objects.filter(dernier=True)
    if dossier:
        Dossier.objects.filter(dernier=True).delete()

    return render(request, 'connexion.html', locals())

def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))


def creercompte(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('/')

    else:
        f = CustomUserCreationForm()

    return render(request, 'creercompte.html', {'form': f})
