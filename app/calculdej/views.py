from django.shortcuts import render
from .forms import CalculDejForm, SupprimerForm, CalculImcForm
# from .forms import CalculDejForm, SupprimerForm, CalculImcForm, ValideForm
from calculdej.models import Categorie
from calculdej.models import Activite
from calculdej.models import Dossier
from calculdej.models import Travail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

@login_required
def calculdej(request):
    return render(request, 'calculdej/calculdej.html')

@login_required
def calculdejimc(request):
    formImc = CalculImcForm(request.POST or None)
    if request.method == 'POST' and 'btncalcul' in request.POST:
        if formImc.is_valid():
            poids = formImc.cleaned_data['poids']
            taille = formImc.cleaned_data['taille']
            imc = round(poids/(taille*taille),2)
    return render(request, 'calculdej/calculdejimc.html', locals())


@login_required
def calculdejprofessionnelle(request):
    formDej = CalculDejForm(request.POST or None)
    formSupp = SupprimerForm(request.POST or None)
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


@login_required
def calculdejresultat(request):
    dossier = Dossier.objects.filter(dernier=True)
    if dossier:
        dossier = dossier.reverse()[0]
    else:
        dossier = Dossier.objects.create(auteur=request.user,dernier=True)
    if dossier.dernier != True:
        dossier = Dossier.objects.create(auteur=request.user,dernier=True)
    dossier.dernier=False
    dossier.save()
    travails = Travail.objects.filter(dossierTrav=dossier)
    return render(request, 'calculdej/calculdejresultat.html', locals())


@login_required
def load_act(request):
    cat_d = request.GET.get('cat')
    acts = Activite.objects.filter(categorie=cat_d)
    return render(request, 'calculdej/acts.html',locals())
