from django.shortcuts import render
from calculdej.models import Categorie
from calculdej.models import Activite
from calculdej.models import Dossier
from calculdej.models import Travail
from django.contrib.auth.decorators import login_required

@login_required
def consulterdossier(request):

    dossiers = Dossier.objects.filter(auteur=request.user)
    return render(request, 'consulterdossier/consulterdossier.html', locals())
