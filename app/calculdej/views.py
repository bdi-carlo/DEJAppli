from .forms import CalculDejForm, DeplacementForm, CalculMBForm
# from .forms import CalculDejForm, SupprimerForm, CalculImcForm, ValideForm
from calculdej.models import Categorie
from calculdej.models import Activite
from calculdej.models import Dossier
from calculdej.models import Travail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from decimal import Decimal
from weasyprint import HTML, CSS
from django.conf import settings
import os
from django.template.loader import render_to_string

poids = 0
taille = 0
sexe = "M"
age = 0
pathologie = ""

deplacements = []

@login_required
def calculdej(request):
    return render(request, 'calculdej/calculdej.html')

@login_required
def calculdejmb(request):
    global poids
    global taille
    global sexe
    global age
    global pathologie

    quitter1 = False
    if request.method == 'GET':
        a = request.GET.get('calculdejprofessionnelle')
        b = request.GET.get('calculdejusuelle')
        c = request.GET.get('calculdejloisir')
        d = request.GET.get('calculdejsport')
        if a is None:
            quitter1 = True
        if b is None:
            quitter1 = True
        if c is None:
            quitter1 = True
        if d is None:
            quitter1 = True

    formImc = CalculMBForm(request.POST or None)
    if request.method == 'POST' and 'btnsuivantt' in request.POST:
        if formImc.is_valid():
            poids = formImc.cleaned_data['poids']
            taille = formImc.cleaned_data['taille']
            sexe = formImc.cleaned_data['sexe']
            age = formImc.cleaned_data['age']
            pathologie = formImc.cleaned_data['pathologie']
            return redirect(reverse(calculdejprofessionnelle))

    return render(request, 'calculdej/calculdejmb.html', locals())


@login_required
def alertmsg(request):
    return render(request, 'calculdej/alertmsg.html', locals())

def calculDureeTotale( travails ):
    # Calcul Durée Totale
    duree = 0
    for tmp in travails:
        test = False
        for cat in Categorie.objects.filter(typeCat="Sportives"):
            if tmp.categorieTrav == cat:
                test = True
        for cat in Categorie.objects.filter(typeCat="Loisirs"):
            if tmp.categorieTrav == cat:
                test = True
        if test:
            duree += tmp.dureeTrav/7
        else:
            duree += tmp.dureeTrav

    return round(duree, 2)

@login_required
def calculdejprofessionnelle(request):
    global deplacements

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

    if request.method == 'POST' and 'btnsuivant' in request.POST:
        if formDej.is_valid() and formDeplacement.is_valid():
            cat = formDej.cleaned_data['cat']
            act = formDej.cleaned_data['act']
            duree = formDej.cleaned_data['duree']
            coef_act = act.coef
            dp = duree * coef_act
            Travail.objects.create(dossierTrav=dossier,categorieTrav=cat,activiteTrav=act,dureeTrav=duree,coefTrav=coef_act)
            # envoi = True
            if 'rdouinon' in request.POST:
                valrd = str(request.POST.get('rdouinon'))
                if valrd == "Oui":
                    deplacements.append(float(formDeplacement.cleaned_data['dureelentsansport']))
                    deplacements.append(float(formDeplacement.cleaned_data['dureemoderesansport']))
                    deplacements.append(float(formDeplacement.cleaned_data['dureemodereavecport']))
                    deplacements.append(float(formDeplacement.cleaned_data['dureeintense']))
                elif valrd == "Non":
                    deplacements = [0,0,0,0]

            return redirect(reverse(calculdejusuelle))

    travails = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Professionnelles')

    return render(request, 'calculdej/calcdejprofessionnelle.html', locals())


@login_required
def calculdejusuelle(request):

    quitter = False
    if request.method == 'GET' and (not ('btnsuivant' in request.GET)):
        quitter = True

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
            Travail.objects.create(dossierTrav=dossier,categorieTrav=cat,activiteTrav=act,dureeTrav=duree,coefTrav=coef_act)
            envoi = True

    elif request.method == 'POST' and 'btnsupprimer' in request.POST:
        id_supp = int(request.POST.get('btnsupprimer'))
        Travail.objects.get(id=id_supp).delete()
        return HttpResponseRedirect(request.path_info)

    travails = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Usuelles')
    travails_all = Travail.objects.filter(dossierTrav=dossier)
    duree_tot = calculDureeTotale( travails_all )
    duree_depassee = duree_tot > 24

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
            Travail.objects.create(dossierTrav=dossier,categorieTrav=cat,activiteTrav=act,dureeTrav=duree,coefTrav=coef_act)
            envoi = True

    elif request.method == 'POST' and 'btnsupprimer' in request.POST:
        id_supp = int(request.POST.get('btnsupprimer'))
        Travail.objects.get(id=id_supp).delete()
        return HttpResponseRedirect(request.path_info)

    travails = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Loisirs')
    travails_all = Travail.objects.filter(dossierTrav=dossier)
    duree_tot = calculDureeTotale( travails_all )
    duree_depassee = duree_tot > 24

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
            Travail.objects.create(dossierTrav=dossier,categorieTrav=cat,activiteTrav=act,dureeTrav=duree,coefTrav=coef_act)
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

    travails_all = Travail.objects.filter(dossierTrav=dossier)
    duree_tot = calculDureeTotale( travails_all )
    duree_depassee = duree_tot > 24

    return render(request, 'calculdej/calcdejsport.html', locals())

