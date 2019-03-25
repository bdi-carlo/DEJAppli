from django.shortcuts import render
from calculdej.models import Categorie
from calculdej.models import Activite
from calculdej.models import Dossier
from calculdej.models import Travail
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
# @user_passes_test(check_user)
def consulterdossier(request):
    dossiers = Dossier.objects.filter(auteur=request.user)

    if request.method == 'POST' and 'btnaffdetails' in request.POST:
        id_dossier = int(request.POST.get('btnaffdetails'))
        dossier = Dossier.objects.get(id=id_dossier)
        date = dossier.date
        taille = dossier.taille
        poids = dossier.poids
        if taille > 0:
            imc = round((poids/((taille/100)*(taille/100))),2)
        else:
            imc = 0
        pathologie = dossier.pathologie
        de = dossier.de

    return render(request, 'consulterdossier/consulterdossier.html', locals())
