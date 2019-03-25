from django.shortcuts import render
from calculdej.models import Categorie
from calculdej.models import Activite
from calculdej.models import Dossier
from calculdej.models import Travail
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test

from django.http import HttpResponse
import csv


def check_user(user):
    if user.is_authenticated:
        username = user.get_username()

    return username=='admin'

@login_required
@user_passes_test(check_user)
def consultertouslesdossiers(request):
    dossiers = Dossier.objects.all()

    if request.method == 'POST' and 'btnaffdetails' in request.POST:
        id_dossier = int(request.POST.get('btnaffdetails'))
        dossier = Dossier.objects.get(id=id_dossier)
        auteur = dossier.auteur
        date = dossier.date
        taille = dossier.taille
        poids = dossier.poids
        if taille > 0:
            imc = round((poids/((taille/100)*(taille/100))),2)
        else:
            imc = 0
        pathologie = dossier.pathologie
        de = dossier.de

    return render(request, 'consultertouslesdossiers/consultertouslesdossiers.html', locals())


@login_required
@user_passes_test(check_user)
def downloadcsv(request):
    dossiers = Dossier.objects.all()

    tabDossiers = [['Poids (en kg)', 'Taille (en cm)', 'Age','Pathologie','DEJ']]

    # with open('stockitems_misuper.csv', 'wb') as myfile:  # python 3: open('stockitems_misuper.csv', 'w', newline="")
    #     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #     wr.writerows(file_rows)

    # On passe toutes les caractéristiques des dossiers dans le tableau tabDossiers
    for dossier in dossiers:
        row = []
        row.append(dossier.poids)
        row.append(dossier.taille)
        row.append(dossier.age)
        row.append(dossier.pathologie)
        row.append(dossier.de)

        tabDossiers.append(row)

    csv.register_dialect('myDialect',
    delimiter = ';',
    quoting=csv.QUOTE_NONE,
    skipinitialspace=True)

    with open('stats.csv', 'w') as f:
        writer = csv.writer(f, dialect='myDialect')
        for row in tabDossiers:
            writer.writerow(row)

    with open('stats.csv') as myfile:
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=stats.csv'
        return response