# Calcul d'une DE en fonction d'une Catégorie et de sa liste d'Activités
def calculDE( cat, activites, MB, TD ):
    global deplacements

    dureeNap = 0
    sommeNap = 0
    for tmp in activites:
        if cat == "Professionnelles":
            dureeNap += tmp.dureeTrav
            sommeNap += (tmp.dureeTrav-Decimal(sum(deplacements))) * tmp.activiteTrav.coef
        if cat == "Loisirs" or cat == "Sportives":
            dureeNap += tmp.dureeTrav/7
            sommeNap += tmp.dureeTrav/7 * tmp.activiteTrav.coef
        if cat == "Usuelles":
            dureeNap += tmp.dureeTrav
            sommeNap += tmp.dureeTrav * tmp.activiteTrav.coef

    if dureeNap == 0:
        return 0
    else:
        if cat == "Professionnelles":
            sommeDeplacements = Decimal(deplacements[0]*2.0 + deplacements[1]*4.0 + deplacements[2]*5.0 + deplacements[3]*7.0)
            nap = (sommeNap+sommeDeplacements) / dureeNap
        else:
            nap = sommeNap / dureeNap

        return float(nap) * float(MB) / float(TD) * float(dureeNap)

@login_required
def calculdejresultat(request):
    global poids
    global taille
    global sexe
    global age
    global pathologie


    MB = 0 # Métabolisme de Base
    TD = 0 # Temps total
    if taille > 0:
        imc = round((poids/((taille/100)*(taille/100))),2)
    else:
        imc = 0

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

    TD = calculDureeTotale( travails )

    # Calcul DE Professionnelles
    DEProfessionnelles = calculDE( "Professionnelles", pros, MB, TD )
    # Calcul DE Usuelles
    DEUsuelles = calculDE( "Usuelles", usuelles, MB, TD )

    # Calcul DE Loisirs
    DELoisirs = calculDE( "Loisirs", loisirs, MB, TD )

    # Calcul DE Sportives
    DESports = calculDE( "Sportives", sports, MB, TD )

    # Calcul DE Totale
    DET = round((DEProfessionnelles+DEUsuelles+DELoisirs+DESports),2)
    DEI = round((DET/24/60),2)
    total = DEProfessionnelles+DEUsuelles+DELoisirs+DESports

    #pourcentages de chaques depenses energetiques
    if total > 0:
        pPro=round(DEProfessionnelles/total,2)*100
        pUse=round(DEUsuelles/total,2)*100
        pLois=round(DELoisirs/total,2)*100
        pSport=round(DESports/total,2)*100



    # Détermination du niveau d'activité journalière
    if DEI < naj1:
        niveau = "faible"
    elif DEI < naj2:
        niveau = "modéré"
    elif DEI < naj3:
        niveau = "intense"
    else:
        niveau = "très intense"

    #on calcul les DE par niveau d intensité
    prosNiveau1 = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Professionnelles').filter(coefTrav__lt=2.49)
    prosNiveau2 = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Professionnelles').filter(coefTrav__gt=2.5).filter(coefTrav__lt=5.0)
    prosNiveau3 = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Professionnelles').filter(coefTrav__gt=5.01)

    sportsNiveau1 = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Sportives').filter(coefTrav__lt=2.49)
    sportsNiveau2 = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Sportives').filter(coefTrav__gt=2.5).filter(coefTrav__lt=5.0)
    sportsNiveau3 = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Sportives').filter(coefTrav__gt=5.01)

    usuellesNiveau1 = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Usuelles').filter(coefTrav__lt=2.49)
    usuellesNiveau2 = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Usuelles').filter(coefTrav__gt=2.5).filter(coefTrav__lt=5.0)
    usuellesNiveau3 = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Usuelles').filter(coefTrav__gt=5.01)

    loisirsNiveau1 = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Loisirs').filter(coefTrav__lt=2.49)
    loisirsNiveau2 = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Loisirs').filter(coefTrav__gt=2.5).filter(coefTrav__lt=5.0)
    loisirsNiveau3 = Travail.objects.filter(dossierTrav=dossier).filter(categorieTrav__typeCat__contains='Loisirs').filter(coefTrav__gt=5.01)


    pros_Niveau1 =calculDE( "Professionnelles", prosNiveau1, MB, TD )
    usuelles_Niveau1=calculDE( "Usuelles", usuellesNiveau1, MB, TD )
    loisirs_Niveau1=calculDE( "Loisirs", loisirsNiveau1, MB, TD )
    sports_Niveau1=calculDE( "Sportives", sportsNiveau1, MB, TD )

    pros_Niveau2 =calculDE( "Professionnelles", prosNiveau2, MB, TD )
    usuelles_Niveau2=calculDE( "Usuelles", usuellesNiveau2, MB, TD )
    loisirs_Niveau2=calculDE( "Loisirs", loisirsNiveau2, MB, TD )
    sports_Niveau2=calculDE( "Sportives", sportsNiveau2, MB, TD )

    pros_Niveau3 =calculDE( "Professionnelles", prosNiveau3, MB, TD )
    usuelles_Niveau3=calculDE( "Usuelles", usuellesNiveau3, MB, TD )
    loisirs_Niveau3=calculDE( "Loisirs", loisirsNiveau3, MB, TD )
    sports_Niveau3=calculDE( "Sportives", sportsNiveau3, MB, TD )

    DENiveau1 = pros_Niveau1+usuelles_Niveau1+loisirs_Niveau1+sports_Niveau1
    DENiveau2 = pros_Niveau2+usuelles_Niveau2+loisirs_Niveau2+sports_Niveau2
    DENiveau3 = pros_Niveau3+usuelles_Niveau3+loisirs_Niveau3+sports_Niveau3

    total=DENiveau1+DENiveau2+DENiveau3

    if total > 0:
        pNiveau1=round(DENiveau1/total,2)*100
        pNiveau2=round(DENiveau2/total,2)*100
        pNiveau3=round(DENiveau3/total,2)*100

        pProsNiveau1=round(pros_Niveau1/total,2)*100
        pProsNiveau2=round(pros_Niveau2/total,2)*100
        pProsNiveau3=round(pros_Niveau3/total,2)*100

        pUsuellesNiveau1=round(usuelles_Niveau1/total,2)*100
        pUsuellesNiveau2=round(usuelles_Niveau2/total,2)*100
        pUsuellesNiveau3=round(usuelles_Niveau3/total,2)*100

        pLoisirsNiveau1=round(loisirs_Niveau1/total,2)*100
        pLoisirsNiveau2=round(loisirs_Niveau2/total,2)*100
        pLoisirsNiveau3=round(loisirs_Niveau3/total,2)*100

        pSportsNiveau1=round(sports_Niveau1/total,2)*100
        pSportsNiveau2=round(sports_Niveau2/total,2)*100
        pSportsNiveau3=round(sports_Niveau3/total,2)*100


    MB = round(MB,2)
    # Enregistrement des informations dans le dossier
    dossier = Dossier.objects.filter(dernier=True).reverse()[0]
    dossier.taille = taille
    dossier.poids = poids
    dossier.age = age
    dossier.sexe = sexe
    dossier.de = DEI
    dossier.pathologie = pathologie

    dossier.dernier=False
    dossier.save()

    if request.method == 'POST' and 'pdf' in request.POST:
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'templates/calculdej/calculdejresultat.html')
        file_pathCss=os.path.join(module_dir, "../static/css/style.css")
        file_pathBase=os.path.join(module_dir, "../templates/baseActivite.html")
        html_string = render_to_string(file_path, {'imc': imc,'DET': DET,'MB': MB,'DEI': DEI,'niveau':niveau})
        HTML(string=html_string).write_pdf("pdfResultats.pdf" ,stylesheets=[CSS(file_pathCss),CSS("https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css")])
        with open("pdfResultats.pdf", 'rb') as pdf:
            response = HttpResponse(pdf.read(),content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=pdfResultats.pdf'
            return response
        pdf.closed

    return render(request, 'calculdej/calculdejresultat.html', locals())



@login_required
def load_act(request):
    cat_d = request.GET.get('cat')
    acts = Activite.objects.filter(categorie=cat_d)
    return render(request, 'calculdej/acts.html',locals())
