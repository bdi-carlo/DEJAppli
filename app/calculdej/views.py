from .forms import CalculDejForm, DeplacementForm, CalculMBForm
# from .forms import CalculDejForm, SupprimerForm, CalculImcForm, ValideForm
from calculdej.models import Categorie
from calculdej.models import Activite
from calculdej.models import Dossier
from calculdej.models import Travail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from decimal import Decimal

poids = 0
taille = 0
sexe = "M"
age = 0

@login_required
def calculdej(request):
    return render(request, 'calculdej/calculdej.html')

@login_required
def calculdejmb(request):
    global poids
    global taille
    global sexe
    global age

    formImc = CalculMBForm(request.POST or None)
    if request.method == 'POST' and 'btnsuivantt' in request.POST:
        if formImc.is_valid():
            poids = formImc.cleaned_data['poids']
            taille = formImc.cleaned_data['taille']
            sexe = formImc.cleaned_data['sexe']
            age = formImc.cleaned_data['age']
            return redirect(reverse(calculdejprofessionnelle))

    return render(request, 'calculdej/calculdejmb.html', locals())


@login_required
def calculdejprofessionnelle(request):
    formDej = CalculDejForm(request.POST or None)
    formDeplacement = DeplacementForm(request.POST or None)
    formDej.CatProfessionnelles()
    cat = None
    dossier = Dossier.objects.filter(dernier=True)
    if dossier:
        dossier = dossier.reverse()[0]
    else:
        dossier = Dossier.objects.create(auteur=request.user,dernier=True)
    if dossier.dernier != True:
        dossier = Dossier.objects.create(auteur=request.user,dernier=True)

    if request.method == 'POST' and 'btnajouter' in request.POST:
        if formDej.is_valid():
            cat = formDej.cleaned_data['cat']
            act = formDej.cleaned_data['act']
            duree = formDej.cleaned_data['duree']
            coef_act = act.coef
            dp = duree * coef_act
            Travail.objects.create(dossierTrav=dossier,categorieTrav=cat,activiteTrav=act,dureeTrav=duree)
            envoi = True
    elif request.method == 'POST' and 'btnenvoyer' in request.POST:
        dossier.dernier=False
        dossier.save()

    elif request.method == 'POST' and 'btnsupprimer' in request.POST:
        id_supp = int(request.POST.get('btnsupprimer'))
        Travail.objects.get(id=id_supp).delete()
        return HttpResponseRedirect(request.path_info)

    travails = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Professionnelles')
    return render(request, 'calculdej/calcdejprofessionnelle.html', locals())


@login_required
def calculdejusuelle(request):
    formDej = CalculDejForm(request.POST or None)
    formDej.CatUsuelles()
    cat = None
    dossier = Dossier.objects.filter(dernier=True)
    if dossier:
        dossier = dossier.reverse()[0]
    else:
        dossier = Dossier.objects.create(auteur=request.user,dernier=True)
    if dossier.dernier != True:
        dossier = Dossier.objects.create(auteur=request.user,dernier=True)

    if request.method == 'POST' and 'btnajouter' in request.POST:
        if formDej.is_valid():
            cat = formDej.cleaned_data['cat']
            act = formDej.cleaned_data['act']
            duree = formDej.cleaned_data['duree']
            coef_act = act.coef
            dp = duree * coef_act
            Travail.objects.create(dossierTrav=dossier,categorieTrav=cat,activiteTrav=act,dureeTrav=duree)
            envoi = True
    elif request.method == 'POST' and 'btnenvoyer' in request.POST:
        dossier.dernier=False
        dossier.save()

    elif request.method == 'POST' and 'btnsupprimer' in request.POST:
        id_supp = int(request.POST.get('btnsupprimer'))
        Travail.objects.get(id=id_supp).delete()
        return HttpResponseRedirect(request.path_info)

    travails = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Usuelles')
    return render(request, 'calculdej/calcdejusuelle.html', locals())

@login_required
def calculdejloisir(request):
    formDej = CalculDejForm(request.POST or None)
    formDej.CatLoisirs()
    dossier = Dossier.objects.filter(dernier=True)
    cat = None
    if dossier:
        dossier = dossier.reverse()[0]
    else:
        dossier = Dossier.objects.create(auteur=request.user,dernier=True)
    if dossier.dernier != True:
        dossier = Dossier.objects.create(auteur=request.user,dernier=True)

    if request.method == 'POST' and 'btnajouter' in request.POST:
        if formDej.is_valid():
            cat = formDej.cleaned_data['cat']
            act = formDej.cleaned_data['act']
            duree = formDej.cleaned_data['duree']
            coef_act = act.coef
            dp = duree * coef_act
            Travail.objects.create(dossierTrav=dossier,categorieTrav=cat,activiteTrav=act,dureeTrav=duree)
            envoi = True
    elif request.method == 'POST' and 'btnenvoyer' in request.POST:
        dossier.dernier=False
        dossier.save()

    elif request.method == 'POST' and 'btnsupprimer' in request.POST:
        id_supp = int(request.POST.get('btnsupprimer'))
        Travail.objects.get(id=id_supp).delete()
        return HttpResponseRedirect(request.path_info)

    travails = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Loisirs')
    return render(request, 'calculdej/calcdejloisir.html', locals())

