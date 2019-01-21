from django.shortcuts import render
from .forms import CalculDejForm, CalculImcForm, ValideForm
from calculdej.models import Categorie
from calculdej.models import Activite
from calculdej.models import Dossier
from calculdej.models import Travail
from django.contrib.auth.decorators import login_required

@login_required
def calculdej(request):
    return render(request, 'calculdej/calculdej.html')

@login_required
def calculdejprofessionnelle(request):
    formDej = CalculDejForm(request.POST or None)
    formDej.CatProfessionnelles()
    dossier = Dossier.objects.filter(dernier=True)
    if dossier:
        dossier = dossier.reverse()[0]
    else:
        dossier = Dossier.objects.create(titre="ttt",auteur=request.user,dernier=True)
    if dossier.dernier != True:
        dossier = Dossier.objects.create(titre="ttt",auteur=request.user,dernier=True)

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

    travails = Travail.objects.filter(dossierTrav=dossier)
    return render(request, 'calculdej/calcdejprofessionnelle.html', locals())


@login_required
def calculdejusuelle(request):
    formDej = CalculDejForm(request.POST or None)
    formDej.CatUsuelles()
    dossier = Dossier.objects.filter(dernier=True)
    if dossier:
        dossier = dossier.reverse()[0]
    else:
        dossier = Dossier.objects.create(titre="ttt",auteur=request.user,dernier=True)
    if dossier.dernier != True:
        dossier = Dossier.objects.create(titre="ttt",auteur=request.user,dernier=True)

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

    travails = Travail.objects.filter(dossierTrav=dossier)
    return render(request, 'calculdej/calcdejusuelle.html', locals())

@login_required
def calculdejloisir(request):
    formDej = CalculDejForm(request.POST or None)
    formDej.CatLoisirs()
    dossier = Dossier.objects.filter(dernier=True)
    if dossier:
        dossier = dossier.reverse()[0]
    else:
        dossier = Dossier.objects.create(titre="ttt",auteur=request.user,dernier=True)
    if dossier.dernier != True:
        dossier = Dossier.objects.create(titre="ttt",auteur=request.user,dernier=True)

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

    travails = Travail.objects.filter(dossierTrav=dossier)
    return render(request, 'calculdej/calcdejloisir.html', locals())

@login_required
def calculdejsport(request):
    formDej = CalculDejForm(request.POST or None)
    formDej.CatSportives()
    dossier = Dossier.objects.filter(dernier=True)
    if dossier:
        dossier = dossier.reverse()[0]
    else:
        dossier = Dossier.objects.create(titre="ttt",auteur=request.user,dernier=True)
    if dossier.dernier != True:
        dossier = Dossier.objects.create(titre="ttt",auteur=request.user,dernier=True)

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

    travails = Travail.objects.filter(dossierTrav=dossier)
    return render(request, 'calculdej/calcdejsport.html', locals())

@login_required
def calculdejresultat(request):
    return render(request, 'calculdej/calculdejresultat.html')


@login_required
def load_act(request):
    cat_d = request.GET.get('cat')
    acts = Activite.objects.filter(categorie=cat_d)
    return render(request, 'calculdej/acts.html',locals())