@login_required
def calculdejsport(request):
    formDej = CalculDejForm(request.POST or None)
    formDej.CatSportives()
    cat = None
    dossier = Dossier.objects.filter(dernier=True)
    if dossier:
        dossier = dossier.reverse()[0]
    else:
        dossier = Dossier.objects.create(auteur=request.user,dernier=True)
    if dossier.dernier != True:
        dossier = Dossier.objects.create(auteur=request.user,dernier=True)

    if request.method == 'POST' and 'btnajouter' in request.POST:
        if formDej.is_valid():
            cat = formDej.cleaned_data['cat']
            act = formDej.cleaned_data['act']
            duree = formDej.cleaned_data['duree']
            coef_act = act.coef
            dp = duree * coef_act
            Travail.objects.create(dossierTrav=dossier,categorieTrav=cat,activiteTrav=act,dureeTrav=duree)
            envoi = True
    elif request.method == 'POST' and 'btnterminer' in request.POST:
        # dossier.dernier=False
        # dossier.save()
        # return render(request, 'calculdej/calculdejresultat.html', locals())
        return calculdejresultat(request)

    elif request.method == 'POST' and 'btnsupprimer' in request.POST:
        id_supp = int(request.POST.get('btnsupprimer'))
        Travail.objects.get(id=id_supp).delete()
        return HttpResponseRedirect(request.path_info)

    travails = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Sportives')
    return render(request, 'calculdej/calcdejsport.html', locals())

# Calcul d'une DE en fonction d'une Catégorie et de sa liste d'Activités
def calculDE( cat, activites, MB, TD ):
    dureeNap = 0
    sommeNap = 0
    for tmp in activites:
        if cat == "Professionnelles" or cat == "Usuelles":
            dureeNap += tmp.dureeTrav
            sommeNap += tmp.dureeTrav * tmp.activiteTrav.coef
        if cat == "Loisirs" or cat == "Sportives":
            dureeNap += tmp.dureeTrav/7
            sommeNap += tmp.dureeTrav/7 * tmp.activiteTrav.coef
    if dureeNap == 0:
        return 0
    else:
        nap = sommeNap / dureeNap
        return float(nap) * float(MB) / float(TD) * float(dureeNap)

@login_required
def calculdejresultat(request):
    global poids
    global taille
    global sexe
    global age

    MB = 0 # Métabolisme de Base
    TD = 0 # Temps total
    imc = round((poids/((taille/100)*(taille/100))),2)

    # Récupération du dossier en cours et sauvegarde de celui-ci
    dossier = Dossier.objects.filter(dernier=True)
    if dossier:
        dossier = dossier.reverse()[0]
    else:
        dossier = Dossier.objects.create(auteur=request.user,dernier=True)
    if dossier.dernier != True:
        dossier = Dossier.objects.create(auteur=request.user,dernier=True)

    dossier.save()

    travails = Travail.objects.filter(dossierTrav=dossier)

    pros = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Professionnelles')
    sports = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Sportives')
    usuelles = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Usuelles')
    loisirs = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Loisirs')

    # Calcul du Métabolisme de Base
    if sexe == "M":
        MB = 13.707*float(poids)+492.3*(float(taille)/100)-6.673*int(age)+77.607
        naj1 = 2.5
        naj2 = 5.0
        naj3 = 7.5
    else:
        MB = 9.740*float(poids)+172.9*(float(taille)/100)-4.737*int(age)+667.051
        naj1 = 2.0
        naj2 = 4.6
        naj3 = 6.0

    # Calcul Durée Totale
    for tmp in travails:
        test = False
        for cat in Categorie.objects.filter(typeCat="Sportives"):
            if tmp.categorieTrav == cat:
                test = True
        for cat in Categorie.objects.filter(typeCat="Loisirs"):
            if tmp.categorieTrav == cat:
                test = True
        if test:
            TD += tmp.dureeTrav/7
        else:
            TD += tmp.dureeTrav

    # Calcul DE Professionnelles
    DEProfessionnelles = calculDE( "Professionnelles", pros, MB, TD )

    # Calcul DE Usuelles
    DEUsuelles = calculDE( "Usuelles", usuelles, MB, TD )

    # Calcul DE Loisirs
    DELoisirs = calculDE( "Loisirs", loisirs, MB, TD )

    # Calcul DE Sportives
    DESports = calculDE( "Sportives", sports, MB, TD )

    # Calcul DE Totale
    DE = round(((DEProfessionnelles+DEUsuelles+DELoisirs+DESports)/24/60),2)

    # Détermination du niveau d'activité journalière
    if DE < naj1:
        niveau = "faible"
    elif DE < naj2:
        niveau = "modéré"
    elif DE < naj3:
        niveau = "intense"
    else:
        niveau = "très intense"

    # Enregistrement des informations dans le dossier
    dossier = Dossier.objects.filter(dernier=True).reverse()[0]
    dossier.imc = imc
    dossier.age = age
    dossier.sexe = sexe
    dossier.de = DE

    dossier.dernier=False
    dossier.save()

    return render(request, 'calculdej/calculdejresultat.html', locals())


@login_required
def load_act(request):
    cat_d = request.GET.get('cat')
    acts = Activite.objects.filter(categorie=cat_d)
    return render(request, 'calculdej/acts.html',locals())
